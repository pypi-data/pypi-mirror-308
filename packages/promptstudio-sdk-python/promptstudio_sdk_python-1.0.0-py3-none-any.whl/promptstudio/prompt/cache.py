from typing import Optional, List, Dict, Any
from diskcache import Cache
import json
import os
from datetime import datetime
from ..prompt.types import Message, MessageContent


class PromptCache:
    def __init__(self, cache_dir: str = "persist-storage/responses"):
        self.cache = Cache(cache_dir)

    async def init_cache(self):
        """Initialize the cache if needed"""
        if not os.path.exists(self.cache.directory):
            os.makedirs(self.cache.directory)

    async def get_cached_response(self, session_id: str) -> Optional[List[Message]]:
        """Get cached conversation for a session"""
        await self.init_cache()
        return self.cache.get(session_id)

    async def save_to_cache(
        self, session_id: str, user_message: List[MessageContent], response: str
    ):
        """Save a message exchange to cache"""
        await self.init_cache()

        conversation = self.cache.get(session_id, [])

        # Add user message
        conversation.append(Message(role="user", content=user_message))

        # Add assistant message
        conversation.append(
            Message(
                role="assistant", content=[MessageContent(type="text", text=response)]
            )
        )

        self.cache.set(session_id, conversation)

    async def clear_cache(self):
        """Clear entire cache"""
        self.cache.clear()

    async def remove_session(self, session_id: str):
        """Remove specific session from cache"""
        self.cache.delete(session_id)

    async def save_summary_to_cache(self, session_id: str, summary: str):
        """Save conversation summary to cache"""
        summary_key = f"summary_{session_id}"
        self.cache.set(summary_key, summary)

    async def get_cached_summary(self, session_id: str) -> Optional[str]:
        """Get cached summary for a session"""
        summary_key = f"summary_{session_id}"
        return self.cache.get(summary_key)
