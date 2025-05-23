import sys
import json
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Sample MCP request to test the server
test_request = {
    "method": "call_tool",
    "params": {
        "name": "generate_azure_diagram_from_text",
        "arguments": {
            "architecture_description": "A web application with a SQL Database backend, protected by a firewall.",
            "output_format": "png",
            "layout_direction": "TB"
        }
    }
}

# Write the request to stdout
print(json.dumps(test_request))
sys.stdout.flush()

# Read the response from stdin
response_text = sys.stdin.readline()
response = json.loads(response_text)

if "result" in response and "data" in response["result"]:
    # Decode base64 image
    image_data = base64.b64decode(response["result"]["data"])
    
    # Save the image
    with open("test_diagram.png", "wb") as f:
        f.write(image_data)
    
    print("Diagram successfully generated and saved as test_diagram.png")
else:
    print(f"Error: {response.get('error', 'Unknown error')}")
