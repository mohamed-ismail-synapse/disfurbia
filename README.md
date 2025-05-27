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
2. Create a virtual environment and install dependencies:
   ```powershell
   uv venv
   .venv\Scripts\activate
   uv pip install -r pyproject.toml
   ```

## Usage
Bleak is the name of the BLE library in use, so the bleak_* scripts are used to communicate with and control Furby.
- To scan for BLE devices and test Furby connection:
  ```powershell
  python bleak_scan_test.py
  ```
- To send commands and interact with Furby:
  ```powershell
  python bleak_furby_test.py
  ```

Separate from the Furby experimentation work, I was toying with this idea of making an chat bot that evaluated a user's joke and caused the Furby to react accordingly. After I realized how complicated loading custom audio via DLC onto Furby could be, I decided just to experiment with MCP client/server interactions to teach myself how it works. I made some audio recordings as placeholders to different reactions, advertised them on an mcp-server, and then used an mcp-client to play the various audio files. It worked. I'll mess with this more later.

- Check that fastmcp is running:
  ```powershell
  fastmcp version
  ```
You can run mcp_server_using_fastmcp.py through python or through fastmcp. Running via python will set up the server according to the transport method coded into the script. Running via fastmcp allows you to pick a different transport method in the command line.

- To run the MCP server through python:
  ```powershell
  python mcp_server_using_fastmcp.py
  ```
- To run the MCP server through fastmcp and set it up to be available via http://127.0.0.1:8000/mcp:
  ```powershell
  fastmcp run mcp_server_using_fastmcp.py --transport streamable-http --port 8000
  ```

- To run the MCP client, which is set up to look for an MCP server at http://localhost:8000/mcp:
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