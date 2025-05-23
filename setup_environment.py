"""
Setup script to fix environment for the Azure Architecture Diagram Generator
"""
import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and print its output"""
    print(f"\n=== {description} ===")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"STDOUT: {result.stdout}")
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    return result.returncode == 0

def setup_virtual_env():
    """Setup or activate virtual environment"""
    if not os.path.exists(".venv"):
        print("Creating virtual environment...")
        if run_command("python -m venv .venv", "Creating virtual environment"):
            print("Virtual environment created.")
        else:
            print("Failed to create virtual environment.")
            return False
    
    # Activate the virtual environment
    if platform.system() == "Windows":
        activate_cmd = r".\.venv\Scripts\activate"
    else:
        activate_cmd = "source .venv/bin/activate"
    
    print(f"Please activate your virtual environment with: {activate_cmd}")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'base_prefix') or sys.base_prefix == sys.prefix:
        print("WARNING: Not running in a virtual environment!")
    
    return True

def install_packages():
    """Install required packages"""
    # Upgrade pip
    run_command("pip install --upgrade pip setuptools wheel", "Upgrading pip and setuptools")
    
    # Install required packages
    packages = [
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0",
        "python-dotenv>=1.0.0",
        "requests>=2.28.0",
        "mcp>=1.5.0",
        "matplotlib>=3.7.0",
        "diagrams>=0.23.0",
        "graphviz"
    ]
    
    # Try installing packages one by one
    for package in packages:
        print(f"Installing {package}...")
        run_command(f"pip install {package}", f"Installing {package}")
    
    # Try to install rsaz-diagrams
    print("Installing rsaz-diagrams...")
    success = run_command("pip install rsaz-diagrams", "Installing rsaz-diagrams")
    
    # If rsaz-diagrams fails, we'll use the regular diagrams package
    if not success:
        print("Failed to install rsaz-diagrams. We'll use the regular diagrams package.")
    
    # Print installed packages
    run_command("pip list", "Installed packages")
    
    return True

def check_graphviz():
    """Check if Graphviz is installed"""
    try:
        import graphviz
        print("Graphviz Python package is installed.")
        
        # Check for graphviz executable
        result = subprocess.run("dot -V", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Graphviz is installed: {result.stdout}")
            return True
        else:
            print("Graphviz executable 'dot' not found in PATH.")
            if platform.system() == "Windows":
                print("Please install Graphviz from: https://graphviz.org/download/")
                print("Then add its bin directory to your PATH.")
            elif platform.system() == "Linux":
                print("Please install Graphviz using: sudo apt-get install graphviz")
            elif platform.system() == "Darwin":  # macOS
                print("Please install Graphviz using: brew install graphviz")
            return False
    except ImportError:
        print("Graphviz Python package not installed.")
        return False

def update_azure_diagram_server():
    """Update the azure_diagram_server.py to use standard diagrams library"""
    if not os.path.exists("azure_diagram_server.py"):
        print("azure_diagram_server.py not found!")
        return False
    
    with open("azure_diagram_server.py", "r") as file:
        content = file.read()
    
    # Check which import style is currently used
    if "from rsaz_diagrams" in content:
        print("Updating imports to use standard diagrams library...")
        
        # Replace imports
        content = content.replace("from rsaz_diagrams", "from diagrams")
        
        with open("azure_diagram_server.py", "w") as file:
            file.write(content)
        
        print("Updated azure_diagram_server.py to use standard diagrams library.")
    else:
        print("azure_diagram_server.py already uses standard diagrams library.")
    
    return True

def main():
    """Main function"""
    print("=== Azure Architecture Diagram Generator Environment Setup ===")
    
    # Setup virtual environment
    if not setup_virtual_env():
        return 1
    
    # Install packages
    if not install_packages():
        return 1
    
    # Check for Graphviz
    if not check_graphviz():
        print("WARNING: Graphviz may not be properly installed. Diagrams generation may fail.")
    
    # Update azure_diagram_server.py if needed
    if not update_azure_diagram_server():
        return 1
    
    print("\n=== Setup Complete ===")
    print("Please run check_health.py to verify that everything is working correctly.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
