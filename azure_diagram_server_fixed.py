import os
import tempfile
import json
import base64
from typing import Optional
import requests
import sys
import logging
from mcp.server.fastmcp import FastMCP, Image
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

# Try to import rsaz_diagrams, but handle import errors gracefully
try:
    from diagrams import Diagram, Cluster
    from diagrams.azure.compute import AppServices
    from diagrams.azure.database import SQLDatabases
    from diagrams.azure.storage import BlobStorage
    from diagrams.azure.network import LoadBalancers, ApplicationGateway, VirtualNetworks
    from diagrams.azure.identity import ActiveDirectory
    from diagrams.azure.security import KeyVaults
    from diagrams.azure.integration import ServiceBus
    from diagrams.azure.analytics import SynapseAnalytics
    from diagrams.azure.aiml import CognitiveServices
    from diagrams.azure.web import AppServicePlans
    DIAGRAMS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import diagrams library: {e}")
    logger.error("Make sure diagrams/rsaz-diagrams and Graphviz are installed and in your PATH.")
    DIAGRAMS_AVAILABLE = False

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("azure-diagram-generator")

# Define Azure OpenAI API credentials (these should be set in environment variables)
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")

# Map Azure resource types to diagrams library components
AZURE_NODE_MAP = {
    "Azure.WebApp": AppServices,
    "Azure.SQLDatabase": SQLDatabases,
    "Azure.BlobStorage": BlobStorage,
    "Azure.LoadBalancer": LoadBalancers,
    "Azure.ApplicationGateway": ApplicationGateway,
    "Azure.VirtualNetwork": VirtualNetworks,
    "Azure.ActiveDirectory": ActiveDirectory,
    "Azure.KeyVault": KeyVaults,
    "Azure.ServiceBus": ServiceBus,
    "Azure.PowerBI": SynapseAnalytics,
    "Azure.CognitiveServices": CognitiveServices,
    "Azure.AppServicePlan": AppServicePlans,
    # Add more mappings as needed
}

def process_text_with_azure_openai(architecture_description: str) -> dict:
    """
    Process the natural language architecture description using Azure OpenAI.
    Returns a structured JSON representation of the architecture.
    """
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
        # For demo purposes, return a sample JSON if no API key is available
        return {
            "diagram_label": "Sample Web App Architecture",
            "resources": [
                {
                    "name": "Web App",
                    "type": "Azure.WebApp",
                    "attributes": {
                        "location": "East US",
                        "sku": "S1"
                    }
                },
                {
                    "name": "SQL Database",
                    "type": "Azure.SQLDatabase",
                    "attributes": {
                        "location": "East US",
                        "sku": "S2"
                    }
                }
            ],
            "relationships": [
                {
                    "source": "Web App",
                    "target": "SQL Database",
                    "type": "connects_to"
                }
            ],
            "clusters": [
                {
                    "name": "Resource Group 1",
                    "resources": ["Web App", "SQL Database"]
                }
            ]
        }
    
    prompt = f"""
    Analyze the following Azure architecture description and convert it into a structured JSON format.
    Follow these guidelines:
    
    1. Identify Azure services, their names, and relevant attributes
    2. Recognize relationships between these services
    3. Understand grouping or clustering (e.g., resources within a resource group or subnet)
    4. Output the extracted information in the following structured JSON format:
    
    {{
      "diagram_label": "...",
      "resources": [
        {{
          "name": "...",
          "type": "Azure.[ResourceType]",
          "attributes": {{
            "location": "...",
            "sku": "..."
          }}
        }}
      ],
      "relationships": [
        {{
          "source": "...",
          "target": "...",
          "type": "..."
        }}
      ],
      "clusters": [
        {{
          "name": "...",
          "resources": ["...", "..."]
        }}
      ]
    }}
    
    Only include resources, relationships, and clusters that are explicitly mentioned or can be directly inferred from the description.
    Use only valid Azure resource types prefixed with "Azure." for the "type" field.
    Make sure all resource names used in relationships and clusters match exactly with the resource names defined.
    
    Architecture Description:
    {architecture_description}
    """
    
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    
    body = {
        "messages": [
            {"role": "system", "content": "You are an AI assistant that extracts Azure architecture information from text descriptions and converts it to structured JSON."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.3
    }
    
    # Get API version from env or use default
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    
    try:
        response = requests.post(
            f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={api_version}",
            headers=headers,
            json=body,
            timeout=30  # Add a 30-second timeout
        )
        
        if response.status_code != 200:
            logger.error(f"Azure OpenAI API request failed: {response.text}")
            raise Exception(f"Azure OpenAI API request failed: {response.text}")
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Extract JSON from the response
        try:
            # First attempt: try to parse the whole content as JSON
            arch_json = json.loads(content)
        except json.JSONDecodeError:
            # Second attempt: try to extract JSON from the content
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > 0:
                arch_json = json.loads(content[json_start:json_end])
            else:
                raise Exception("Failed to extract JSON from Azure OpenAI response")
        
        return arch_json
    except requests.exceptions.Timeout:
        logger.error("Azure OpenAI API request timed out")
        raise Exception("Azure OpenAI API request timed out after 30 seconds")
    except Exception as e:
        logger.exception(f"Error calling Azure OpenAI API: {str(e)}")
        raise Exception(f"Error calling Azure OpenAI API: {str(e)}")

def generate_diagram_from_json(arch_json: dict, output_format: str = "png", layout_direction: str = "TB") -> bytes:
    """
    Generate a diagram from the structured JSON representation of the architecture using diagrams.
    Returns the diagram as bytes.
    """
    if not DIAGRAMS_AVAILABLE:
        raise Exception("diagrams library is not available. Please install it.")
    # Create a temporary file to save the diagram
    with tempfile.TemporaryDirectory() as tmpdirname:
        diagram_path = os.path.join(tmpdirname, "diagram")
        # Create the diagram
        with Diagram(arch_json.get("diagram_label", "Azure Architecture"), 
                    filename=diagram_path, 
                    direction=layout_direction,
                    outformat=output_format,
                    show=False) as diagram:
            # Dictionary to keep track of created nodes
            nodes = {}
            # Process clusters first
            cluster_objects = {}
            cluster_resource_mapping = {}
            for cluster_info in arch_json.get("clusters", []):
                cluster_name = cluster_info.get("name", "Cluster")
                cluster = Cluster(cluster_name)
                cluster_objects[cluster_name] = cluster
                # Map resources to their clusters
                for resource_name in cluster_info.get("resources", []):
                    cluster_resource_mapping[resource_name] = cluster_name
            # Create nodes for resources
            for resource in arch_json.get("resources", []):
                resource_name = resource.get("name", "Resource")
                resource_type = resource.get("type", "Azure.WebApp")
                # Get the diagram node class
                node_class = AZURE_NODE_MAP.get(resource_type, AppServices)
                # Create the node in the appropriate cluster or directly in the diagram
                if resource_name in cluster_resource_mapping:
                    cluster_name = cluster_resource_mapping[resource_name]
                    with cluster_objects[cluster_name]:
                        nodes[resource_name] = node_class(resource_name)
                else:
                    nodes[resource_name] = node_class(resource_name)
            # Create relationships between nodes
            for relationship in arch_json.get("relationships", []):
                source_name = relationship.get("source")
                target_name = relationship.get("target")
                if source_name in nodes and target_name in nodes:
                    nodes[source_name] >> nodes[target_name]
        # Read the generated diagram file
        output_path = f"{diagram_path}.{output_format}"
        with open(output_path, "rb") as f:
            diagram_bytes = f.read()
        return diagram_bytes

@mcp.tool()
async def generate_azure_diagram_from_text(
    architecture_description: str,
    output_format: str = "png",
    layout_direction: str = "TB"
) -> Image:
    """
    Generate an Azure architecture diagram from a natural language description.
    
    Args:
        architecture_description: A natural language description of the Azure architecture.
        output_format: The output format of the diagram (png or svg). Default: png.
        layout_direction: The layout direction of the diagram (TB for top-to-bottom or LR for left-to-right). Default: TB.
    
    Returns:
        An image of the generated diagram.
    """
    logger.info(f"Processing architecture description: {architecture_description[:100]}...")
    
    try:
        # Process the text with Azure OpenAI to get a structured JSON representation
        arch_json = process_text_with_azure_openai(architecture_description)
        
        logger.info("Successfully processed architecture description")
        
        # Generate the diagram from the JSON
        diagram_bytes = generate_diagram_from_json(arch_json, output_format, layout_direction)
        
        logger.info(f"Generated diagram ({len(diagram_bytes)} bytes)")
        
        # Base64 encode the diagram bytes
        diagram_data = base64.b64encode(diagram_bytes).decode('utf-8')
        
        logger.info("Returning image data")
        
        # Return the diagram as an image
        return Image(data=diagram_data, format=output_format)
    except Exception as e:
        # In case of an error, return a text error message
        logger.exception(f"Error generating diagram: {str(e)}")
        raise Exception(f"Error generating diagram: {str(e)}")

if __name__ == "__main__":
    print("Starting Azure Diagram Generator MCP Server...")
    mcp.run(transport='stdio')
