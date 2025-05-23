# Setup and run script for Azure Architecture Diagram Generator
param(
    [switch]$InstallDependencies,
    [switch]$RunMcpServer,
    [switch]$RunApiServer,
    [switch]$OpenWebClient
)

# Function to print colorful messages
function Write-ColorOutput($message, $color) {
    Write-Host $message -ForegroundColor $color
}

# Check if we should install dependencies
if ($InstallDependencies) {
    Write-ColorOutput "Installing Python dependencies..." "Yellow"
    pip install "mcp[server]" diagrams requests graphviz python-dotenv fastapi uvicorn
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "Dependencies installed successfully!" "Green"
    } else {
        Write-ColorOutput "Failed to install dependencies." "Red"
        exit 1
    }
}

# Check if .env file exists and prompt to create if not
if (-not (Test-Path ".\.env")) {
    Write-ColorOutput "No .env file found. Let's create one..." "Yellow"
    $apiKey = Read-Host "Enter your Azure OpenAI API key"
    $endpoint = Read-Host "Enter your Azure OpenAI endpoint URL"
    $deployment = Read-Host "Enter your Azure OpenAI deployment name (default: gpt-4)"
    
    if ([string]::IsNullOrEmpty($deployment)) {
        $deployment = "gpt-4"
    }
    
    $envContent = @"
# Azure OpenAI API Credentials
AZURE_OPENAI_API_KEY=$apiKey
AZURE_OPENAI_ENDPOINT=$endpoint
AZURE_OPENAI_DEPLOYMENT=$deployment
"@
    
    try {
        Set-Content -Path ".\.env" -Value $envContent
        Write-ColorOutput ".env file created successfully!" "Green"
    } catch {
        Write-ColorOutput "Failed to create .env file: $_" "Red"
        exit 1
    }
} else {
    Write-ColorOutput ".env file already exists. Using existing configuration." "Green"
}

# Start servers based on parameters
$processes = @()

if ($RunMcpServer) {
    Write-ColorOutput "Starting MCP Server..." "Cyan"
    Start-Process -NoNewWindow python -ArgumentList "azure_diagram_server.py" -PassThru | ForEach-Object { $processes += $_ }
}

if ($RunApiServer) {
    Write-ColorOutput "Starting API Server..." "Cyan"
    Start-Process -NoNewWindow python -ArgumentList "api_server.py" -PassThru | ForEach-Object { $processes += $_ }
}

if ($OpenWebClient) {
    Write-ColorOutput "Opening Web Client..." "Cyan"
    Start-Process -NoNewWindow explorer -ArgumentList "index.html"
}

if ($RunMcpServer -or $RunApiServer) {
    Write-ColorOutput "Servers are running. Press CTRL+C to stop." "Green"
    try {
        # Keep the script running
        while ($true) {
            Start-Sleep -Seconds 1
        }
    } finally {
        # Clean up processes when the script is terminated
        foreach ($process in $processes) {
            if (-not $process.HasExited) {
                Write-ColorOutput "Stopping process with ID $($process.Id)..." "Yellow"
                Stop-Process -Id $process.Id -Force
            }
        }
    }
}
