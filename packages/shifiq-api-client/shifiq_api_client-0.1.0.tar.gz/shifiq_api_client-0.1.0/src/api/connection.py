import websockets
import asyncio
import json
from typing import Callable, Dict

class PlayerWebSocketHandler:
    def __init__(self, ws_url: str, player_id: str, api_key: str):
        self.ws_url = f"{ws_url}/players/{player_id}/ws"
        self.api_key = api_key
        self.handlers: Dict[str, Callable] = {}
        self.running = False
        
    def register_handler(self, command: str, handler: Callable):
        """Register a handler function for a specific command"""
        self.handlers[command] = handler

    async def _handle_message(self, message: str):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            command = data.get('command')
            if command in self.handlers:
                await self.handlers[command](data)
            else:
                print(f"Unhandled command received: {command}")
        except json.JSONDecodeError:
            print(f"Invalid message format received: {message}")

    async def connect(self):
        """Establish WebSocket connection and handle messages"""
        self.running = True
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        while self.running:
            try:
                async with websockets.connect(self.ws_url, extra_headers=headers) as websocket:
                    while self.running:
                        message = await websocket.recv()
                        await self._handle_message(message)
            except websockets.exceptions.ConnectionClosed:
                print("Connection lost, attempting to reconnect...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error in WebSocket connection: {e}")
                await asyncio.sleep(5)

    def stop(self):
        """Stop the WebSocket connection"""
        self.running = False 