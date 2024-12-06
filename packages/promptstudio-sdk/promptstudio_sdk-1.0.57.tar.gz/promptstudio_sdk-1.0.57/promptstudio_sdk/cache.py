from typing import Dict, List, Optional
import logging
from .persistent_cache import PersistentCache

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

    @classmethod
    def print_cache_contents(cls) -> None:
        """Print all contents of the cache for debugging"""
        print("\n=== Cache Contents ===")
        if not cls._cache:
            print("Cache is empty")
        for key, value in cls._cache.items():
            print(f"\nKey: {key}")
            print(f"Value: {value}")


class InteractionCacheManager:
    _interaction_cache: Dict[str, Dict] = {}
    _user_messages: Dict[str, Dict] = {}
    _prompt_version_messages: Dict[str, List] = {}
    _persistent = PersistentCache()

    @classmethod
    def save_user_messages(cls, prompt_id: str, messages: Dict) -> None:
        """Save user messages with system message and variables"""
        logger.info(f"Saving user messages for prompt_id: {prompt_id}")
        logger.debug(f"Messages content: {messages}")
        cls._user_messages[prompt_id] = messages

    @classmethod
    def save_interaction(
        cls,
        session_id: str,
        interaction_data: Dict,
        prompt_id: str,
        version: str,
    ) -> None:
        """
        Save interaction with hierarchical tracking and message history
        Structure: prompt_id -> session_id -> version -> messages
        """
        logger.info(
            f"Saving interaction - Prompt ID: {prompt_id}, Session: {session_id}, Version: {version}"
        )

        # Initialize prompt_id if not exists
        if prompt_id not in cls._interaction_cache:
            cls._interaction_cache[prompt_id] = {}
            logger.debug(f"Created new prompt cache for {prompt_id}")

        # Initialize session if not exists
        if session_id not in cls._interaction_cache[prompt_id]:
            cls._interaction_cache[prompt_id][session_id] = {}
            logger.debug(f"Created new session cache for {session_id}")

        # Initialize version if not exists
        if version not in cls._interaction_cache[prompt_id][session_id]:
            cls._interaction_cache[prompt_id][session_id][version] = {
                "messages": [],
                "lastResponseAt": None,
            }
            logger.debug(f"Created new version cache for {version}")

        # Get existing messages
        existing_messages = cls._interaction_cache[prompt_id][session_id][version].get(
            "messages", []
        )

        # Add new messages to existing ones
        new_messages = interaction_data.get("messages", [])

        # Combine existing and new messages while maintaining order
        updated_messages = existing_messages + new_messages

        # Update cache with combined messages
        cls._interaction_cache[prompt_id][session_id][version].update(
            {
                "messages": updated_messages,
                "lastResponseAt": interaction_data["lastResponseAt"],
                "memory_type": interaction_data.get("memory_type", "fullMemory"),
                "window_size": interaction_data.get("window_size", 10),
            }
        )

        # Save to persistent storage
        cache_key = f"{prompt_id}_{session_id}_{version}"
        persistent_data = {
            "messages": updated_messages,
            "lastResponseAt": interaction_data["lastResponseAt"],
            "memory_type": interaction_data.get("memory_type", "fullMemory"),
            "window_size": interaction_data.get("window_size", 10),
        }
        cls._persistent.save(cache_key, persistent_data)

        logger.info(
            f"Saved interaction. Total messages in cache: " f"{len(updated_messages)}"
        )
        logger.debug(
            f"Current cache state for {prompt_id}/{session_id}/{version}: "
            f"{cls._interaction_cache[prompt_id][session_id][version]}"
        )

    @classmethod
    def get_interaction_history(
        cls, prompt_id: str, session_id: str, version: str
    ) -> Optional[Dict]:
        """Get interaction history with persistence"""
        # Try memory cache first
        history = (
            cls._interaction_cache.get(prompt_id, {}).get(session_id, {}).get(version)
        )

        # If not in memory, try persistent storage
        if not history:
            cache_key = f"{prompt_id}_{session_id}_{version}"
            history = cls._persistent.load(cache_key)
            if history:
                # Update memory cache
                if prompt_id not in cls._interaction_cache:
                    cls._interaction_cache[prompt_id] = {}
                if session_id not in cls._interaction_cache[prompt_id]:
                    cls._interaction_cache[prompt_id][session_id] = {}
                cls._interaction_cache[prompt_id][session_id][version] = history

        return history

    @classmethod
    def get_all_prompt_interactions(cls, prompt_id: str) -> Dict:
        """Get all interactions for a specific prompt across all sessions and versions"""
        interactions = cls._interaction_cache.get(prompt_id, {})
        logger.info(f"Retrieved all interactions for prompt ID: {prompt_id}")
        logger.debug(f"Interactions content: {interactions}")
        return interactions

    @classmethod
    def clear_cache(cls) -> None:
        """Clear both memory and persistent cache"""
        cls._interaction_cache.clear()
        cls._user_messages.clear()
        cls._prompt_version_messages.clear()
        cls._persistent.clear()
        logger.info("Cleared all cache (memory and persistent)")

    @classmethod
    def print_cache_contents(cls) -> None:
        """Print all contents of different caches for debugging"""
        print("\n=== Interaction Cache Contents ===")
        if not cls._interaction_cache:
            print("Interaction cache is empty")
        for prompt_id, sessions in cls._interaction_cache.items():
            print(f"\nPrompt ID: {prompt_id}")
            for session_id, versions in sessions.items():
                print(f"  Session ID: {session_id}")
                for version, data in versions.items():
                    print(f"    Version: {version}")
                    print(f"    Messages: {data['messages']}")
                    print(f"    Last Response At: {data['lastResponseAt']}")

        print("\n=== User Messages Cache Contents ===")
        if not cls._user_messages:
            print("User messages cache is empty")
        for key, value in cls._user_messages.items():
            print(f"\nPrompt ID: {key}")
            print(f"Messages: {value}")

    @classmethod
    def verify_cache_storage(
        cls, prompt_id: str, session_id: str, version: str
    ) -> Dict:
        """
        Verify cache storage for a specific prompt, session and version
        Returns a dictionary with cache verification details
        """
        verification_result = {
            "cache_exists": False,
            "message_count": 0,
            "last_message": None,
            "cache_details": None,
        }

        try:
            # Check if cache exists for this combination
            if (
                prompt_id in cls._interaction_cache
                and session_id in cls._interaction_cache[prompt_id]
                and version in cls._interaction_cache[prompt_id][session_id]
            ):

                cache_data = cls._interaction_cache[prompt_id][session_id][version]
                messages = cache_data.get("messages", [])

                verification_result.update(
                    {
                        "cache_exists": True,
                        "message_count": len(messages),
                        "last_message": messages[-1] if messages else None,
                        "cache_details": {
                            "lastResponseAt": cache_data.get("lastResponseAt"),
                            "total_interactions": len(messages)
                            // 2,  # user + assistant messages
                        },
                    }
                )

                logger.info(
                    f"Cache verification for prompt_id={prompt_id}, "
                    f"session_id={session_id}, version={version}: {verification_result}"
                )
            else:
                logger.warning(
                    f"No cache found for prompt_id={prompt_id}, "
                    f"session_id={session_id}, version={version}"
                )

        except Exception as e:
            logger.error(f"Error verifying cache: {str(e)}")
            verification_result["error"] = str(e)

        return verification_result
