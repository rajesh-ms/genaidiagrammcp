import os
import base64
import json
import logging
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP, Image
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fallback_mcp_server")

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("azure-diagram-generator-fallback")

def generate_simple_diagram(architecture_description: str, output_format: str = "png") -> bytes:
    """
    Generate a simple fallback diagram using matplotlib.
    This is used when the full diagram generation is not available.
    """
    # Create a simple diagram with matplotlib
    plt.figure(figsize=(10, 6))
    
    # Add a title
    plt.title("Azure Architecture Diagram (Fallback Mode)", fontsize=16)
    
    # Add a border
    plt.axhline(y=0, color='blue', linestyle='-', alpha=0.3)
    plt.axhline(y=1, color='blue', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='blue', linestyle='-', alpha=0.3)
    plt.axvline(x=1, color='blue', linestyle='-', alpha=0.3)
    
    # Add the description as text
    plt.text(0.5, 0.7, "This is a fallback diagram.", 
             horizontalalignment='center', fontsize=14)
    plt.text(0.5, 0.6, "The full diagram generation requires Graphviz to be installed.", 
             horizontalalignment='center', fontsize=12)
    plt.text(0.5, 0.5, "Description:", 
             horizontalalignment='center', fontsize=12, fontweight='bold')
    
    # Split the description into lines for better display
    lines = []
    words = architecture_description.split()
    current_line = ""
    for word in words[:100]:  # Limit to first 100 words
        if len(current_line + " " + word) > 60:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # Add the description lines
    y_pos = 0.45
    for line in lines[:10]:  # Limit to 10 lines
        plt.text(0.5, y_pos, line, horizontalalignment='center', fontsize=10)
        y_pos -= 0.03
    
    if len(lines) > 10:
        plt.text(0.5, y_pos, "...", horizontalalignment='center', fontsize=10)
    
    # Remove axes
    plt.axis('off')
    
    # Save the diagram to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format=output_format, bbox_inches='tight')
    plt.close()
    
    # Get the bytes
    buf.seek(0)
    img_bytes = buf.getvalue()
    
    # Return raw bytes
    return img_bytes

@mcp.tool()
async def generate_azure_diagram_from_text(
    architecture_description: str,
    output_format: str = "png",
    layout_direction: str = "TB"
) -> Image:
    """Generate an Azure architecture diagram from a natural language description."""
    logger.info(f"Generating fallback diagram for: {architecture_description[:100]}...")
    
    # Generate simple diagram
    diagram_bytes = generate_simple_diagram(architecture_description, output_format)
    
    # Create base64 encoded data for MCP Image
    diagram_data = base64.b64encode(diagram_bytes).decode('utf-8')
    
    return Image(data=diagram_data, format=output_format)

if __name__ == "__main__":
    logger.info("Starting Fallback MCP server for Azure architecture diagram generation")
    mcp.run(transport='stdio')
