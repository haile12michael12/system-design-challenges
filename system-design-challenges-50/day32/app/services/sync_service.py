from typing import Dict, Any, List
from app.core.ws_manager import manager
from app.core.ot_engine import ot_engine, crdt_engine
from app.core.logger import get_logger
from app.db.crud import DocumentCRUD
from app.db.session import AsyncSessionLocal
import asyncio

logger = get_logger("sync_service")

class SyncService:
    """
    Service for handling document synchronization and merging
    """
    
    @staticmethod
    async def merge_document_changes(document_id: str, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge document changes using OT/CRDT algorithms
        """
        try:
            # Get current document state
            current_state = manager.get_document_state(document_id)
            
            # If we're using OT, transform operations
            if operations and operations[0].get("type") == "ot":
                # Transform operations against concurrent changes
                transformed_ops = []
                for op in operations:
                    transformed_op = ot_engine.transform_operation(op, [])
                    transformed_ops.append(transformed_op)
                    
                # Apply transformed operations
                new_state = current_state
                for op in transformed_ops:
                    new_state = ot_engine.apply_operation(new_state, op)
                    
                # Update document state
                manager.update_document_state(document_id, new_state)
                
                return {
                    "success": True,
                    "state": new_state,
                    "operations": transformed_ops
                }
                
            # If we're using CRDT, merge document states
            elif operations and operations[0].get("type") == "crdt":
                # Create document states from operations
                doc_states = []
                for op in operations:
                    doc_state = op.get("state", {})
                    doc_states.append(doc_state)
                    
                # Merge all document states
                merged_state = doc_states[0] if doc_states else {}
                for doc_state in doc_states[1:]:
                    merged_state = crdt_engine.merge_documents(merged_state, doc_state)
                    
                # Update document state
                manager.update_document_state(document_id, str(merged_state))
                
                return {
                    "success": True,
                    "state": str(merged_state)
                }
                
            else:
                # Simple merge - just use the latest operation
                if operations:
                    latest_op = operations[-1]
                    new_content = latest_op.get("content", current_state)
                    manager.update_document_state(document_id, new_content)
                    
                    return {
                        "success": True,
                        "state": new_content
                    }
                    
            return {
                "success": True,
                "state": current_state
            }
            
        except Exception as e:
            logger.error(f"Error merging document changes for {document_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
            
    @staticmethod
    async def broadcast_document_update(document_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Broadcast document update to all connected users
        """
        try:
            await manager.broadcast(document_id, update_data)
            return True
        except Exception as e:
            logger.error(f"Error broadcasting document update for {document_id}: {str(e)}")
            return False
            
    @staticmethod
    async def save_document_state(document_id: str) -> bool:
        """
        Save the current document state to persistent storage
        """
        try:
            # Get current state
            current_state = manager.get_document_state(document_id)
            
            # Save to database
            async with AsyncSessionLocal() as db:
                success = await DocumentCRUD.update_document(
                    db, document_id, content=current_state
                )
                return success is not None
                
        except Exception as e:
            logger.error(f"Error saving document state for {document_id}: {str(e)}")
            return False
            
    @staticmethod
    async def handle_concurrent_edits(document_id: str, user_operations: Dict[str, List[Dict[str, Any]]]) -> bool:
        """
        Handle concurrent edits from multiple users
        """
        try:
            # Merge all user operations
            all_operations = []
            for user_id, operations in user_operations.items():
                all_operations.extend(operations)
                
            # Merge the operations
            result = await SyncService.merge_document_changes(document_id, all_operations)
            
            if result["success"]:
                # Broadcast the merged state
                await SyncService.broadcast_document_update(document_id, {
                    "type": "document_update",
                    "state": result["state"]
                })
                
                # Save to persistent storage
                await SyncService.save_document_state(document_id)
                
                return True
            else:
                logger.error(f"Failed to merge document changes: {result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error handling concurrent edits for {document_id}: {str(e)}")
            return False

# Global sync service instance
sync_service = SyncService()