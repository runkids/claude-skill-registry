---
name: docker-mcp
description: Docker management via MCP protocol. Use when the user wants to interact with Docker on their system - listing containers, images, managing container lifecycle (start/stop/restart), viewing logs, executing commands in containers, pulling images, running new containers, or working with docker-compose files.
---

# Docker MCP Server

This skill provides comprehensive Docker management capabilities through the Model Context Protocol (MCP). It enables Claude to interact with Docker directly on the user's macOS system.

## Installation

### Prerequisites

- Docker Desktop for Mac installed and running
- Python 3.10 or higher
- MCP package: `pip install mcp`

### Setup Steps

1. **Install the MCP package** (if not already installed):
   ```bash
   pip install mcp
   ```

2. **Configure Claude Desktop** to use this MCP server by editing your Claude Desktop config file at:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

3. **Add the server configuration**:
   ```json
   {
     "mcpServers": {
       "docker": {
         "command": "python3",
         "args": ["/path/to/docker-mcp/scripts/docker_mcp_server.py"]
       }
     }
   }
   ```
   
   Replace `/path/to/docker-mcp/` with the actual path to where this skill is saved.

4. **Restart Claude Desktop** for changes to take effect

## Available Tools

The MCP server provides the following Docker operations:

### Container Management
- **docker_ps** - List containers (running or all)
- **docker_start** - Start stopped containers
- **docker_stop** - Stop running containers
- **docker_restart** - Restart containers
- **docker_rm** - Remove containers
- **docker_logs** - View container logs
- **docker_exec** - Execute commands in running containers
- **docker_stats** - View resource usage statistics
- **docker_inspect** - Get detailed container/image information

### Image Management
- **docker_images** - List Docker images
- **docker_pull** - Pull images from registry
- **docker_rmi** - Remove images
- **docker_run** - Create and start new containers

### Docker Compose
- **docker_compose_up** - Start services from compose file
- **docker_compose_down** - Stop and remove compose services

### Networking & Volumes
- **docker_network_ls** - List networks
- **docker_volume_ls** - List volumes

## Usage Examples

Once configured, you can ask Claude to:
- "Show me all running Docker containers"
- "Pull the latest nginx image"
- "Start the container named my-app"
- "Show me the logs for container xyz"
- "Execute 'ls -la' in the nginx container"
- "Run a new container from ubuntu:latest"
- "Start my docker-compose services"

## Troubleshooting

If the MCP server isn't working:

1. Verify Docker is running: `docker ps` in terminal
2. Check the config file path is correct
3. Ensure Python 3 is available: `python3 --version`
4. Verify mcp package is installed: `pip show mcp`
5. Check Claude Desktop logs for error messages
6. Restart Claude Desktop after any config changes
