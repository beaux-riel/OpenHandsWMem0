"""Mem0 memory adapter for OpenHands."""

import datetime
import json
import uuid
from typing import Any, Dict, List, Optional

try:
    from mem0 import Memory
    MEM0_AVAILABLE = True
except ImportError:
    MEM0_AVAILABLE = False

from openhands.core.logger import openhands_logger as logger
from openhands.events.event import Event
from openhands.events.action.message import MessageAction


class Mem0Adapter:
    """Adapter for Mem0 memory service."""

    def __init__(self, api_key: Optional[str] = None, enabled: bool = True):
        """Initialize the Mem0 adapter.
        
        Args:
            api_key: The OpenAI API key to use for Mem0.
            enabled: Whether Mem0 is enabled.
        """
        self.api_key = api_key
        self.enabled = enabled and api_key is not None and len(api_key) > 0
        
        if not MEM0_AVAILABLE:
            logger.warning("mem0 package is not installed. Please install it with 'pip install mem0'")
            self.enabled = False
            return
            
        if not self.enabled:
            logger.info("Mem0 memory adapter is disabled")
            return
            
        try:
            # Initialize mem0 memory
            import os
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
            self.memory = Memory()
            logger.info("Mem0 memory adapter initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize mem0 memory adapter: {str(e)}")
            self.enabled = False
            
    def add_event(self, event: Event, user_id: str) -> None:
        """Add an event to mem0 memory.
        
        Args:
            event: The OpenHands event to store
            user_id: The user ID to associate with this memory
        """
        if not self.enabled:
            return
            
        try:
            # Convert event to a format suitable for mem0
            if isinstance(event, MessageAction):
                # For message actions, store the content directly
                self.memory.add(event.content, user_id=user_id)
            else:
                # For other events, store a serialized version
                event_data = {
                    "event_type": event.__class__.__name__,
                    "content": getattr(event, "content", str(event)),
                    "timestamp": getattr(event, "timestamp", None)
                }
                self.memory.add(json.dumps(event_data), user_id=user_id)
                
            logger.debug(f"Added event to mem0 memory for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to add event to mem0 memory: {str(e)}")
            
    def search_memories(self, query: str, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant memories based on a query.
        
        Args:
            query: The search query
            user_id: The user ID to search memories for
            limit: Maximum number of memories to return
            
        Returns:
            A list of memory entries
        """
        if not self.enabled:
            return []
            
        try:
            results = self.memory.search(query=query, user_id=user_id, limit=limit)
            return results.get("results", [])
        except Exception as e:
            logger.error(f"Failed to search mem0 memories: {str(e)}")
            return []
            
    def get_all_memories(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all memories for a user.
        
        Args:
            user_id: The user ID to get memories for
            limit: Maximum number of memories to return
            
        Returns:
            A list of memory entries
        """
        if not self.enabled:
            return []
            
        try:
            results = self.memory.get_all(user_id=user_id, limit=limit)
            return results.get("results", [])
        except Exception as e:
            logger.error(f"Failed to get all mem0 memories: {str(e)}")
            return []
            
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a specific memory by ID.
        
        Args:
            memory_id: The ID of the memory to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
            
        try:
            self.memory.delete(memory_id)
            return True
        except Exception as e:
            logger.error(f"Failed to delete mem0 memory: {str(e)}")
            return False
            
    def delete_all_memories(self, user_id: str) -> bool:
        """Delete all memories for a user.
        
        Args:
            user_id: The user ID to delete memories for
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
            
        try:
            self.memory.delete_all(user_id=user_id)
            return True
        except Exception as e:
            logger.error(f"Failed to delete all mem0 memories: {str(e)}")
            return False