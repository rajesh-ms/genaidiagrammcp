#!/usr/bin/env python3
"""
Docker health check script for Azure Architecture Diagram Generator.
"""

import os
import sys
import requests
import subprocess
import time
import json

def check_docker_running():
    """Check if Docker is running."""
    try:
        subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✅ Docker is running")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Docker is not running or not installed")
        return False

def check_container_running():
    """Check if the Azure Diagram Generator container is running."""
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "-q", "azure-diagram-generator"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            print("✅ Azure Diagram Generator container is running")
            return True
        else:
            print("❌ Azure Diagram Generator container is not running")
            return False
    except subprocess.SubprocessError:
        print("❌ Could not check container status")
        return False

def check_api_accessible():
    """Check if the API server is accessible."""
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ API server is accessible")
            return True
        else:
            print(f"❌ API server returned status code {response.status_code}")
            return False
    except requests.RequestException:
        print("❌ Could not connect to API server")
        return False

def check_diagram_generation():
    """Test diagram generation through the API."""
    try:
        response = requests.post(
            "http://localhost:8000/generate-diagram",
            json={
                "architecture_description": "A simple web app and database",
                "output_format": "png",
                "layout_direction": "TB"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Diagram generation works")
            return True
        else:
            print(f"❌ Diagram generation failed with status code {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
    except requests.RequestException as e:
        print(f"❌ Error during diagram generation test: {e}")
        return False

def get_container_logs(lines=20):
    """Get the container logs."""
    try:
        result = subprocess.run(
            ["docker-compose", "logs", "--tail", str(lines), "azure-diagram-generator"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.SubprocessError:
        return "Could not get container logs"

def main():
    """Main function."""
    print("=== Azure Architecture Diagram Generator Docker Health Check ===")
    
    docker_ok = check_docker_running()
    if not docker_ok:
        print("\n❌ Docker is not running. Please start Docker and try again.")
        return 1
    
    container_ok = check_container_running()
    if not container_ok:
        print("\n❌ Container is not running. Please start it with 'docker-compose up -d'")
        return 1
    
    api_ok = check_api_accessible()
    if api_ok:
        diagram_ok = check_diagram_generation()
    else:
        diagram_ok = False
        print("\nCannot test diagram generation because API server is not accessible")
    
    print("\n=== Summary ===")
    print(f"Docker running: {'✅' if docker_ok else '❌'}")
    print(f"Container running: {'✅' if container_ok else '❌'}")
    print(f"API accessible: {'✅' if api_ok else '❌'}")
    print(f"Diagram generation: {'✅' if diagram_ok else '❌'}")
    
    if not (docker_ok and container_ok and api_ok and diagram_ok):
        print("\n=== Recent Container Logs ===")
        logs = get_container_logs()
        print(logs)
        
        print("\n=== Recommendations ===")
        if not docker_ok:
            print("- Start Docker Desktop or Docker service")
        if not container_ok:
            print("- Start the container with 'docker-compose up -d'")
        if not api_ok:
            print("- Check container logs for API server errors")
            print("- Ensure port 8000 is not being used by another application")
        if not diagram_ok:
            print("- Check if the MCP server started correctly in the container")
            print("- Verify the Azure OpenAI API credentials in your .env file")
        
        return 1
    else:
        print("\n✅ All checks passed! The Docker deployment is working correctly.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
