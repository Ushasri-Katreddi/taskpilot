
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TASKS_SERVER_URL = "http://127.0.0.1:8001/mcp"


MCP_SERVERS_CONFIG = {
    "mcpServers": {
        "math": {
            "command": sys.executable,
            "args": [
                "-m",
                "servers.math_server",
            ],
            "cwd": str(PROJECT_ROOT),
        },
        "tasks": {
            "url": TASKS_SERVER_URL,
        },
    }
}
