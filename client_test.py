import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def content_text(result) -> str:
    if not getattr(result, "content", None):
        return ""
    block = result.content[0]
    return getattr(block, "text", str(block))


def print_tool_result(name: str, result):
    if result.isError:
        print(f"[ERROR] {name}: {content_text(result)}")
    else:
        txt = content_text(result)
        try:
            parsed = json.loads(txt)
            print(f"[OK] {name}: {json.dumps(parsed, indent=2)}")
        except Exception:
            print(f"[OK] {name}: {txt}")


async def main():
    server = StdioServerParameters(command="python", args=["server_mcp.py"])

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("\nTools:", [t.name for t in tools.tools])

            resources = await session.list_resources()
            print("Resources:", [str(r.uri) for r in resources.resources])

            # r = await session.read_resource("notes://mcp")
            # print("Read notes://mcp:", r.contents[0].text)

            # print_tool_result("get_time", await session.call_tool("get_time", {}))
            # print_tool_result("sum_numbers", await session.call_tool("sum_numbers", {"a": 10, "b": 5}))
            # print_tool_result("get_note('python')", await session.call_tool("get_note", {"title": "python"}))
            # print_tool_result("get_note('missing')", await session.call_tool("get_note", {"title": "missing"}))

            print_tool_result("get_http_json_v2", await session.call_tool("get_http_json_v2", {"url": "http://10.255.255.1"}))

if __name__ == "__main__":
    asyncio.run(main())