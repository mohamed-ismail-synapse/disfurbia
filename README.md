# disfurbia
A hardware engineer's attempt at forcing an LLM-based chat bot to only speak through a Furby.

## Features
- Connects to a Furby via Bluetooth Low Energy (BLE)
- Uses an LLM-based chatbot interface to generate responses (todo)
- Furby speaks responses using existing audio & actions
- Modular MCP server/client architecture for extensibility (todo)
- Joke rating and response system (todo)

## Requirements
- Python 3.8+
- Windows OS (tested)
- Bluetooth Low Energy (BLE) adapter
- Furby device (with BLE support)

## Installation & Setup
1. Install uv (recommended for fast, reliable Python package management):
2. Install dependencies:
   ```powershell
   uv pip install -r pyproject.toml
   ```

## Usage
- To scan for BLE devices and test Furby connection:
  ```powershell
  python bleak_scan_test.py
  ```
- To send commands and interact with Furby:
  ```powershell
  python bleak_furby_test.py
  ```
- To run the MCP server (for LLM/chatbot integration):
  ```powershell
  python mcp_server_using_fastmcp.py
  ```
- To run the MCP client:
  ```powershell
  python mcp_client_using_fastmcp.py
  ```

## Development
- Audio files for responses are in the `audio/` directory.
- MCP server and client use the `fastmcp` library for communication.
- BLE communication is handled via the `bleak` library.
- Modify or add new tools in `mcp_server_using_fastmcp.py`.
- For custom Furby BLE commands, edit `bleak_furby_test.py`.

## Future Work
- Integrate real-time LLM chatbot (e.g., OpenAI, local models)
- Add support for BLE characteristics
- Improve error handling and user feedback
- Cross-platform support (Linux, macOS)

## Acknowledgements
I stand on the shoulders of giants. Or giant nerds. Big thank yous to the following:
- [cluesang's work on controlling a Bittle robot using MCP](https://github.com/cluesang/pyBittle-mcp-server)
- [pdjstone's work on controlling a Furby from a Chrome-based web app](https://github.com/pdjstone/furby-web-bluetooth)
- [Jeija's work on reverse-engineering the Furby BLE interface](https://github.com/Jeija/bluefluff)