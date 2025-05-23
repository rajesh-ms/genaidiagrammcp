# A fixed API server implementation
import os
import json
import logging
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_server")

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"status": "API server is running", "endpoints": ["/generate-diagram"]}

@app.post("/generate-diagram")
async def generate_diagram(request: DiagramRequest):
    """API endpoint to generate a diagram from a natural language description."""
    
    logger.info(f"Received request with output_format={request.output_format}, layout_direction={request.layout_direction}")
    
    # Validate the input
    if not request.architecture_description.strip():
        logger.error("Empty architecture description received")
        raise HTTPException(status_code=400, detail="Architecture description cannot be empty")
    
    # Path to the MCP server script
    mcp_server_path = os.path.join(os.path.dirname(__file__), "fallback_mcp_server.py")
    
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
    
    # Send the request as JSON string with newline
    stdin_data = json.dumps(mcp_request) + "\n"
    
    try:
        # Start the MCP server process
        logger.info("Starting MCP server process")
        process = subprocess.Popen(
            ["python", mcp_server_path],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the request and get the response
        stdout_data, stderr_data = process.communicate(stdin_data)
        
        if process.returncode != 0:
            logger.error(f"MCP server error: {stderr_data}")
            raise HTTPException(status_code=500, detail=f"MCP server error: {stderr_data}")
        
        # Parse the JSON response
        try:
            logger.info("Parsing MCP response")
            mcp_response = json.loads(stdout_data)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse response: {stdout_data[:200]}...")
            raise HTTPException(status_code=500, detail=f"Invalid response from MCP server")
        
        # Check for errors in the response
        if "error" in mcp_response:
            logger.error(f"MCP error: {mcp_response['error']}")
            raise HTTPException(status_code=500, detail=f"MCP error: {mcp_response['error']}")
        
        # Extract the image data
        try:
            image_data = mcp_response["result"]["data"]
            image_format = mcp_response["result"]["format"]
        except KeyError as e:
            logger.error(f"Missing data in response: {e}")
            raise HTTPException(status_code=500, detail=f"Invalid response structure: {e}")
        
        # Return the image data
        logger.info(f"Successfully generated diagram in {image_format} format")
        return {
            "image_data": image_data,
            "image_format": image_format
        }
    
    except Exception as e:
        logger.exception(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

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
