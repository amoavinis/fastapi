from typing import List, Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        # Track which vehicles each connection is subscribed to
        self.subscriptions: Dict[WebSocket, List[int]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.subscriptions[websocket] = []

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]

    def subscribe_to_vehicle(self, websocket: WebSocket, vehicle_id: int):
        if websocket in self.subscriptions:
            if vehicle_id not in self.subscriptions[websocket]:
                self.subscriptions[websocket].append(vehicle_id)

    def unsubscribe_from_vehicle(self, websocket: WebSocket, vehicle_id: int):
        if websocket in self.subscriptions:
            if vehicle_id in self.subscriptions[websocket]:
                self.subscriptions[websocket].remove(vehicle_id)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            await connection.send_json(message)

    async def broadcast_vehicle_update(self, vehicle_id: int, message: dict):
        """Broadcast vehicle update only to clients subscribed to that vehicle"""
        for connection in self.active_connections:
            if vehicle_id in self.subscriptions.get(connection, []):
                await connection.send_json(message)

    async def broadcast_to_all_vehicle_subscribers(self, message: dict):
        """Broadcast to all clients that have any vehicle subscriptions"""
        for connection in self.active_connections:
            if self.subscriptions.get(connection, []):
                await connection.send_json(message)

manager = ConnectionManager()
