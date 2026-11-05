
import pytest
from fastmcp import Client

from servers.math_server import mcp


@pytest.mark.asyncio
async def test_math_tools():
    async with Client(mcp) as client:

        # Test addition
        result = await client.call_tool("add", {"a": 10, "b": 20})
        assert result.data == 30

        # Test multiplication
        result = await client.call_tool("multiply", {"a": 5, "b": 4})
        assert result.data == 20

        # Test percentage
        result = await client.call_tool(
            "percentage",
            {"value": 25, "total": 100}
        )
        assert result.data == 25


@pytest.mark.asyncio
async def test_percentage_zero_total():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "percentage",
            {"value": 25, "total": 0},
            raise_on_error=False
        )

        assert result.is_error
