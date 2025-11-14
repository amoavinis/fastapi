from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import json

from ..db.database import get_db
from ..utils.websocket import manager
from .. import models

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time vehicle updates.

    Clients can send messages to subscribe/unsubscribe to specific vehicles:
    - {"action": "subscribe", "vehicle_id": 1}
    - {"action": "unsubscribe", "vehicle_id": 1}
    - {"action": "subscribe_all"}
    """
    await manager.connect(websocket)
    try:
        # Send connection success message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to vehicle tracking WebSocket"
        })

        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                action = message.get("action")

                if action == "subscribe" and "vehicle_id" in message:
                    vehicle_id = message["vehicle_id"]
                    manager.subscribe_to_vehicle(websocket, vehicle_id)
                    await websocket.send_json({
                        "type": "subscription",
                        "message": f"Subscribed to vehicle {vehicle_id}"
                    })

                elif action == "unsubscribe" and "vehicle_id" in message:
                    vehicle_id = message["vehicle_id"]
                    manager.unsubscribe_from_vehicle(websocket, vehicle_id)
                    await websocket.send_json({
                        "type": "subscription",
                        "message": f"Unsubscribed from vehicle {vehicle_id}"
                    })

                elif action == "subscribe_all":
                    # Client wants updates for all vehicles (broadcast mode)
                    await websocket.send_json({
                        "type": "subscription",
                        "message": "Subscribed to all vehicle updates"
                    })

                elif action == "ping":
                    # Simple ping/pong for keepalive
                    await websocket.send_json({
                        "type": "pong"
                    })

            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
