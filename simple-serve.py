from fastmcp import FastMCP
import random
import json

# Create MCP server
mcp = FastMCP("Simple Calculator Server")

# Tool : Add two numbers
@mcp.tool
def add_num(a:int,b:int)->int:
    """ Add two numbers 
        a:first num
        b:second num
        add together
    """
    return a+b

# Tool: Random Number Generator
@mcp.tool
def random_number(min_val: int = 1, max_val: int = 100) -> int:
    """
    A random integer between min_val and max_val
    """
    return random.randint(min_val, max_val)


# Resource: Server Information
@mcp.resource("info://server")
def server_info() -> str:
    """
    Get information about this server.
    """
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A basic MCP server with math tools",
        "tools": ["random_number"],
        "author": "Your Name"
    }

    return json.dumps(info, indent=2)


# Start the server
if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )