# Mem0 Integration for OpenHands

This module integrates [mem0](https://github.com/mem0ai/mem0) with OpenHands to provide enhanced memory capabilities for AI agents.

## Features

- Long-term memory storage for conversations
- Semantic search across past interactions
- Memory management through the OpenHands UI
- Configurable through the settings panel

## Setup

1. Enable mem0 in the OpenHands settings
2. Add your OpenAI API key in the mem0 settings tab
3. Start using OpenHands with enhanced memory capabilities

## API

The mem0 adapter provides the following methods:

- `add_event(event, user_id)`: Store an event in mem0
- `search_memories(query, user_id, limit)`: Search for memories based on a query
- `get_all_memories(user_id, limit)`: Get all memories for a user
- `delete_memory(memory_id)`: Delete a specific memory
- `delete_all_memories(user_id)`: Delete all memories for a user

## Implementation Details

The mem0 integration consists of:

1. **Mem0Adapter**: A class that interfaces with the mem0 library
2. **Memory Extensions**: Extensions to the OpenHands Memory class to support mem0
3. **API Endpoints**: Backend routes for managing mem0 memories
4. **UI Components**: Frontend components for configuring and viewing memories

## Requirements

- OpenAI API key (required for mem0 to function)
- mem0 Python package (`pip install mem0`)

## Example Usage

```python
from openhands.memory.mem0_adapter import Mem0Adapter

# Initialize the adapter
adapter = Mem0Adapter(api_key="your-openai-api-key", enabled=True)

# Store a memory
adapter.add_event(message_event, user_id="user123")

# Search for memories
results = adapter.search_memories("query", user_id="user123", limit=5)

# Get all memories
all_memories = adapter.get_all_memories(user_id="user123", limit=10)

# Delete a memory
adapter.delete_memory("memory_id")

# Clear all memories
adapter.delete_all_memories(user_id="user123")
```