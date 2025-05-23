# Azure Architecture Diagram Generator with MCP

An MCP (Model Context Protocol) Server that generates Azure architecture diagrams from natural language descriptions using AI and the Python diagrams library.

## 🚀 Features

- **Natural Language Processing**: Convert plain English descriptions into structured Azure architecture diagrams
- **MCP Server Integration**: Fully compatible with the Model Context Protocol for seamless integration
- **Multiple Output Formats**: Generate diagrams in PNG or SVG formats
- **Flexible Layouts**: Support for top-to-bottom (TB) and left-to-right (LR) diagram layouts
- **Azure Resource Support**: Comprehensive support for Azure services including Web Apps, Databases, Storage, Networking, and more
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Web Interface**: Simple web client for testing and interaction
- **Fallback Mechanisms**: Robust error handling with fallback servers

## 🏗️ Architecture

- **MCP Server**: Uses FastMCP Python library to create an MCP server
- **AI Processing**: Azure OpenAI API processes natural language descriptions
- **Diagram Generation**: Python `diagrams` library creates visual representations
- **Web Client**: Static HTML interface for testing and demonstration

## 📋 Prerequisites

- Python 3.8+
- Graphviz (required by the diagrams library)
- Azure OpenAI API access (optional, falls back to sample data)
- Docker (for containerized deployment)

## 🛠️ Installation

### Option 1: Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rajesh-ms/genaidiagrammcp.git
   cd genaidiagrammcp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Graphviz**:
   - Windows: Download from [Graphviz website](https://graphviz.org/download/)
   - macOS: `brew install graphviz`
   - Linux: `sudo apt-get install graphviz` (Ubuntu/Debian)

4. **Set up environment variables** (optional):
   ```bash
   cp production.env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

### Option 2: Docker Deployment

1. **Clone and run with Docker**:
   ```bash
   git clone https://github.com/rajesh-ms/genaidiagrammcp.git
   cd genaidiagrammcp
   docker-compose up --build
   ```

## 🚦 Quick Start

### Running the MCP Server

```bash
python azure_diagram_server.py
```

### Running the API Server

```bash
python api_server.py
```

### Using PowerShell Scripts

```powershell
# Start all services
.\Start-Servers.ps1 -RunMcpServer -RunApiServer -OpenWebClient

# Or use individual scripts
.\Start-Docker.ps1      # Start with Docker
.\Stop-Docker.ps1       # Stop Docker services
```

## 🧪 Testing

### Direct MCP Testing

```bash
python test_mcp_direct.py
```

### Validation

```bash
python validate_mcp.py
```

### Web Interface

Open `index.html` in your browser or use the API endpoint:

```bash
curl -X POST http://localhost:8000/generate-diagram \
  -H "Content-Type: application/json" \
  -d '{
    "architecture_description": "A web application with load balancer, two web servers, and a database",
    "output_format": "png",
    "layout_direction": "TB"
  }'
```

## 📖 Usage Examples

### Simple Web Application

```text
"A simple web application with a load balancer, two web servers, and a SQL database"
```

### Microservices Architecture

```text
"A microservices architecture with an API gateway, three microservices (user service, order service, payment service), a message queue, and separate databases for each service"
```

### Multi-tier Application

```text
"A three-tier application with a web tier using App Services, an application tier with Function Apps, and a data tier with Cosmos DB and Blob Storage"
```

## 🔧 Configuration

### Environment Variables

- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT`: Deployment name (default: gpt-4)
- `AZURE_OPENAI_API_VERSION`: API version (default: 2023-05-15)
- `API_HOST`: API server host (default: 127.0.0.1)
- `API_PORT`: API server port (default: 8000)
- `DEPLOYMENT_MODE`: development or production
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Supported Azure Resources

The server supports a wide range of Azure services:

- **Compute**: App Services, Function Apps
- **Database**: SQL Database, Cosmos DB
- **Storage**: Blob Storage, File Storage
- **Networking**: Load Balancers, Application Gateway, Virtual Networks
- **Security**: Key Vault, Active Directory
- **Integration**: Service Bus, Event Grid
- **Analytics**: Synapse Analytics, Power BI
- **AI/ML**: Cognitive Services, Machine Learning

## 🐳 Docker

The project includes comprehensive Docker support:

- `Dockerfile`: Main application container
- `docker-compose.yml`: Complete development environment
- `entrypoint.sh`: Container startup script
- Health checks and automatic restarts

## 📁 Project Structure

```
├── azure_diagram_server.py     # Main MCP server
├── api_server.py              # REST API server
├── index.html                 # Web client interface
├── docker-compose.yml         # Docker configuration
├── requirements.txt           # Python dependencies
├── validate_mcp.py           # Validation script
├── test_mcp_direct.py        # Direct testing script
├── diagrams/                 # Generated diagram outputs
├── .vscode/                  # VS Code configuration
└── scripts/                  # PowerShell management scripts
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Graphviz not found**: Ensure Graphviz is installed and in your PATH
2. **Import errors**: Check that all Python dependencies are installed
3. **Docker issues**: Ensure Docker Desktop is running
4. **API connection**: Verify your Azure OpenAI credentials

### Support

- Check the [Issues](https://github.com/rajesh-ms/genaidiagrammcp/issues) page
- Review the validation gallery at `validation_gallery.html`
- Run the health check scripts in the repository

## 🏷️ Version

Current version: 1.0.0

---

Made with ❤️ for the Azure and MCP communities
