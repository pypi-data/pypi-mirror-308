from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    _cache: Dict[str, Dict] = {}

    @classmethod
    def set_prompt_details(cls, prompt_id: str, details: Dict) -> None:
        """Store prompt details in cache with version info"""
        logger.info(f"Caching prompt details for {prompt_id}: {details}")
        cls._cache[prompt_id] = details

    @classmethod
    def get_prompt_details(cls, prompt_id: str) -> Optional[Dict]:
        """Get prompt details from cache"""
        details = cls._cache.get(prompt_id)
        logger.info(f"Retrieved prompt details for {prompt_id}: {details}")
        return details

    @classmethod
    def has_prompt_details(cls, prompt_id: str) -> bool:
        """Check if prompt details exist in cache"""
        return prompt_id in cls._cache


class InteractionCacheManager:
    _interaction_cache: Dict[str, Dict] = {}  # Session-based cache
    _user_messages: Dict[str, Dict] = {}  # User messages cache
    _prompt_version_messages: Dict[str, List] = {}  # Version-specific message history

    @classmethod
    def save_user_messages(cls, prompt_id: str, messages: Dict) -> None:
        """Save user messages with system message and variables"""
        logger.info(f"Saving user messages for {prompt_id}: {messages}")
        cls._user_messages[prompt_id] = messages

    @classmethod
    def get_user_messages(cls, prompt_id: str) -> Optional[Dict]:
        """Get user messages including system message"""
        messages = cls._user_messages.get(prompt_id)
        logger.info(f"Retrieved user messages for {prompt_id}: {messages}")
        return messages

    @classmethod
    def save_interaction(
        cls,
        session_id: str,
        interaction_data: Dict,
        prompt_id: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        """Save interaction with version tracking"""
        logger.info(f"Saving interaction for session {session_id}")

        # Save to session cache
        if session_id not in cls._interaction_cache:
            cls._interaction_cache[session_id] = {
                "messages": [],
                "lastResponseAt": None,
            }
        cls._interaction_cache[session_id]["messages"].extend(
            interaction_data["messages"]
        )
        cls._interaction_cache[session_id]["lastResponseAt"] = interaction_data[
            "lastResponseAt"
        ]

        # Save to version-specific cache if prompt_id and version provided
        if prompt_id and version:
            version_key = f"{prompt_id}_v{version}"
            if version_key not in cls._prompt_version_messages:
                cls._prompt_version_messages[version_key] = []
            cls._prompt_version_messages[version_key].extend(
                interaction_data["messages"]
            )
            logger.info(f"Saved to version cache {version_key}")

    @classmethod
    def get_interaction(cls, session_id: str) -> Optional[Dict]:
        """Get interaction history for a session"""
        interaction = cls._interaction_cache.get(session_id)
        logger.info(f"Retrieved interaction for session {session_id}: {interaction}")
        return interaction

    @classmethod
    def get_prompt_version_messages(cls, prompt_id: str, version: str) -> List:
        """Get message history for specific prompt version"""
        version_key = f"{prompt_id}_v{version}"
        messages = cls._prompt_version_messages.get(version_key, [])
        logger.info(
            f"Retrieved version messages for {version_key}: {len(messages)} messages"
        )
        return messages

    @classmethod
    def clear_cache(cls) -> None:
        """Clear all caches"""
        cls._interaction_cache.clear()
        cls._user_messages.clear()
        cls._prompt_version_messages.clear()
        logger.info("All caches cleared")
