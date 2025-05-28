from fastmcp import FastMCP
import json
import asyncio
from pyFurby import pyFurby
import nest_asyncio

# Apply nest_asyncio to allow running asyncio event loops inside another running loop
nest_asyncio.apply()

# Create a new MCP server
app = FastMCP(
    title="Furby Actions MCP",
    description="A server to list and interact with Furby actions.",
)

# Global Furby instance
myFurby = pyFurby()
furby_connected = False

@app.tool()
def connect_furby() -> str:
    """Connect to the nearest Furby via BLE."""
    global furby_connected
    if furby_connected:
        return "Furby already connected."
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(myFurby.connect())
    if result:
        furby_connected = True
        return f"Connected to Furby at {myFurby.address}"
    else:
        return "Failed to connect to Furby."

@app.tool()
def disconnect_furby() -> str:
    """Disconnect from the Furby."""
    global furby_connected
    if not furby_connected:
        return "Furby is not connected."
    loop = asyncio.get_event_loop()
    loop.run_until_complete(myFurby.disconnect())
    furby_connected = False
    return "Disconnected from Furby."

@app.tool()
def send_named_command(command: str) -> str:
    """Send a named command (e.g., 'fart', 'snore') to Furby."""
    if not furby_connected:
        return "Furby is not connected."
    loop = asyncio.get_event_loop()
    loop.run_until_complete(myFurby.send_named_command(command))
    return f"Sent command: {command}"

@app.tool()
def send_custom_command(w: int, x: int, y: int, z: int) -> str:
    """Send a custom 4-byte command to Furby (W,X,Y,Z)."""
    if not furby_connected:
        return "Furby is not connected."
    loop = asyncio.get_event_loop()
    loop.run_until_complete(myFurby.send_custom_command([w, x, y, z]))
    return f"Sent custom command: {[w, x, y, z]}"

# Existing action list tool

def load_action_list(path="actionlist.json"):
    """Load the Furby action list from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.tool()
def list_furby_actions() -> list:
    """List all available Furby actions and their descriptions/values."""
    return load_action_list()

if __name__ == "__main__":
    app.run()
else:
    pass
