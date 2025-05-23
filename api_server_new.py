import os
import json
import subprocess
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_server")

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware to allow the web client to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiagramRequest(BaseModel):
    architecture_description: str
    output_format: str = "png"
    layout_direction: str = "TB"

@app.get("/")
async def root():
    """Root endpoint to verify the API server is running."""
    return {"status": "API server is running", "endpoints": ["/generate-diagram", "/diagram"]}

@app.post("/generate-diagram")
async def generate_diagram(request: DiagramRequest):
    """API endpoint to generate a diagram from a natural language description."""
    
    logger.info(f"Received request with output_format={request.output_format}, layout_direction={request.layout_direction}")
    
    # Validate the input
    if not request.architecture_description.strip():
        logger.error("Empty architecture description received")
        raise HTTPException(status_code=400, detail="Architecture description cannot be empty")
      # Path to the MCP server script
    mcp_server_path = os.path.join(os.path.dirname(__file__), "azure_diagram_server.py")
    fallback_server_path = os.path.join(os.path.dirname(__file__), "fallback_mcp_server.py")
    logger.info(f"MCP server path: {mcp_server_path}")
    
    # Create an MCP request
    mcp_request = {
        "method": "call_tool",
        "params": {
            "name": "generate_azure_diagram_from_text",
            "arguments": {
                "architecture_description": request.architecture_description,
                "output_format": request.output_format,
                "layout_direction": request.layout_direction
            }
        }
    }
      try:
        # First try the main MCP server
        logger.info("Starting MCP server process")
        process = subprocess.Popen(
            ["python", mcp_server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the request to the MCP server
        stdin_data = json.dumps(mcp_request) + "\n"
        logger.info("Sending request to MCP server")
        stdout_data, stderr_data = process.communicate(stdin_data)
        
        if process.returncode != 0 or "error" in stderr_data:
            logger.warning(f"Main MCP server failed with error: {stderr_data}")
            logger.info("Falling back to simplified MCP server")
            
            # Try with the fallback server
            fallback_process = subprocess.Popen(
                ["python", fallback_server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            fallback_stdout, fallback_stderr = fallback_process.communicate(stdin_data)
            
            if fallback_process.returncode != 0:
                logger.error(f"Fallback MCP server error: {fallback_stderr}")
                raise HTTPException(status_code=500, detail=f"Both MCP servers failed. Error: {fallback_stderr}")
            
            stdout_data = fallback_stdout
            
        # Parse the response
        logger.info("Parsing MCP server response")
        try:
            mcp_response = json.loads(stdout_data)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse MCP server response: {stdout_data}")
            raise HTTPException(status_code=500, detail=f"Failed to parse MCP server response: {stdout_data[:200]}...")
        
        if "error" in mcp_response:
            logger.error(f"MCP error: {mcp_response['error']}")
            raise HTTPException(status_code=500, detail=f"MCP error: {mcp_response['error']}")
        
        # Extract the image data
        logger.info("Extracting image data from MCP response")
        try:
            image_data = mcp_response["result"]["data"]
            image_format = mcp_response["result"]["format"]
        except KeyError as e:
            logger.error(f"Failed to extract image data from MCP response: {e}")
            logger.error(f"MCP response: {mcp_response}")
            raise HTTPException(status_code=500, detail=f"Failed to extract image data from MCP response: {str(e)}")
        
        # Return the image data
        logger.info(f"Successfully generated diagram in {image_format} format")
        return {
            "image_data": image_data,  # This is base64 encoded
            "image_format": image_format
        }
        
    except Exception as e:
        logger.exception(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/diagram")
async def get_diagram():
    """
    Serve the latest generated diagram image.
    """
    diagram_path = os.path.join(os.path.dirname(__file__), "test_diagram.png")
    if not os.path.exists(diagram_path):
        raise HTTPException(status_code=404, detail="Diagram not found")
    return FileResponse(diagram_path, media_type="image/png")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )

if __name__ == "__main__":
    logger.info("Starting API server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
