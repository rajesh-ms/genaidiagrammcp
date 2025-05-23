#!/usr/bin/env python3
"""
Validation script for the Azure Diagram Generator MCP Server.
This script tests the MCP server by creating sample Azure diagrams.
"""

import asyncio
import os
import sys
import base64
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the MCP server module
from azure_diagram_server import generate_azure_diagram_from_text

async def test_simple_web_app():
    """Test generating a simple web app architecture diagram."""
    print("🔹 Testing Simple Web App Architecture...")
    
    description = """
    I need a simple architecture with a web application connected to a SQL Database. 
    Both resources should be in the East US region. The web app should be on a Standard S1 tier 
    and the database on S2. Place everything in a single resource group called 'WebApp-RG'.
    """
    
    try:
        result = await generate_azure_diagram_from_text(
            architecture_description=description,
            output_format="png",
            layout_direction="TB"
        )
        
        if result and result.data:
            # Save the diagram to a file
            diagram_path = Path("./diagrams/simple_web_app_test.png")
            diagram_path.parent.mkdir(exist_ok=True)
            
            with open(diagram_path, "wb") as f:
                f.write(base64.b64decode(result.data))
            
            print(f"✅ Simple Web App diagram generated successfully: {diagram_path}")
            return True
        else:
            print("❌ Failed to generate Simple Web App diagram")
            return False
            
    except Exception as e:
        print(f"❌ Error generating Simple Web App diagram: {str(e)}")
        return False

async def test_microservices_architecture():
    """Test generating a microservices architecture diagram."""
    print("🔹 Testing Microservices Architecture...")
    
    description = """
    Design a microservices architecture with three services: UserService, OrderService, 
    and ProductService. Each service has its own database. The services communicate 
    through an Azure Service Bus. Include Azure Key Vault for secrets management. 
    Protect the architecture with Azure Active Directory. Place everything in the 
    Central US region within a single virtual network.
    """
    
    try:
        result = await generate_azure_diagram_from_text(
            architecture_description=description,
            output_format="png",
            layout_direction="LR"
        )
        
        if result and result.data:
            # Save the diagram to a file
            diagram_path = Path("./diagrams/microservices_test.png")
            diagram_path.parent.mkdir(exist_ok=True)
            
            with open(diagram_path, "wb") as f:
                f.write(base64.b64decode(result.data))
            
            print(f"✅ Microservices diagram generated successfully: {diagram_path}")
            return True
        else:
            print("❌ Failed to generate Microservices diagram")
            return False
            
    except Exception as e:
        print(f"❌ Error generating Microservices diagram: {str(e)}")
        return False

async def test_multi_tier_application():
    """Test generating a multi-tier application diagram."""
    print("🔹 Testing Multi-Tier Application...")
    
    description = """
    Create a multi-tier application with a front-end web app, a middle-tier API app, 
    and a back-end SQL database. Add blob storage for file uploads. The front-end 
    connects to the API, and the API connects to both the database and storage. 
    All resources should be in the West US 2 region. Group the web and API apps 
    in a 'Frontend-RG' resource group and the database and storage in a 'Backend-RG' 
    resource group.
    """
    
    try:
        result = await generate_azure_diagram_from_text(
            architecture_description=description,
            output_format="svg",
            layout_direction="TB"
        )
        
        if result and result.data:
            # Save the diagram to a file
            diagram_path = Path("./diagrams/multi_tier_test.svg")
            diagram_path.parent.mkdir(exist_ok=True)
            
            with open(diagram_path, "wb") as f:
                f.write(base64.b64decode(result.data))
            
            print(f"✅ Multi-tier diagram generated successfully: {diagram_path}")
            return True
        else:
            print("❌ Failed to generate Multi-tier diagram")
            return False
            
    except Exception as e:
        print(f"❌ Error generating Multi-tier diagram: {str(e)}")
        return False

async def main():
    """Main validation function."""
    print("🚀 Starting Azure Diagram Generator MCP Server Validation...")
    print("=" * 60)
    
    # Create diagrams directory if it doesn't exist
    Path("./diagrams").mkdir(exist_ok=True)
    
    # Run all tests
    tests = [
        test_simple_web_app(),
        test_microservices_architecture(),
        test_multi_tier_application()
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    # Count successful tests
    successful_tests = sum(1 for result in results if result is True)
    total_tests = len(tests)
    
    print("=" * 60)
    print(f"📊 Validation Results: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! MCP server is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
