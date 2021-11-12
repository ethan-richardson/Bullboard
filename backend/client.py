import asyncio
import websockets

connected = set()

async def server(websocket, path):
    # Add connected client to set
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                await conn.send(f'THIS IS A TEST SOCKET MESSAGE: {message}')
    finally:
        # Remove the connected client
        connected.remove(websocket)