import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server = StdioServerParameters(
        command="python",
        args=["server_mcp.py"],
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            r1 = await session.call_tool("get_time", {})
            print("get_time:", r1)

            r2 = await session.call_tool("sum_numbers", {"a": 10, "b": 3})
            print("sum_numbers:", r2)

            r3 = await session.call_tool("multiply_numbers", {"a": 6, "b": 7})
            print("multiply_numbers:", r3)

            resources = await session.list_resources()
            print("Resources:", [r.uri for r in resources.resources])

            r1 = await session.read_resource("notes://today")
            print("read notes://today:", r1)

            r2 = await session.read_resource("notes://python")
            print("read notes://python:", r2)

            r3 = await session.call_tool("get_note", {"title": "python"})
            print("get_note('python'):", r3)

            r4 = await session.call_tool("get_note", {"title": "missing"})
            print("get_note('missing'):", r4)


if __name__ == "__main__":
    asyncio.run(main())