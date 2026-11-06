
from fastmcp import FastMCP

# Initialize the Math MCP server
mcp = FastMCP(
    name="Math MCP Server",
    instructions="Provides mathematical operations such as addition, multiplication, and percentage calculation."
)


@mcp.tool()
def add(a: float, b: float) -> float:
    """
    Add two numbers and return their sum.

    Args:
        a: First number.
        b: Second number.
    """
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers and return their product.

    Args:
        a: First number.
        b: Second number.
    """
    return a * b


@mcp.tool()
def percentage(value: float, total: float) -> float:
    """
    Calculate what percentage a value represents out of a total.

    Formula: (value / total) * 100.

    Example:
    value=25, total=200 returns 12.5.

    This tool does NOT calculate X percent of Y.
    """
    if total == 0:
        raise ValueError("Cannot calculate percentage: total cannot be zero.")

    return (value / total) * 100


if __name__ == "__main__":
    mcp.run(transport="stdio")
