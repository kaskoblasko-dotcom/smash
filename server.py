import asyncio
import websockets

clients = set()

async def handler(ws):
    if len(clients) >= 2:
        await ws.send('{"error": "room full"}')
        await ws.close()
        return
    clients.add(ws)
    try:
        async for msg in ws:
            # pass every message to the other player
            for other in clients:
                if other is not ws:
                    await other.send(msg)
    finally:
        clients.discard(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Smash server running on port 8765")
        await asyncio.Future()  # run forever

asyncio.run(main())