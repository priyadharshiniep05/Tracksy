from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "admin": [],
            "drivers": [],
            "customers": []
        }

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)

    async def broadcast_to_room(self, room: str, message: dict):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            # Receive messages and echo back or broadcast
            data = await websocket.receive_json()
            # In a real app, we would process and broadcast based on type
            await manager.broadcast_to_room(room, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
