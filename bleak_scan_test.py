import asyncio
from bleak import BleakScanner, BleakClient

async def scan_and_connect():
    print("🔍 Scanning for BLE devices (5 seconds)...")
    try:
        devices = await BleakScanner.discover(timeout=5.0)
    except Exception as e:
        print(f"⚠️ Scan failed: {e}")
        return

    furby = None
    for d in devices:
        print(f"Found: {d.name} @ {d.address}")
        if d.name and "Furby" in d.name:
            furby = d
            break

    if not furby:
        print("❌ No device named 'Furby' found.")
        return

    print(f"✅ Found Furby: {furby.name} @ {furby.address}")

    client = BleakClient(furby.address)
    try:
        await client.connect(timeout=10.0)
        if not client.is_connected:
            print("❌ Failed to connect to Furby.")
            return
        print("🔌 Connected to Furby. Discovering services...")

        for service in client.services:
            print(f"🧱 Service: {service.uuid}")
            for char in service.characteristics:
                props = ', '.join(char.properties)
                print(f"  🔹 Char: {char.uuid} ({props})")

    except Exception as e:
        print(f"⚠️ Error during connection or discovery: {e}")
    finally:
        if client.is_connected:
            print("🔌 Disconnecting from Furby...")
            await client.disconnect()
            print("✅ Disconnected.")

if __name__ == "__main__":
    try:
        asyncio.run(scan_and_connect())
    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user.")
