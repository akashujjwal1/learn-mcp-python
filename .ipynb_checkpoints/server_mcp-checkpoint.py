from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("learning-mcp-server")

NOTES = {
    "today": "Learned MCP tool lifecycle: initialize -> list_tools -> call_tool.",
    "python": "Python FastMCP uses decorators like @mcp.tool and @mcp.resource.",
}

@mcp.tool()
def get_time() -> dict:
    return {"now": datetime.now(timezone.utc).isoformat()}

@mcp.tool()
def sum_numbers(a: float, b: float) -> dict:
    return {"result": a + b}

@mcp.tool()
def multiply_numbers(a: float, b: float) -> dict:
    return {"result": a * b}

@mcp.resource("notes://today")
def today_notes() -> str:
    return NOTES["today"]

@mcp.resource("notes://python")
def python_notes() -> str:
    return NOTES["python"]

@mcp.tool()
def get_note(title: str) -> dict:
    key = title.strip().lower()
    if key not in NOTES:
        raise ValueError(f"Note '{title}' not found")
    return {"title":key, "content":NOTES[key]}

if __name__ == "__main__":
    mcp.run()