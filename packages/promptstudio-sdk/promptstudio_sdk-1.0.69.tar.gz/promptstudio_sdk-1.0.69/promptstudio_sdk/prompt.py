from typing import Dict, Any, List, Union, Optional

import requests
import logging
import uuid
import json
from datetime import datetime
from .base import Base
from .cache import CacheManager, InteractionCacheManager
import os
import hashlib
import tempfile
from pathlib import Path
import mimetypes


from openai import OpenAI
import openai

import anthropic
import google.generativeai as genai
from google.ai import generativelanguage as glm
from google.generativeai import types as generation_types

from google.ai.generativelanguage_v1beta.types import content


# import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class PromptManager(Base):
    async def get_all_prompts(self, folder_id: str) -> Dict:
        """
        Get all prompts for a given folder

        Args:
            folder_id: ID of the folder

        Returns:
            Dictionary containing prompt versions
        """
        logger.info(f"Fetching all prompts for folder: {folder_id}")
        response = await self._request(f"/{folder_id}")
        logger.info(f"Successfully retrieved prompts for folder: {folder_id}")
        return response

    async def windowmemory_save_log_ai_interaction_prompt(
        self,
        user_id: str,
        user_prompt_id: str,
        user_prompt: dict,
        interaction_request: Dict,
    ) -> Dict:
        """Process and save AI interaction using window memory cache"""
        try:
            logger.info(f"Processing AI interaction for user_id: {user_id}")
            logger.info(f"User prompt details: {user_prompt}")
            logger.info(f"Interaction request: {interaction_request}")

            # Generate session_id if not present
            session_id = interaction_request.get("session_id") or str(uuid.uuid4())
            logger.info(f"Using session_id: {session_id}")

            # Print initial cache state
            logger.info("Initial cache state:")
            CacheManager.print_cache_contents()
            InteractionCacheManager.print_cache_contents()

            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")
            logger.info(f"Version: {version}")
            if not version:
                logger.info(f"Fetching latest version for prompt_id: {user_prompt_id}")
                latest_version_response = await self._request(
                    f"/fetch/prompt/latest_version/{user_prompt_id}"
                )
                version = str(latest_version_response["data"]["latest_version"])
            logger.info(f"Using version: {version}")

            # First fetch and cache prompt details
            cache_key = f"{user_prompt_id}_{session_id}_v{version}"
            prompt_details = CacheManager.get_prompt_details(cache_key)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, version
                )
            logger.info(f"Cached new prompt details for {cache_key}")

            # Get interaction history
            interaction_history = InteractionCacheManager.get_interaction_history(
                user_prompt_id, session_id, version
            )
            logger.info(f"Retrieved interaction history: {interaction_history}")

            # Build message collection with window memory
            prompt_collection_msg = []
            window_size = interaction_request.get("window_size", 10)

            # Add system message if platform is OpenAI
            if user_prompt["platform"] == "openai":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": [
                            {"type": "text", "text": prompt_details["system_prompt"]}
                        ],
                    }
                )

            # Add previous messages within window size
            if interaction_history and interaction_history.get("messages"):
                # Get last N messages based on window size
                messages = interaction_history["messages"]
                start_idx = max(
                    0, len(messages) - (window_size * 2)
                )  # *2 for pairs of messages
                window_messages = messages[start_idx:]
                prompt_collection_msg.extend(window_messages)
                logger.info(f"Added {len(window_messages)} messages from window")

            # Add new user message
            prompt_collection_msg.append(
                {
                    "role": "user",
                    "content": interaction_request["user_message"],
                }
            )

            # Make AI platform request
            platform_name = prompt_details["ai_platform"]
            response = await self._make_ai_platform_request(
                platform_name=platform_name,
                prompt_details={
                    **prompt_details,
                    "response_format": prompt_details.get(
                        "response_format", {"type": "text"}
                    ),
                },
                messages=prompt_collection_msg,
                system_message=prompt_details["system_prompt"],
            )
            logger.info(f"Response from AI platform: {response}")

            assistant_reply = response["response"]
            logger.info(f"Assistant reply: {assistant_reply}")

            # Create new messages to save
            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": [{"type": "text", "text": f"{assistant_reply}"}],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Save to cache with window memory configuration
            InteractionCacheManager.save_interaction(
                session_id=session_id,
                interaction_data={
                    "messages": new_messages,
                    "lastResponseAt": current_time,
                    "memory_type": "windowMemory",
                    "window_size": window_size,
                },
                prompt_id=user_prompt_id,
                version=version,
            )

            # Print final cache state
            logger.info("Final cache state after interaction:")
            CacheManager.print_cache_contents()
            InteractionCacheManager.print_cache_contents()

            return {
                "message": "AI interaction saved successfully for memory type: window memory",
                "user_prompt_id": user_prompt_id,
                "response": assistant_reply,
                "session_id": session_id,
            }

        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    async def fullmemory_save_log_ai_interaction_prompt(
        self,
        user_id: str,
        user_prompt_id: str,
        user_prompt: dict,
        interaction_request: Dict,
    ) -> Dict:
        """Process and save AI interaction using cache memory"""
        try:
            logger.info(f"Processing AI interaction for user_id: {user_id}")
            logger.info(f"User prompt details: {user_prompt}")
            logger.info(f"Interaction request: {interaction_request}")

            # Generate session_id if not present
            session_id = interaction_request.get("session_id") or str(uuid.uuid4())
            logger.info(f"Using session_id: {session_id}")

            # Print initial cache state
            logger.info("Initial cache state:")
            CacheManager.print_cache_contents()
            InteractionCacheManager.print_cache_contents()

            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")
            logger.info(f"Version: {version}")
            # if not version:
            #     logger.info(f"Fetching latest version for prompt_id: {user_prompt_id}")
            #     latest_version_response = await self._request(
            #         f"/fetch/prompt/latest_version/{user_prompt_id}"
            #     )
            #     version = str(latest_version_response["data"]["latest_version"])
            # logger.info(f"Using version: {version}")

            # First fetch and cache prompt details
            cache_key = f"{user_prompt_id}_{session_id}_v{version}"
            prompt_details = CacheManager.get_prompt_details(cache_key)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, session_id, version
                )
                logger.info(f"Cached new prompt details for {cache_key}")

            # Get interaction history
            interaction_history = InteractionCacheManager.get_interaction_history(
                user_prompt_id, session_id, version
            )
            logger.info(f"Retrieved interaction history: {interaction_history}")

            # Build message collection
            prompt_collection_msg = []

            # Add system message if platform is OpenAI
            if user_prompt["platform"] == "openai":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": [
                            {"type": "text", "text": prompt_details["system_prompt"]}
                        ],
                    }
                )

                # Add previous messages
            if interaction_history and interaction_history.get("messages"):
                prompt_collection_msg.extend(interaction_history["messages"])
                logger.info(
                    f"Added {len(interaction_history['messages'])} previous messages"
                )
            # prompt_collection_msg.extend(interaction_history["messages"])

            logger.info(
                f"Prompt collection message111111111: {interaction_request["user_message"]}"
            )

            # Add previous messages from history
            if interaction_history and interaction_history.get("messages"):
                prompt_collection_msg.extend(interaction_history["messages"])
                logger.info(
                    f"Added {len(interaction_history['messages'])} previous messages"
                )

            # Add new user message
            prompt_collection_msg.append(
                {
                    "role": "user",
                    "content": interaction_request["user_message"],
                }
            )

            # Make AI platform request
            platform_name = prompt_details["ai_platform"]
            response = await self._make_ai_platform_request(
                platform_name=platform_name,
                prompt_details={
                    **prompt_details,
                    "response_format": prompt_details.get(
                        "response_format", {"type": "text"}
                    ),
                },
                messages=prompt_collection_msg,
                system_message=prompt_details["system_prompt"],
            )
            logger.info(f"Response from AI platform qqqqqqqqqqqqq: {response}")

            assistant_reply = response["response"]
            logger.info(f"Assistant reply qqqqqqqqqqqqq: {assistant_reply}")

            logger.info(
                f"Prompt collection message333333333: {interaction_request["user_message"]}"
            )

            # Create new messages to save
            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": [{"type": "text", "text": f"{assistant_reply}"}],
                    "env": interaction_request.get("env", "test"),
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Save to cache with all required information
            InteractionCacheManager.save_interaction(
                session_id=session_id,
                interaction_data={
                    "messages": new_messages,
                    "lastResponseAt": current_time,
                    "memory_type": interaction_request.get("memory_type", "fullMemory"),
                    "window_size": interaction_request.get("window_size", 10),
                },
                prompt_id=user_prompt_id,
                version=version,
            )

            # Print final cache state
            logger.info("Final cache state after interaction:")
            CacheManager.print_cache_contents()
            InteractionCacheManager.print_cache_contents()

            return {
                "message": "AI interaction saved successfully for memory type: full memory",
                "user_prompt_id": user_prompt_id,
                "response": assistant_reply,
                "session_id": session_id,
            }

        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    async def _fetch_and_cache_prompt_details(
        self, prompt_id: str, session_id: str, version: Optional[str] = None
    ) -> Dict:
        """
        Fetch prompt details from PromptStudio

        Args:
            prompt_id: ID of the prompt
            session_id: Session ID
            version: Optional version number (if None, will use null in request)

        Returns:
            Dictionary containing prompt details
        """
        try:
            # Clean the prompt_id
            prompt_id = prompt_id.strip()

            # Prepare request body with proper version format
            request_body = {"version": int(float(version)) if version else None}

            logger.info(
                f"Fetching prompt details for prompt_id: {prompt_id}, version: {version}"
            )
            logger.info(f"Request body: {request_body}")

            # Make request to version_data endpoint
            response = await self._request(
                f"/fetch/prompt/version_data/{prompt_id}",
                method="POST",
                json=request_body,
            )

            logger.info(f"Response from version_data endpoint: {response}")

            if not response.get("data") or not response["data"].get("result"):
                logger.error(f"Invalid response format for prompt_id: {prompt_id}")
                raise ValueError("Invalid response format from API")

            # Extract data from response
            result = response["data"]["result"]
            prompt = result["prompt"]
            ai_platform = prompt["aiPlatform"]
            messages = result["messages"]
            platform_config = result.get("platformConfig", {})

            # Extract and format the prompt details
            prompt_details = {
                "ai_platform": ai_platform["platform"],
                "model": ai_platform["model"],
                "system_prompt": messages.get("systemMessage", ""),
                "temperature": ai_platform["temp"],
                "max_tokens": ai_platform["max_tokens"],
                "messages": messages.get("messages", []),
                "top_p": ai_platform["top_p"],
                "frequency_penalty": ai_platform["frequency_penalty"],
                "presence_penalty": ai_platform["presence_penalty"],
                "response_format": ai_platform["response_format"],
                "version": prompt["version"],
                "platform_config": platform_config,  # Include platform config if needed
            }

            logger.info(
                f"Successfully fetched details for prompt_id: {prompt_id}, version: {version}"
            )
            logger.debug(f"Prompt details: {prompt_details}")

            # Cache the prompt details
            cache_key = f"{prompt_id}_{session_id}_v{prompt['version']}"
            logger.info(f"Caching details with key: {cache_key}")
            CacheManager.set_prompt_details(cache_key, prompt_details)

            return prompt_details

        except Exception as e:
            logger.error(f"Error fetching prompt details: {str(e)}")
            raise

    def modify_messages_for_openai(self, messages):
        """Convert file types to image_url format for OpenAI"""
        modified_messages = []
        supported_extensions = [".png", ".jpeg", ".jpg", ".webp", ".jfif"]

        for message in messages:
            modified_content = []
            for content in message.get("content", []):
                if content.get("type") == "file" and content.get("file_url", {}).get(
                    "url"
                ):
                    image_url = content["file_url"]["url"]
                    _, extension = os.path.splitext(image_url)
                    if extension.lower() not in supported_extensions:
                        raise ValueError(
                            f"Unsupported image extension: {extension}. "
                            "We currently support PNG (.png), JPEG (.jpeg and .jpg), "
                            "WEBP (.webp), and JFIF (.jfif)"
                        )
                    modified_content.append(
                        {"type": "image_url", "image_url": {"url": image_url}}
                    )
                else:
                    modified_content.append(content)

            modified_messages.append(
                {"role": message["role"], "content": modified_content}
            )
        return modified_messages

    async def _make_openai_request(self, prompt_details: Dict, payload: Dict) -> Dict:
        """Make a direct request to OpenAI"""
        logger.info("Preparing OpenAI API request")

        logger.info(f"Prompt details: {prompt_details}")
        logger.info(f"Payload: {payload}")

        # Get OpenAI API key from environment when in bypass mode
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required when using bypass mode"
            )

        # Extract messages from payload
        messages = payload.get("user_message", [])

        # Format messages for OpenAI while preserving structure
        formatted_messages = []

        # Add system message if present
        # if prompt_details.get("system_prompt"):
        #     formatted_messages.append(
        #         {"role": "system", "content": prompt_details["system_prompt"]}
        #     )

        # Process each message and handle file types
        messages = self.modify_messages_for_openai(messages)
        logger.info(f"Messages after modification: {messages}")

        # Remove the first object (system message) and extend the formatted messages
        if len(messages) > 0:
            formatted_messages.extend(messages[1:])  # Skip the first message

        # Add system message at the start if present
        if prompt_details.get("system_prompt"):
            formatted_messages.insert(
                0,
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": prompt_details["system_prompt"]}
                    ],
                },
            )

        logger.info(f"Formatted messages after processing: {formatted_messages}")
        try:
            logger.info("Making request to OpenAI API")
            response = openai_interaction(
                secret_key=openai_api_key,  # Use OpenAI key from environment
                model=prompt_details["model"],
                messages=formatted_messages,
                temperature=prompt_details.get("temp", 0.7),
                max_tokens=prompt_details["max_tokens"],
                top_p=prompt_details.get("top_p", 0.5),
                frequency_penalty=prompt_details.get("frequency_penalty", 0.7),
                presence_penalty=prompt_details.get("presence_penalty", 0.3),
                response_format={"type": "text"},
            )
            logger.info("Successfully received response from OpenAI")
            return response
        except Exception as e:
            logger.error(f"Error making OpenAI request: {str(e)}")
            raise

    async def _make_anthropic_request(
        self, prompt_details: Dict, payload: Dict
    ) -> Dict:
        """Make a direct request to Anthropic"""
        logger.info("Preparing Anthropic API request")
        user_message = next(
            (msg for msg in payload["user_message"] if msg["type"] == "text"), None
        )
        if not user_message:
            logger.error("No text message found in payload")
            raise ValueError("Text message is required for Anthropic requests")

        try:
            logger.info("Making request to Anthropic API")
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "model": prompt_details["model"],
                    "messages": [
                        {"role": "system", "content": prompt_details["system_prompt"]},
                        {"role": "user", "content": user_message["text"]},
                    ],
                    "max_tokens": prompt_details["max_tokens"],
                },
            )
            response.raise_for_status()
            data = response.json()
            logger.info("Successfully received response from Anthropic")
            return {"response": data["content"][0]["text"]}
        except Exception as e:
            logger.error(f"Error making Anthropic request: {str(e)}")
            raise

    async def _direct_ai_request(
        self, prompt_id: str, session_id: str, payload: Dict
    ) -> Dict:
        """Handle direct AI platform requests"""
        logger.info(f"Processing direct AI request for prompt_id: {prompt_id}")
        logger.info(f"Payload _direct_ai_request: {payload}")

        # Get version from payload
        version = (
            str(payload.get("version")) if payload.get("version") is not None else None
        )

        if version:
            cache_key = f"{prompt_id}_{session_id}_v{version}"
            prompt_details = CacheManager.get_prompt_details(cache_key)
        else:
            # Try to find latest version in cache
            prompt_details = None
            logger.info("No version specified, will fetch latest version")

        if not prompt_details:
            logger.info(f"Prompt details not found in cache, fetching from server")
            prompt_details = await self._fetch_and_cache_prompt_details(
                prompt_id, version
            )
            version = prompt_details[
                "version"
            ]  # Get the version (might be latest if none was specified)

        logger.info(
            f"Making request to AI platform: {prompt_details['ai_platform']} with version {version}"
        )
        try:
            if prompt_details["ai_platform"] == "openai":
                return await self._make_openai_request(prompt_details, payload)
            elif prompt_details["ai_platform"] == "anthropic":
                return await self._make_anthropic_request(prompt_details, payload)
            else:
                logger.error(
                    f"Unsupported AI platform: {prompt_details['ai_platform']}"
                )
                raise ValueError(
                    f"Unsupported AI platform: {prompt_details['ai_platform']}"
                )
        except Exception as e:
            logger.error(f"Error in direct AI request: {str(e)}")
            raise

    async def chat_with_prompt(
        self,
        prompt_id: str,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[int] = None,
    ) -> Dict[str, str]:
        """
        Chat with a specific prompt

        Args:
            prompt_id: ID of the prompt
            user_message: List of message dictionaries
            memory_type: Type of memory ('fullMemory', 'windowMemory', or 'summarizedMemory')
            window_size: Size of the memory window
            session_id: Session identifier
            variables: Dictionary of variables
            version: Optional version number

        Returns:
            Dictionary containing the response
        """
        logger.info(f"Starting chat with prompt_id: {prompt_id}")
        logger.info(f"User message777777777: {user_message}")
        payload = {
            "user_message": user_message,
            "memory_type": memory_type,
            "window_size": window_size,
            "session_id": session_id,
            "variables": variables,
            "request_from": "python_sdk",
            "env": self.env,
        }

        if version is not None:
            logger.info(f"Using prompt version: {version}")
            payload["version"] = version

        try:
            if self.bypass:
                logger.info("Bypass mode enabled, making direct AI request")
                return await self._direct_ai_request(prompt_id, session_id, payload)
            else:
                logger.info("Making request to PromptStudio API")
                return self._request(
                    f"/chat_with_prompt_version/{prompt_id}",
                    method="POST",
                    json=payload,
                )
        except Exception as e:
            logger.error(f"Error in chat_with_prompt: {str(e)}")
            raise

    async def _make_ai_platform_request(
        self,
        platform_name: str,
        prompt_details: Dict,
        messages: List[Dict],
        system_message: str,
    ) -> Dict:
        """
        Make request to the appropriate AI platform

        Args:
            platform_name: Name of the AI platform (openai, anthropic, etc.)
            prompt_details: Dictionary containing prompt configuration
            messages: List of messages to send
            system_message: System message to use

        Returns:
            Dictionary containing the response
        """
        logger.info(f"Making request to AI platform: {platform_name}")

        try:
            if platform_name.lower() == "openai":
                return await self._make_openai_request(
                    prompt_details, {"user_message": messages}
                )
            elif platform_name.lower() == "anthropic":
                return await self._make_anthropic_request(
                    prompt_details, {"user_message": messages}
                )
            elif platform_name.lower() == "gemini":
                # Get Gemini API key from environment
                gemini_api_key = os.getenv("GEMINI_API_KEY")
                if not gemini_api_key:
                    raise ValueError(
                        "GEMINI_API_KEY environment variable is required when using Gemini"
                    )

                return gemini_interaction_chat_with_prompt(
                    secret_key=gemini_api_key,  # Use Gemini key from environment
                    model=prompt_details["model"],
                    messages=messages,
                    system_message=system_message,
                    temperature=prompt_details.get("temp", 0.7),
                    max_output_tokens=prompt_details.get("max_tokens", 1000),
                    top_p=prompt_details.get("top_p", 0.8),
                    top_k=prompt_details.get("top_k", 40),
                    response_format=prompt_details.get(
                        "response_format", {"type": "text"}
                    ),
                )
            else:
                error_msg = f"Unsupported AI platform: {platform_name}"
                logger.error(error_msg)
                raise ValueError(error_msg)

        except Exception as e:
            logger.error(f"Error in _make_ai_platform_request: {str(e)}")
            raise


def openai_interaction(
    secret_key,
    model,
    messages,
    temperature,
    max_tokens,
    top_p,
    frequency_penalty,
    presence_penalty,
    response_format,
):
    """Make a request to OpenAI API"""
    # Set the OpenAI API key
    client = OpenAI(api_key=secret_key)

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            response_format=response_format,
        )
        logger.info(f"OpenAI response: {response}")

        # Get the response content using the new API format
        assistant_reply = response.choices[0].message.content.strip()

        if response_format["type"] == "text":
            logger.info(f"OpenAI response format: text")
            # For text responses, try to parse JSON if it's in that format
            try:
                parsed_reply = json.loads(assistant_reply)
                if (
                    isinstance(parsed_reply, list)
                    and len(parsed_reply) > 0
                    and "text" in parsed_reply[0]
                ):
                    assistant_reply = parsed_reply[0]["text"]
                elif isinstance(parsed_reply, str):
                    assistant_reply = parsed_reply
            except json.JSONDecodeError:
                # If it's not valid JSON, keep the original string
                pass

            # Remove surrounding quotes if present
            assistant_reply = assistant_reply.strip('"')

            # If it's still a valid JSON string, parse it one more time
            try:
                parsed_reply = json.loads(assistant_reply)
                if isinstance(parsed_reply, str):
                    assistant_reply = parsed_reply
            except json.JSONDecodeError:
                pass
        else:
            logger.info(f"OpenAI response format: json")
            # For JSON responses, parse the JSON string
            assistant_reply = json.loads(assistant_reply)

        return {
            "response": assistant_reply,
        }
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise


def format_messages_for_gemini(messages, system_message=None):
    formatted_messages = []

    for i, msg in enumerate(messages):
        role = msg.get("role")
        content = msg.get("content")

        if isinstance(content, list):
            text_content = " ".join(
                [
                    (
                        part.get("text", "")
                        if isinstance(part.get("text"), str)
                        else json.dumps(part.get("text", ""))
                    )
                    for part in content
                    if part.get("type") == "text"
                ]
            )
        elif isinstance(content, str):
            text_content = content
        else:
            text_content = json.dumps(content)

        if i == 0 and system_message:
            text_content = f"{system_message}\n\n{text_content}"

        formatted_messages.append(
            {
                "role": "user" if role in ["user", "system"] else "model",
                "parts": [{"text": text_content}],
            }
        )

    return formatted_messages


def create_response_schema(payload: dict) -> content.Schema:
    def create_property_schema(prop):
        if isinstance(prop["type"], list):
            # Handle multiple types
            #  return content.Schema(
            #     type=content.Type.UNION,
            return glm.Content.Schema(
                type=glm.Content.Type.STRING,
                items=[
                    create_property_schema({"type": t})
                    for t in prop["type"]
                    if t != "null"
                ],
            )
        elif prop["type"] == "string":
            return content.Schema(type=content.Type.STRING)
        elif prop["type"] == "integer":
            return content.Schema(type=content.Type.INTEGER)
        elif prop["type"] == "number":
            return content.Schema(type=content.Type.NUMBER)
        elif prop["type"] == "boolean":
            return content.Schema(type=content.Type.BOOLEAN)
        elif prop["type"] == "array":
            if "items" in prop:
                return content.Schema(
                    type=content.Type.ARRAY, items=create_property_schema(prop["items"])
                )
            return content.Schema(type=content.Type.ARRAY)
        elif prop["type"] == "object":
            return create_response_schema(prop)
        else:
            return content.Schema(
                type=content.Type.STRING
            )  # Default to string for unknown types

    properties = {}
    for key, value in payload["properties"].items():
        properties[key] = create_property_schema(value)

    required = payload.get("required", [])
    return content.Schema(
        type=content.Type.OBJECT, properties=properties, required=required
    )


def gemini_interaction_chat_with_prompt(
    secret_key,
    model,
    messages,
    system_message,
    temperature,
    max_output_tokens,
    top_p,
    top_k,
    response_format,
):
    genai.configure(api_key=secret_key)

    if system_message and system_message.strip():
        gemini_model = genai.GenerativeModel(
            model_name=model, system_instruction=system_message
        )
    else:
        gemini_model = genai.GenerativeModel(model_name=model)

    if response_format["type"] == "text":
        response_schema = None
        response_mime_type = "text/plain"
    else:
        try:
            response_schema = create_gemini_schema(response_format)
            response_mime_type = "application/json"
        except Exception as e:
            raise ValueError(f"Invalid JSON schema")

    generated_history = convert_messages_to_gemini_format(messages)
    # Prepare the message to send
    last_message_parts = generated_history[-1]["parts"]

    # Check if there is any text in the last message parts
    if not any(isinstance(part, str) and part.strip() for part in last_message_parts):
        # If no text is found, add a default text message
        last_message_parts = [""] + last_message_parts

    chat = gemini_model.start_chat(history=generated_history)

    try:

        response = chat.send_message(
            last_message_parts,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                response_schema=response_schema,
                response_mime_type=response_mime_type,
            ),
        )

        # Check if we have a valid response
        if response is None:
            raise ValueError("No valid response received from Gemini API")

        # The last response will be the model's reply to the most recent user message
        if response_mime_type == "text/plain":
            assistant_reply = response.text

        else:
            assistant_reply = response.candidates[0].content.parts[0].text
            assistant_reply = json.loads(assistant_reply)

        return {"response": assistant_reply}

    except genai.types.generation_types.BlockedPromptException as e:
        raise ValueError(f"Gemini API error: The prompt was blocked. Reason: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in Gemini interaction: {str(e)}")
        raise ValueError(f"Unexpected error occurred: {str(e)}")


def create_gemini_schema(response_dict: Dict[str, Any]) -> genai.protos.Schema:
    """
    Convert any dictionary into a Gemini response schema format.

    Args:
        response_dict (dict): Input dictionary to convert

    Returns:
        genai.protos.Schema: Gemini schema format
    """

    def _process_value(value: Any) -> genai.protos.Schema:
        if isinstance(value, dict):
            if "type" in value:
                # Handle OpenAPI/JSON schema style definitions
                schema_type = value["type"].upper()
                properties = {}
                required = []

                if schema_type == "OBJECT" and "properties" in value:
                    properties = {
                        k: _process_value(v) for k, v in value["properties"].items()
                    }
                    required = value.get("required", [])
                elif schema_type == "ARRAY" and "items" in value:
                    return genai.protos.Schema(
                        type=genai.protos.Type.ARRAY,
                        items=_process_value(value["items"]),
                    )

                schema = genai.protos.Schema(
                    type=getattr(genai.protos.Type, schema_type),
                    properties=properties,
                    required=required,
                )

                # Handle enums if present
                if "enum" in value:
                    schema = genai.protos.Schema(
                        type=genai.protos.Type.STRING, enum=value["enum"]
                    )

                # Handle description if present
                if "description" in value:
                    schema.description = value["description"]

                return schema
            else:
                # Handle nested dictionary without type specification
                return genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={k: _process_value(v) for k, v in value.items()},
                )
        elif isinstance(value, list):
            if value:
                return genai.protos.Schema(
                    type=genai.protos.Type.ARRAY, items=_process_value(value[0])
                )
            return genai.protos.Schema(
                type=genai.protos.Type.ARRAY,
                items=genai.protos.Schema(type=genai.protos.Type.STRING),
            )
        elif isinstance(value, bool):
            return genai.protos.Schema(type=genai.protos.Type.BOOLEAN)
        elif isinstance(value, int):
            return genai.protos.Schema(type=genai.protos.Type.INTEGER)
        elif isinstance(value, float):
            return genai.protos.Schema(type=genai.protos.Type.NUMBER)
        else:
            return genai.protos.Schema(type=genai.protos.Type.STRING)

    # Process the root schema
    return _process_value(response_dict)


def convert_messages_to_gemini_format(messages):
    gemini_messages = []
    for message in messages:
        role = "user" if message["role"] == "user" else "model"
        parts = []

        for content in message["content"]:
            if content["type"] == "text":
                parts.append(content["text"])
            elif content["type"] == "file":
                parts.append(upload_file_to_gemini(file_url=content["file_url"]["url"]))

        gemini_messages.append({"role": role, "parts": parts})

    return gemini_messages


def upload_file_to_gemini(file_url):

    with tempfile.TemporaryDirectory() as tempdir:
        tempfiles = Path(tempdir)
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.content

        # Generate file name and path
        name = file_url.split("/")[-1]
        hash = hashlib.sha256(data).hexdigest()
        path = tempfiles / hash

        # Write data to file
        path.write_bytes(data)

        print("Uploading:", file_url)
        mime_type = identify_mime_type(file_url)
        file_content = genai.upload_file(path, mime_type=mime_type)
        return file_content


def identify_mime_type(file_url):
    # Extract the file extension from the URL
    _, file_extension = os.path.splitext(file_url)
    file_extension = file_extension.lower()

    # Define custom mappings for specific file types
    custom_mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".jfif": "image/jpeg",
        ".webp": "image/webp",
        ".heic": "image/heic",
        ".heif": "image/heif",
        ".wav": "audio/wav",
        ".mp3": "audio/mp3",
        ".aiff": "audio/aiff",
        ".aac": "audio/aac",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
    }

    # Check if the file extension is in our custom mappings
    if file_extension in custom_mime_types:
        return custom_mime_types[file_extension]

    # If not in custom mappings, use mimetypes library as a fallback
    mime_type, _ = mimetypes.guess_type(file_url)

    # If mimetypes library couldn't determine the type, return a default
    if mime_type is None:
        return "application/octet-stream"

    return mime_type


async def summarymemory_save_log_ai_interaction_prompt(
    self,
    user_id: str,
    user_prompt_id: str,
    user_prompt: dict,
    interaction_request: Dict,
) -> Dict:
    """Process and save AI interaction using summary memory cache"""
    try:
        logger.info(f"Processing AI interaction for user_id: {user_id}")
        logger.info(f"User prompt details: {user_prompt}")
        logger.info(f"Interaction request: {interaction_request}")

        # Generate session_id if not present
        session_id = interaction_request.get("session_id") or str(uuid.uuid4())
        logger.info(f"Using session_id: {session_id}")

        # Print initial cache state
        logger.info("Initial cache state:")
        CacheManager.print_cache_contents()
        InteractionCacheManager.print_cache_contents()

        # Get version (either from request or fetch latest)
        version = interaction_request.get("version")
        logger.info(f"Version: {version}")
        if not version:
            logger.info(f"Fetching latest version for prompt_id: {user_prompt_id}")
            latest_version_response = await self._request(
                f"/fetch/prompt/latest_version/{user_prompt_id}"
            )
            version = str(latest_version_response["data"]["latest_version"])
        logger.info(f"Using version: {version}")

        # First fetch and cache prompt details
        cache_key = f"{user_prompt_id}_{session_id}_v{version}"
        prompt_details = CacheManager.get_prompt_details(cache_key)

        if not prompt_details:
            # Fetch and cache if not found
            prompt_details = await self._fetch_and_cache_prompt_details(
                user_prompt_id, version
            )
            logger.info(f"Cached new prompt details for {cache_key}")

        # Get interaction history
        interaction_history = InteractionCacheManager.get_interaction_history(
            user_prompt_id, session_id, version
        )
        logger.info(f"Retrieved interaction history: {interaction_history}")

        # Initialize message collection
        prompt_collection_msg = []
        if user_prompt["platform"] == "openai":
            prompt_collection_msg.append(
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": prompt_details["system_prompt"]}
                    ],
                }
            )

        # Get existing summarized content
        summarized_content = self._get_existing_summarized_content(
            interaction_history, session_id
        )

        if not summarized_content:
            # If no summary exists, generate one from all messages
            prompt_collection_msg.extend(
                interaction_history.get("messages", []) if interaction_history else []
            )

            # Add new user message for summary generation
            prompt_collection_msg.extend(
                [
                    {
                        "role": "user",
                        "content": interaction_request["user_message"],
                    },
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": self.SUMMARY_PROMPT}],
                    },
                ]
            )

            # Generate summary
            summarized_content = await self._generate_summary(
                prompt_collection_msg, prompt_details, interaction_request
            )
            logger.info(f"Generated new summary: {summarized_content}")

        # Prepare messages for new response
        new_messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": prompt_details["system_prompt"]}],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": f"Previous conversation summary: {summarized_content}",
                    }
                ],
            },
            {
                "role": "user",
                "content": interaction_request["user_message"],
            },
        ]

        # Get AI response
        response = await self._make_ai_platform_request(
            platform_name=prompt_details["ai_platform"],
            prompt_details={
                **prompt_details,
                "response_format": prompt_details.get(
                    "response_format", {"type": "text"}
                ),
            },
            messages=new_messages,
            system_message=prompt_details["system_prompt"],
        )
        logger.info(f"Response from AI platform: {response}")

        assistant_reply = response["response"]
        logger.info(f"Assistant reply: {assistant_reply}")

        # Create new messages to save
        current_time = datetime.now().isoformat()
        new_messages = [
            {
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": interaction_request["user_message"],
                "env": interaction_request.get("env", "test"),
                "requestFrom": interaction_request.get("request_from", "sdk"),
                "initiatedAt": current_time,
            },
            {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": [{"type": "text", "text": f"{assistant_reply}"}],
                "env": interaction_request.get("env", "test"),
                "requestFrom": interaction_request.get("request_from", "sdk"),
                "initiatedAt": current_time,
            },
        ]

        # Save to cache with summary
        InteractionCacheManager.save_interaction(
            session_id=session_id,
            interaction_data={
                "messages": new_messages,
                "lastResponseAt": current_time,
                "memory_type": "summarizedMemory",
                "summarized_content": summarized_content,
            },
            prompt_id=user_prompt_id,
            version=version,
        )

        # Print final cache state
        logger.info("Final cache state after interaction:")
        CacheManager.print_cache_contents()
        InteractionCacheManager.print_cache_contents()

        return {
            "message": "AI interaction saved successfully for memory type: summarized memory",
            "user_prompt_id": user_prompt_id,
            "response": assistant_reply,
            "session_id": session_id,
        }

    except Exception as e:
        error_message = f"An error occurred while processing AI interaction: {str(e)}"
        logger.error(error_message)
        raise ValueError(error_message)


# Helper methods for summary memory
SUMMARY_PROMPT = """Please provide a concise summary of the conversation so far, 
highlighting the key points and important context that would be relevant for continuing the discussion."""


def _get_existing_summarized_content(
    self, interaction_history: Dict, session_id: str
) -> str:
    """Get existing summarized content from interaction history"""
    if (
        interaction_history
        and interaction_history.get("memory_type") == "summarizedMemory"
        and "summarized_content" in interaction_history
    ):
        return interaction_history["summarized_content"]
    return ""


async def _generate_summary(
    self, messages: list, prompt_details: Dict, interaction_request: Dict
) -> str:
    """Generate a summary of the conversation"""
    try:
        # Make request to AI platform for summary
        response = await self._make_ai_platform_request(
            platform_name=prompt_details["ai_platform"],
            prompt_details={
                **prompt_details,
                "response_format": {"type": "text"},
            },
            messages=messages,
            system_message=self.SUMMARY_PROMPT,
        )

        return response["response"]
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise ValueError(f"Failed to generate summary: {str(e)}")
