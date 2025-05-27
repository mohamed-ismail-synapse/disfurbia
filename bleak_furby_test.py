import asyncio
import time
from bleak import BleakScanner, BleakClient

RX_CHAR_UUID = "dab91382-b5a1-e29c-b041-bcd562613bde"
TX_CHAR_UUID = "dab91383-b5a1-e29c-b041-bcd562613bde"

FURBY_COMMANDS = {
    "fart":   bytes([0x13, 0x00, 0x01, 0x02, 0x01, 0x04]),
    "snore":  bytes([0x13, 0x00, 0x4a, 0x00, 0x00, 0x01]),
    "toot":   bytes([0x13, 0x00, 0x07, 0x00, 0x01, 0x02]),
    "laugh":  bytes([0x13, 0x00, 0x02, 0x00, 0x00, 0x00]),
}

last_command_time = 0.0

KEEP_ALIVE_CMD = bytes([0x20, 0x06])
KEEP_ALIVE_RESP_PREFIX = b'\x22'

# List of (future, prefix) pairs for response matching
pending_responses = []

def notification_handler(sender, data):
    print(f"📩 Notification from {sender}: {data.hex()}")
    # Check all pending futures for a matching prefix
    for fut, prefix in pending_responses[:]:
        if prefix is None or data.startswith(prefix):
            if not fut.done():
                fut.set_result(data)
            pending_responses.remove((fut, prefix))

async def send_command(client, tx_uuid, data, response_prefix=None, timeout=2.0):
    fut = asyncio.get_event_loop().create_future()
    if response_prefix is not None:
        pending_responses.append((fut, response_prefix))
    await client.write_gatt_char(tx_uuid, data)
    global last_command_time
    last_command_time = time.time()
    if response_prefix is not None:
        try:
            resp = await asyncio.wait_for(fut, timeout)
            return resp
        except asyncio.TimeoutError:
            pending_responses.remove((fut, response_prefix))
            print("⚠️ Command response timed out.")
            return None

async def keep_alive_task(client, tx_uuid):
    try:
        while True:
            global last_command_time
            if (time.time() - last_command_time) > 3.0:
                print("👁️ Sending keep-alive...")
                resp = await send_command(client, tx_uuid, KEEP_ALIVE_CMD, KEEP_ALIVE_RESP_PREFIX)
                if resp:
                    print("✅ Keep-alive response received!")
                else:
                    print("⚠️ No keep-alive response!")
                await asyncio.sleep(1.0)
            else:
                await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        pass

async def main():
    print("🔍 Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=5.0)
    furby = next((d for d in devices if d.name and "Furby" in d.name), None)
    if not furby:
        print("❌ No device named 'Furby' found.")
        return

    print(f"✅ Found Furby @ {furby.address}")
    client = BleakClient(furby.address)

    try:
        await client.connect(timeout=10.0)
        if not client.is_connected:
            print("❌ Failed to connect.")
            return

        print("🔌 Connected to Furby!")

        await client.start_notify(RX_CHAR_UUID, notification_handler)

        # Start keep-alive task
        keep_alive = asyncio.create_task(keep_alive_task(client, TX_CHAR_UUID))
        print("👁️ Keep-alive started. Furby is focused.")

        # Command loop
        while True:
            cmd = await asyncio.get_event_loop().run_in_executor(
                None, input, "\n🧠 Enter a command (fart, snore, toot, laugh), 'quit', or 'W,X,Y,Z': "
            )
            cmd = cmd.strip().lower()
            if cmd == "quit":
                print("👋 Exiting...")
                break
            elif cmd in FURBY_COMMANDS:
                print(f"➡️ Sending command: {cmd}")
                await send_command(client, TX_CHAR_UUID, FURBY_COMMANDS[cmd], None)
                print(f"✅ Sent command: {cmd}")
            else:
                # Try to parse as W,X,Y,Z
                try:
                    nums = [int(x) for x in cmd.split(",")]
                    if len(nums) == 4 and all(0 <= n <= 255 for n in nums):
                        data = bytes([0x13, 0x00] + nums)
                        print(f"➡️ Sending custom command: {data.hex()}")
                        await send_command(client, TX_CHAR_UUID, data, None)
                        print("✅ Sent custom command.")
                    else:
                        print("❌ Enter four numbers between 0 and 255, separated by commas.")
                except Exception:
                    print("❌ Unknown command or invalid format.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        print("🧹 Cleaning up...")
        if 'keep_alive' in locals():
            keep_alive.cancel()
            await keep_alive
        if client.is_connected:
            await client.stop_notify(RX_CHAR_UUID)
            await client.disconnect()
            print("✅ Disconnected from Furby.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user.")
