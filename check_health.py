import requests
import os
import sys
import time

def check_api_server():
    """Check if the API server is running."""
    try:
        response = requests.get("http://127.0.0.1:8000")
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server at http://127.0.0.1:8000")
        return False

def check_mcp_server():
    """
    Check if the MCP server is running.
    Note: MCP server checks are indirect since we communicate with it through the API server.
    """
    print("ℹ️ MCP server checks are performed through the API server")
    print("ℹ️ Attempting a simple diagram generation to test MCP server...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/generate-diagram",
            json={
                "architecture_description": "A simple web app and database",
                "output_format": "png",
                "layout_direction": "TB"
            }
        )
        
        if response.status_code == 200:
            print("✅ MCP server is responding through the API server")
            return True
        else:
            print(f"❌ MCP server test failed with status code {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server to test MCP server")
        return False

def check_env_file():
    """Check if the .env file exists and has required variables."""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
    
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT"
    ]
    
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables in .env: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ .env file found with required variables")
        return True

def main():
    print("=== Azure Architecture Diagram Generator Health Check ===")
    print(f"Current working directory: {os.getcwd()}")
    print("Checking servers and configuration...")
    
    env_ok = check_env_file()
    api_ok = check_api_server()
    
    if api_ok:
        mcp_ok = check_mcp_server()
    else:
        mcp_ok = False
        print("ℹ️ Skipping MCP server check since API server is not running")
    
    print("\n=== Summary ===")
    print(f"Environment configuration: {'✅' if env_ok else '❌'}")
    print(f"API server: {'✅' if api_ok else '❌'}")
    print(f"MCP server: {'✅' if mcp_ok else '❌'}")
    
    if not (env_ok and api_ok and mcp_ok):
        print("\n=== Recommendations ===")
        if not env_ok:
            print("- Create or fix the .env file with required Azure OpenAI credentials")
        if not api_ok:
            print("- Start the API server using the 'Run API Server' task or 'python api_server.py'")
        if not mcp_ok and api_ok:
            print("- Check the MCP server configuration and make sure Azure OpenAI API credentials are correct")
        
        print("\nYou can start all services at once with the 'Run All Services' task or 'pwsh -File Start-Servers.ps1 -RunMcpServer -RunApiServer'")
        return 1
    else:
        print("\n✅ All checks passed! The system should be working correctly.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
