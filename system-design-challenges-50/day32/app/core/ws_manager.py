from fastapi import WebSocket
from typing import Dict, List, Set
import json
import asyncio
from app.core.logger import get_logger

logger = get_logger("ws_manager")

class ConnectionManager:
    def __init__(self):
        # Store active connections per document
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Store document states
        self.document_states: Dict[str, str] = {}
        # Store user information per connection
        self.connection_users: Dict[WebSocket, str] = {}
        
    async def connect(self, websocket: WebSocket, document_id: str, user_id: str) -> bool:
        """
        Connect a websocket to a document
        """
        try:
            await websocket.accept()
            
            # Add to active connections
            if document_id not in self.active_connections:
                self.active_connections[document_id] = []
            self.active_connections[document_id].append(websocket)
            
            # Store user information
            self.connection_users[websocket] = user_id
            
            logger.info(f"User {user_id} connected to document {document_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect websocket: {str(e)}")
            return False
            
    def disconnect(self, websocket: WebSocket, document_id: str) -> None:
        """
        Disconnect a websocket from a document
        """
        try:
            # Remove from active connections
            if document_id in self.active_connections:
                if websocket in self.active_connections[document_id]:
                    self.active_connections[document_id].remove(websocket)
                    
            # Remove user information
            if websocket in self.connection_users:
                user_id = self.connection_users.pop(websocket)
                logger.info(f"User {user_id} disconnected from document {document_id}")
                
        except Exception as e:
            logger.error(f"Failed to disconnect websocket: {str(e)}")
            
    async def broadcast(self, document_id: str, message: dict, exclude: WebSocket = None) -> None:
        """
        Broadcast a message to all connections for a document
        """
        if document_id in self.active_connections:
            # Create a copy of the list to avoid modification during iteration
            connections = list(self.active_connections[document_id])
            
            for connection in connections:
                if connection != exclude:
                    try:
                        await connection.send_text(json.dumps(message))
                    except Exception as e:
                        logger.error(f"Failed to send message to connection: {str(e)}")
                        # Remove dead connections
                        self.disconnect(connection, document_id)
                        
    async def send_personal_message(self, websocket: WebSocket, message: dict) -> None:
        """
        Send a message to a specific websocket
        """
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to send personal message: {str(e)}")
            
    def get_document_connections(self, document_id: str) -> List[WebSocket]:
        """
        Get all active connections for a document
        """
        return self.active_connections.get(document_id, [])
        
    def get_document_user_count(self, document_id: str) -> int:
        """
        Get the number of users connected to a document
        """
        return len(self.active_connections.get(document_id, []))
        
    def update_document_state(self, document_id: str, content: str) -> None:
        """
        Update the document state
        """
        self.document_states[document_id] = content
        
    def get_document_state(self, document_id: str) -> str:
        """
        Get the current document state
        """
        return self.document_states.get(document_id, "")

# Global connection manager instance
manager = ConnectionManager()