import asyncio
from fastmcp import Client

#client = Client("mcp_server_using_fastmcp.py") # Assumes my_mcp_server.py exists
client = Client("http://localhost:8000/mcp")

async def main():
    # Connection is established here
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        if any(tool.name == "say_hello" for tool in tools):
            result = await client.call_tool("say_hello")
            print(result[0].text)

        while True:
            for tool in tools:
                print(tool.name + " : " + tool.description)
            user_input = input("What command would you like?")
            result = await client.call_tool(user_input)

    # Connection is closed automatically here
    print(f"Client connected: {client.is_connected()}")

if __name__ == "__main__":
    asyncio.run(main())