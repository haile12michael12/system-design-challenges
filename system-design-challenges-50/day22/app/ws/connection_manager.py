from fastapi import WebSocket
from typing import List, Dict
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Store active connections by user ID
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a websocket and associate it with a user ID"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected via WebSocket")

    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a websocket"""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"User {user_id} disconnected from WebSocket")

    async def send_personal_message(self, message: dict, user_id: int):
        """Send a message to a specific user"""
        if user_id in self.active_connections:
            # Send to all connections for this user
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected users"""
        # Flatten all connections
        all_connections = []
        for user_connections in self.active_connections.values():
            all_connections.extend(user_connections)
        
        # Send to all connections
        for connection in all_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")

    def get_user_connection_count(self, user_id: int) -> int:
        """Get the number of active connections for a user"""
        return len(self.active_connections.get(user_id, []))

    def get_total_connection_count(self) -> int:
        """Get the total number of active connections"""
        return sum(len(connections) for connections in self.active_connections.values())

# Global connection manager instance
manager = ConnectionManager()