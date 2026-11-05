
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


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
            "url": "http://127.0.0.1:8001/mcp",
        },
    }
}
