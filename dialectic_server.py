"""An MCP server for the dialectic process."""
from mcp.server.fastmcp import FastMCP

import dialectic

mcp = FastMCP("Dialectic", dependencies=["aiohttp"])

@mcp.tool()
async def dialectic_tool(topic: str) -> str:
    """Perform a dialectic on a topic"""

    synthesis = await dialectic.dialectic(topic)
    return synthesis

# @mcp.prompt()
def dialectic_prompt(topic: str) -> str:
    """Create an dialectic prompt"""
    return f"Please perform a dialectic on this topc: {topic}"
