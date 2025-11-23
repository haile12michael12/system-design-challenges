from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.orchestrator.state import RegionState
import asyncio
import json

router = APIRouter()
region_state = RegionState()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/regions")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive any message from client (optional)
            data = await websocket.receive_text()
            
            # Send current region status
            regions = region_state.get_all_regions()
            await manager.send_personal_message(json.dumps(regions), websocket)
            
            # Wait before sending next update
            await asyncio.sleep(5)  # Update every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        print(f"WebSocket error: {e}")