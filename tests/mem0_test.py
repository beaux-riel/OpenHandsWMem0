"""
Test file for mem0 integration with OpenHands.
This is a sample test file that demonstrates how to use mem0 with OpenHands.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from openhands.memory.mem0_adapter import Mem0Adapter
from openhands.events.event import Event
from openhands.events.action.message import MessageAction


class TestMem0Adapter(unittest.TestCase):
    """Test the Mem0Adapter class."""

    def setUp(self):
        """Set up the test environment."""
        # Use a placeholder API key for testing
        self.api_key = "sk-test-placeholder-api-key"
        
        # Create a mock Memory instance
        self.mock_memory = MagicMock()
        
        # Patch the Memory class
        self.memory_patcher = patch('openhands.memory.mem0_adapter.Memory', 
                                   return_value=self.mock_memory)
        self.mock_memory_class = self.memory_patcher.start()
        
        # Initialize the adapter with the mock
        self.adapter = Mem0Adapter(api_key=self.api_key, enabled=True)
        
    def tearDown(self):
        """Clean up after the test."""
        self.memory_patcher.stop()
        
    def test_initialization(self):
        """Test that the adapter initializes correctly."""
        self.assertTrue(self.adapter.enabled)
        self.assertEqual(self.adapter.api_key, self.api_key)
        
    def test_add_event_message(self):
        """Test adding a message event to mem0."""
        # Create a message event
        message_event = MessageAction(content="Test message")
        
        # Add the event
        self.adapter.add_event(message_event, user_id="test_user")
        
        # Verify the memory.add method was called with the right parameters
        self.mock_memory.add.assert_called_once_with("Test message", user_id="test_user")
        
    def test_search_memories(self):
        """Test searching for memories."""
        # Set up the mock to return a specific result
        self.mock_memory.search.return_value = {
            "results": [
                {"id": "1", "text": "Test memory", "created_at": "2023-01-01T00:00:00Z"}
            ]
        }
        
        # Search for memories
        results = self.adapter.search_memories("test", user_id="test_user", limit=5)
        
        # Verify the search method was called with the right parameters
        self.mock_memory.search.assert_called_once_with(
            query="test", user_id="test_user", limit=5
        )
        
        # Verify the results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "Test memory")
        
    def test_get_all_memories(self):
        """Test getting all memories."""
        # Set up the mock to return specific results
        self.mock_memory.get_all.return_value = {
            "results": [
                {"id": "1", "text": "Memory 1", "created_at": "2023-01-01T00:00:00Z"},
                {"id": "2", "text": "Memory 2", "created_at": "2023-01-02T00:00:00Z"}
            ]
        }
        
        # Get all memories
        results = self.adapter.get_all_memories(user_id="test_user", limit=10)
        
        # Verify the get_all method was called with the right parameters
        self.mock_memory.get_all.assert_called_once_with(
            user_id="test_user", limit=10
        )
        
        # Verify the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["text"], "Memory 1")
        self.assertEqual(results[1]["text"], "Memory 2")
        
    def test_delete_memory(self):
        """Test deleting a memory."""
        # Delete a memory
        self.adapter.delete_memory("memory_id")
        
        # Verify the delete method was called with the right parameters
        self.mock_memory.delete.assert_called_once_with("memory_id")
        
    def test_delete_all_memories(self):
        """Test deleting all memories for a user."""
        # Delete all memories
        self.adapter.delete_all_memories(user_id="test_user")
        
        # Verify the delete_all method was called with the right parameters
        self.mock_memory.delete_all.assert_called_once_with(user_id="test_user")


if __name__ == "__main__":
    unittest.main()