from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.ws_manager import manager
from app.core.ot_engine import ot_engine, crdt_engine
from app.core.logger import get_logger
from typing import Dict, Any
import json

router = APIRouter(prefix="/ws", tags=["websocket"])

logger = get_logger("ws.editor")

@router.websocket("/editor/{document_id}")
async def websocket_endpoint(websocket: WebSocket, document_id: str, user_id: str):
    """
    WebSocket endpoint for collaborative document editing
    """
    # Connect the websocket
    connected = await manager.connect(websocket, document_id, user_id)
    if not connected:
        await websocket.close()
        return
        
    try:
        # Send current document state to the new user
        current_state = manager.get_document_state(document_id)
        if current_state:
            await manager.send_personal_message(websocket, {
                "type": "document_state",
                "content": current_state
            })
        
        # Notify other users about the new user
        await manager.broadcast(document_id, {
            "type": "user_joined",
            "user_id": user_id,
            "user_count": manager.get_document_user_count(document_id)
        }, exclude=websocket)
        
        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "operation":
                # Handle document operation (OT/CRDT)
                operation = message["operation"]
                
                # Transform operation if needed (OT)
                # In a real implementation, this would be more complex
                transformed_operation = ot_engine.transform_operation(operation, [])
                
                # Apply operation to document state
                current_state = manager.get_document_state(document_id)
                new_state = ot_engine.apply_operation(current_state, transformed_operation)
                manager.update_document_state(document_id, new_state)
                
                # Broadcast operation to other users
                await manager.broadcast(document_id, {
                    "type": "operation",
                    "operation": transformed_operation,
                    "user_id": user_id
                }, exclude=websocket)
                
            elif message["type"] == "cursor":
                # Handle cursor position update
                await manager.broadcast(document_id, {
                    "type": "cursor",
                    "user_id": user_id,
                    "position": message["position"]
                }, exclude=websocket)
                
            elif message["type"] == "selection":
                # Handle selection update
                await manager.broadcast(document_id, {
                    "type": "selection",
                    "user_id": user_id,
                    "range": message["range"]
                }, exclude=websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, document_id)
        await manager.broadcast(document_id, {
            "type": "user_left",
            "user_id": user_id,
            "user_count": manager.get_document_user_count(document_id)
        })
        logger.info(f"User {user_id} disconnected from document {document_id}")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {str(e)}")
        manager.disconnect(websocket, document_id)