import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def main():
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Get available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")

        # Connect to Furby first
        if any(t.name == "connect_furby" for t in tools):
            print("Connecting to Furby...")
            result = await client.call_tool("connect_furby")
            print(result[0])
        else:
            print("No 'connect_furby' tool found on the server.")
            return

        # Main user interaction loop
        while True:
            print("\nAvailable tools:")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")
            user_input = input("What command would you like? (or 'quit' to exit): ").strip()
            if user_input.lower() == "quit":
                break
            try:
                # For tools that require arguments, prompt for them
                if user_input == "send_named_command":
                    command = input("Enter Furby command name (e.g., fart, snore): ").strip()
                    result = await client.call_tool("send_named_command", command=command)
                elif user_input == "send_custom_command":
                    w = int(input("W: "))
                    x = int(input("X: "))
                    y = int(input("Y: "))
                    z = int(input("Z: "))
                    result = await client.call_tool("send_custom_command", w=w, x=x, y=y, z=z)
                else:
                    result = await client.call_tool(user_input)
                print("Result:", result[0] if result else "No response.")
            except Exception as e:
                print(f"Error calling tool: {e}")

if __name__ == "__main__":
    asyncio.run(main())