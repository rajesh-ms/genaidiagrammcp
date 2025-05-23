# Azure Architecture Diagram Generator with MCP

This project uses the Model Context Protocol (MCP) to generate Azure architecture diagrams from natural language descriptions. It provides a web interface for users to describe their Azure architecture and view the generated diagram.

## Features

- **Natural Language Processing**: Converts text descriptions into structured JSON representations of Azure architectures using Azure OpenAI API
- **Diagram Generation**: Creates visual diagrams from the structured JSON using the `diagrams` or `rsaz-diagrams` library
- **MCP Server**: Exposes the functionality through an MCP server
- **Web Client**: Provides a responsive web interface to interact with the system

## Architecture

The system consists of three main components:

1. **MCP Server** (`azure_diagram_server.py`): Processes natural language descriptions and generates diagrams
2. **API Server** (`api_server.py`): Acts as a bridge between the web client and the MCP server
3. **Web Client** (`index.html`): Provides a user interface for entering architecture descriptions and viewing diagrams

## Prerequisites

- Python 3.8+
- Graphviz (must be installed separately and added to PATH)
- Azure OpenAI API access (optional but recommended for better results)

## Installation

1. Clone this repository

2. Set up the environment:

```powershell
# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Install Graphviz:
   - **Windows**: Download from [Graphviz Downloads](https://graphviz.org/download/) and add to PATH
   - **macOS**: `brew install graphviz`
   - **Linux**: `apt-get install graphviz`

4. Configure Azure OpenAI API:
   - Create a `.env` file in the project root with your Azure OpenAI credentials

## Running the Application

### Using Docker (Recommended)

The easiest way to run the application is using Docker:

```bash
# Build and start the Docker container
docker-compose up -d

# Check the logs
docker-compose logs -f
```

Once the container is running, you can access the web interface by opening `index.html` in your browser.

### Using the Setup Script

Run the provided setup script to install dependencies and configure the environment:

```powershell
.\setup.bat
```

### Using PowerShell Script

The `Start-Servers.ps1` script provides a convenient way to run all services:

```powershell
# Start all services
.\Start-Servers.ps1 -RunMcpServer -RunApiServer -OpenWebClient
```

### Running Services Individually

1. **Run the MCP Server**:
   ```powershell
   python azure_diagram_server.py
   ```

2. **Run the API Server**:
   ```powershell
   python api_server.py
   ```

3. **Open the Web Client**:
   - Open `index.html` in a web browser

## Health Check

To ensure all services are running correctly:

```powershell
python check_health.py
```

## Using the Web Interface

1. Open `index.html` in a web browser
2. Enter a natural language description of your Azure architecture
3. Select output format and layout direction
4. Click "Generate Diagram"
5. View and download the generated diagram

## Example Descriptions

1. **Simple Web App**:
   ```
   I need a simple architecture with a web application connected to a SQL Database. Both resources should be in the East US region. The web app should be on a Standard S1 tier and the database on S2. Place everything in a single resource group called 'WebApp-RG'.
   ```

2. **Multi-Tier Application**:
   ```
   Create a multi-tier application with a front-end web app, a middle-tier API app, and a back-end SQL database. Add blob storage for file uploads. The front-end connects to the API, and the API connects to both the database and storage.
   ```

## Direct API Access

The API server provides the following endpoints:

- `GET /`: Health check endpoint
- `POST /generate-diagram`: Generate a diagram from a description
- `GET /diagram`: Retrieve the latest generated diagram

## Docker Deployment

This project includes Docker configuration for easy deployment:

### Prerequisites for Docker Deployment

- Docker and Docker Compose installed on your system
- .env file with Azure OpenAI API credentials (optional)

### Building and Running the Docker Container

#### Option 1: Using Docker Manager (Recommended for Windows)

The project includes a PowerShell script for easy Docker management:

```powershell
# Build and start the container
.\Docker-Manager.ps1 -Build -Start

# Check container health
.\Docker-Manager.ps1 -Check

# View container logs
.\Docker-Manager.ps1 -Logs

# Restart the container
.\Docker-Manager.ps1 -Restart

# Stop the container
.\Docker-Manager.ps1 -Stop

# Show help
.\Docker-Manager.ps1 -Help
```

#### Option 2: Using Docker Compose Directly

```bash
# Build the Docker image
docker-compose build

# Start the container in the background
docker-compose up -d

# Check the logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Docker Container Structure

The Docker container runs both the MCP server and the API server:

1. The MCP server runs in the background
2. The API server runs in the foreground and listens on port 8000
3. The web client can be accessed by opening `index.html` in your browser

### Accessing the Dockerized API

When running in Docker, the API server will be available at:

- Local development: http://localhost:8000
- Remote access: http://<your-server-ip>:8000

## Troubleshooting

### General Issues

If you encounter issues:

1. Check if the `.env` file is properly configured
2. Verify that Graphviz is installed and in your PATH
3. Ensure all services are running
4. Check the console output for error messages

### Docker-Specific Issues

1. **Container not starting**:
   - Check Docker logs: `docker-compose logs`
   - Verify that port 8000 is not in use by another application

2. **API server not accessible**:
   - Ensure the container is running: `docker ps`
   - Check if the API server started correctly: `docker-compose logs azure-diagram-generator`
   - Try accessing the API directly: http://localhost:8000

3. **Web client cannot connect to API**:
   - Make sure the API server is running and accessible
   - Check browser console for CORS errors (you may need to modify CORS settings)

4. **Graphviz errors**:
   - The Docker container includes Graphviz, but if you see errors, check the logs
   - Try rebuilding the container: `docker-compose build --no-cache`

## License

[MIT License](LICENSE)
{
    "mcpServers": {
        "azure-diagram-generator": {
            "command": "python",
            "args": [
                "C:\\ABSOLUTE\\PATH\\TO\\azure_diagram_server.py"
            ]
        }
    }
}
```

Replace `C:\\ABSOLUTE\\PATH\\TO\\` with the absolute path to where you saved the server file.

3. Restart Claude for Desktop.

## Using the Web Client

The web client (`index.html`) can interact with the MCP server through the API server:

1. Start the API server:

```bash
python api_server.py
```

2. Open the `index.html` file in your preferred web browser.
3. Enter a description of your Azure architecture in the text area.
4. Choose the output format (PNG or SVG) and layout direction.
5. Click "Generate Diagram" to create and display the diagram.

The web client will attempt to connect to the API server running at `http://127.0.0.1:8000`. If it can't connect, it will fall back to simulation mode with a placeholder diagram.

## Example Architecture Descriptions

Here are some examples you can try:

1. **Simple Web App**: "A web app connected to a SQL database, all within a single resource group."

2. **Multi-Tier Application**: "A front-end web app, a middle-tier API app, and a back-end SQL database with a blob storage for file uploads."

3. **Microservices Architecture**: "Three microservices communicating through a service bus, with each microservice having its own database."

## Limitations

- The web client currently uses simulated responses and doesn't connect to the actual MCP server.
- The diagram generation is dependent on Graphviz being properly installed.
- Without Azure OpenAI API credentials, the server will return a simple sample diagram.

## Future Improvements

- Implement proper communication between the web client and MCP server
- Add more Azure resource types to the diagrams mapping
- Improve error handling and user feedback
- Add support for more diagram customization options
