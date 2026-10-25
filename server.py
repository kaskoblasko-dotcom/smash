import asyncio
import os
import websockets

clients = set()
PORT = int(os.environ.get("PORT", 8765))

async def handler(ws):
    if len(clients) >= 2:
        await ws.send('{"error": "room full"}')
        await ws.close()
        return
    clients.add(ws)
    try:
        async for msg in ws:
            # pass every message to the other player
            for other in list(clients):
                if other is not ws:
                    await other.send(msg)
    finally:
        clients.discard(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Smash server running on port {PORT}")
        await asyncio.Future()  # run forever

asyncio.run(main())
