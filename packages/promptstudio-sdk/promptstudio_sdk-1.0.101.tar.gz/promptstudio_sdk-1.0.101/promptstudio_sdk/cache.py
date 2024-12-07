from typing import Optional, List, Dict, Any
import os
import json
from datetime import datetime

from typing import Optional, List, Dict
from enum import Enum
from pydantic import BaseModel


class MessageType(str, Enum):
    TEXT = "text"
    FILE = "file"


class Memory(str, Enum):
    FULL_MEMORY = "fullMemory"
    WINDOW_MEMORY = "windowMemory"
    SUMMARIZED_MEMORY = "summarizedMemory"


class FileUrl(BaseModel):
    url: str


class MessageContent(BaseModel):
    type: MessageType
    text: Optional[str] = None
    file_url: Optional[FileUrl] = None


class Message(BaseModel):
    role: str
    content: List[MessageContent]


class RequestPayload(BaseModel):
    user_message: List[MessageContent]
    memory_type: Memory
    window_size: int
    session_id: str
    variables: Dict[str, str]
    version: Optional[float] = None


class AIPlatform(BaseModel):
    platform: str
    model: str
    temp: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    top_k: Optional[int] = None
    response_format: Optional[Dict[str, str]] = None


class PromptDetail(BaseModel):
    id: str
    ai_platform: AIPlatform
    version: float
    is_published: bool
    is_image_support: bool
    is_audio_support: bool


class PromptResponse(BaseModel):
    response: str


try:
    from diskcache import Cache
except ImportError as e:
    raise ImportError(
        "Could not import diskcache. Please ensure it's installed correctly with: pip install diskcache"
    ) from e


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
                role="assistant",
                content=[MessageContent(type=MessageType.TEXT, text=response)],
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
