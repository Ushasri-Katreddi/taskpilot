
import asyncio

from langchain.mcp import MCPAdapter

from client.mcp_config import MCP_SERVERS_CONFIG


async def main():

    async with MCPAdapter(MCP_SERVERS_CONFIG) as adapter:

        # Dynamically discover tools from both MCP servers
        tools = await adapter.list_tools()

        print("\nTools discovered through MCPAdapter:")

        for tool in tools:
            print(f"- {tool.name}")

        print(f"\nTotal tools discovered: {len(tools)}")

        # Verify that both servers contributed tools
        tool_names = [tool.name for tool in tools]

        assert any(name.startswith("math_") for name in tool_names)
        assert any(name.startswith("tasks_") for name in tool_names)

        print("\nMCPAdapter connection successful!")


if __name__ == "__main__":
    asyncio.run(main())
