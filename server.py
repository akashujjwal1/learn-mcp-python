from datetime import datetime, timezone

def get_time(_args):
    return {"now": datetime.now(timezone.utc).isoformat()}

def sum_numbers(args):
    a, b = args.get("a"), args.get("b")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("a and b must be numbers")
    return {"result": a + b}

TOOLS = {
    "get_time": get_time,
    "sum_numbers": sum_numbers,
}

def invoke_tool(name, args=None):
    args = args or {}
    if name not in TOOLS:
        return {"ok": False, "error": f"Unknown tool: {name}"}
    try:
        return {"ok": True, "data": TOOLS[name](args)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    print(invoke_tool("get_time"))
    print(invoke_tool("sum_numbers", {"a": 10, "b": 5}))
    print(invoke_tool("sum_numbers", {"a": "10", "b": 5}))