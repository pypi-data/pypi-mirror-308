from typing import Dict, List, Optional
import logging
from .persistent_cache import PersistentCache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)
logger = logging.getLogger(__name__)


class CacheManager:
    _prompt_details_cache = {}

    @classmethod
    def get_prompt_details(cls, cache_key: str) -> Optional[Dict]:
        """Get prompt details from cache using prompt_id and session_id"""
        return cls._prompt_details_cache.get(cache_key)

    @classmethod
    def set_prompt_details(cls, cache_key: str, prompt_details: Dict):
        """Set prompt details in cache using prompt_id and session_id"""
        cls._prompt_details_cache[cache_key] = prompt_details

    @classmethod
    def print_cache_contents(cls):
        logger.info("=== CacheManager Contents ===")
        if not cls._prompt_details_cache:
            logger.info("Cache is empty")
        else:
            for key, value in cls._prompt_details_cache.items():
                logger.info(f"Key: {key}")
                logger.info(f"Value: {value}")


class InteractionCacheManager:
    _interaction_cache = {}
    _user_messages_cache = {}

    @classmethod
    def get_interaction_history(
        cls, prompt_id: str, session_id: str, version: Optional[str] = None
    ) -> Optional[Dict]:
        """Get interaction history from cache using prompt_id and session_id"""
        cache_key = f"{prompt_id}_{session_id}"
        logger.info(f"Getting interaction history with key: {cache_key}")
        return cls._interaction_cache.get(cache_key)

    @classmethod
    def save_interaction(
        cls,
        session_id: str,
        interaction_data: Dict,
        prompt_id: str,
        version: Optional[str] = None,
    ):
        """Save interaction data to cache"""
        logger.info(f"\nSaving interaction to cache:")
        logger.info(f"Session ID: {session_id}")
        logger.info(f"Prompt ID: {prompt_id}")

        cache_key = f"{prompt_id}_{session_id}"
        logger.info(f"Cache key: {cache_key}")

        # Get existing cache
        existing_cache = cls._interaction_cache.get(cache_key, {})
        logger.info(f"Existing cache found: {bool(existing_cache)}")
        if existing_cache:
            logger.info(
                f"Previous summarized_content: {existing_cache.get('summarized_content', 'None')}"
            )

        # Update with new data
        if not existing_cache:
            existing_cache = {"messages": [], "summarized_content": None}

        existing_cache["messages"].extend(interaction_data["messages"])
        existing_cache["lastResponseAt"] = interaction_data["lastResponseAt"]
        existing_cache["memory_type"] = interaction_data["memory_type"]

        # Update summarized_content
        if interaction_data["memory_type"] == "summarizedMemory":
            existing_cache["summarized_content"] = interaction_data[
                "summarized_content"
            ]
            logger.info(
                f"Updated summarized_content: {existing_cache['summarized_content']}"
            )

        # Save to cache
        cls._interaction_cache[cache_key] = existing_cache
        logger.info("Cache updated successfully")

        # Verify save
        saved_cache = cls._interaction_cache.get(cache_key, {})
        logger.info("\nVerifying saved data:")
        logger.info(
            f"Saved summarized_content: {saved_cache.get('summarized_content', 'None')}"
        )

    @classmethod
    def print_cache_contents(cls):
        logger.info("=== Interaction Cache Contents ===")
        if not cls._interaction_cache:
            logger.info("Interaction cache is empty")
        else:
            for key, value in cls._interaction_cache.items():
                logger.info(f"Key: {key}")
                logger.info(f"Value: {value}")

        logger.info("\n=== User Messages Cache Contents ===")
        if not cls._user_messages_cache:
            logger.info("User messages cache is empty")
        else:
            for key, value in cls._user_messages_cache.items():
                logger.info(f"Key: {key}")
                logger.info(f"Value: {value}")
