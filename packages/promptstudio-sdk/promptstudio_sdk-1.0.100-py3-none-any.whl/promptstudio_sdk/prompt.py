import base64
import aiohttp
from typing import List, Dict, Any, Optional, Union
from fastapi import HTTPException
import google.generativeai as genai
from anthropic import Anthropic
import openai
from enum import Enum
from pydantic import BaseModel

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


from promptstudio_sdk.cache import PromptCache
from promptstudio_sdk.base import Base

SUMMARY_PROMPT = """Summarize the above conversation in a detailed, concise, and well-structured manner. 
ensuring the summary does not exceed 250 words. Capture the key points and context, including important 
questions, answers, and relevant follow-up, while avoiding unnecessary repetition."""


class PromptManager(Base):
    """Manages prompts for AI interactions, including caching and API calls."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize PromptManager with configuration"""
        super().__init__(config)
        self.cache = PromptCache()

    async def chat_with_prompt(
        self,
        prompt_id: str,
        user_message: List[Dict[str, Any]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Chat with a prompt using the API.
        """
        try:
            logger.info(f"Starting chat with prompt ID: {prompt_id}")
            logger.info(f"Session ID: {session_id}")
            logger.info(f"Memory Type: {memory_type}")
            logger.info(f"Window Size: {window_size}")
            logger.info(f"User Message: {user_message}")

            # Format payload for API
            payload = {
                "user_message": user_message,
                "memory_type": memory_type,
                "window_size": window_size,
                "session_id": session_id,
                "variables": variables,
                "request_from": "python_sdk",
                "env": self.env,
                "version": version,
            }

            logger.info("Prepared payload for API request")
            logger.debug(
                f"Full payload: {payload}"
            )  # More detailed logging at debug level

            endpoint = f"/chat_with_prompt_version/{prompt_id}"
            logger.info(f"Making API request to endpoint: {endpoint}")

            # Make direct API call
            response = await self.request(
                endpoint,
                method="POST",
                data=payload,
            )

            logger.info("Received response from API")
            logger.debug(
                f"Full response: {response}"
            )  # More detailed logging at debug level

            if "data" in response and "response" in response["data"]:
                logger.info("Successfully processed chat response")
                response_preview = (
                    response["data"]["response"][:100] + "..."
                )  # Preview first 100 chars
                logger.info(f"Response preview: {response_preview}")
            else:
                logger.warning("Unexpected response format")

            return response

        except Exception as e:
            logger.error(f"Error in chat_with_prompt: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"API call failed: {str(e)}")

    async def get_prompt_details(
        self, prompt_id: str, version: Optional[float] = None
    ) -> Dict:
        """Get prompt details from the API"""
        response = await self.request(
            f"/fetch/prompt/version_data/{prompt_id}",
            method="POST",
            data={"version": version},
        )
        return response

    async def _convert_image_to_base64(self, image_url: str) -> str:
        """Convert image URL to base64 string"""
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                image_data = await response.read()
                return base64.b64encode(image_data).decode("utf-8")

    async def _handle_gemini_chat(
        self,
        prompt_details: Dict,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[int] = None,
    ) -> Dict[str, str]:
        """Handle chat with Google's Gemini model"""
        try:
            # Configure Gemini
            api_key = prompt_details["data"]["result"]["platformConfig"]["platformKey"]
            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(
                model_name=prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "model"
                ],
                generation_config={
                    "temperature": prompt_details["data"]["result"]["prompt"][
                        "ai_platform"
                    ]["temp"],
                    "top_k": prompt_details["data"]["result"]["prompt"]["ai_platform"][
                        "top_k"
                    ],
                    "top_p": prompt_details["data"]["result"]["prompt"]["ai_platform"][
                        "top_p"
                    ],
                    "max_output_tokens": prompt_details["data"]["result"]["prompt"][
                        "ai_platform"
                    ]["max_tokens"],
                },
            )

            # Get cached messages based on memory type
            messages = []
            if session_id:
                cached_messages = await self.cache.get_cached_response(session_id)

                if cached_messages:
                    if memory_type == "summarizedMemory":
                        summary = await self.cache.get_cached_summary(session_id)
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {user_message}"
                                        }
                                    ],
                                }
                            )
                    elif memory_type == "windowMemory":
                        window_size = window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in user_message:
                if msg.type == "text":
                    user_message_parts.append({"text": msg.text})
                elif msg.type == "file":
                    user_message_parts.append(
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": await self._convert_image_to_base64(
                                    msg.file_url.url
                                ),
                            }
                        }
                    )

            messages.append({"role": "user", "parts": user_message_parts})

            # Generate response
            chat = model.start_chat(history=messages)
            response = await chat.send_message(user_message_parts)

            # Update summary if using summarized memory
            if memory_type == "summarizedMemory":
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self,
        prompt_details: Dict,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[int] = None,
    ) -> Dict[str, str]:
        """Handle chat with OpenAI models"""
        try:
            # Configure OpenAI
            api_key = prompt_details["data"]["result"]["platformConfig"]["platformKey"]
            client = openai.AsyncOpenAI(api_key=api_key)

            messages = []
            system_message = prompt_details["data"]["result"]["messages"][
                "systemMessage"
            ]
            if system_message:
                messages.append({"role": "system", "content": system_message})

            # Handle memory and cached messages
            if session_id:
                cached_messages = await self.cache.get_cached_response(session_id)
                if cached_messages:
                    if memory_type == "summarizedMemory":
                        summary = await self.cache.get_cached_summary(session_id)
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": f"Previous conversation summary: {summary}",
                                        }
                                    ],
                                }
                            )
                    elif memory_type == "windowMemory":
                        window_size = window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in user_message:
                if msg.type == "text":
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == "file":
                    user_content.append(
                        {"type": "image_url", "image_url": {"url": msg.file_url.url}}
                    )

            messages.append({"role": "user", "content": user_content})

            # Generate response
            response = await client.chat.completions.create(
                model=prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "model"
                ],
                messages=messages,
                temperature=prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "temp"
                ],
                max_tokens=prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "max_tokens"
                ],
                top_p=prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "top_p"
                ],
                frequency_penalty=prompt_details["data"]["result"]["prompt"][
                    "ai_platform"
                ]["frequency_penalty"],
                presence_penalty=prompt_details["data"]["result"]["prompt"][
                    "ai_platform"
                ]["presence_penalty"],
            )

            response_text = response.choices[0].message.content

            # Update summary if using summarized memory
            if memory_type == "summarizedMemory":
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self,
        prompt_details: Dict,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[int] = None,
    ) -> Dict[str, str]:
        """Handle chat with Anthropic's Claude model"""
        try:
            # Configure Anthropic
            api_key = prompt_details["data"]["result"]["platformConfig"]["platformKey"]
            client = Anthropic(api_key=api_key)

            messages = []
            system_message = prompt_details["data"]["result"]["messages"][
                "systemMessage"
            ]

            # Handle memory and cached messages
            if session_id:
                cached_messages = await self.cache.get_cached_response(session_id)
                if cached_messages:
                    if memory_type == "summarizedMemory":
                        summary = await self.cache.get_cached_summary(session_id)
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif memory_type == "windowMemory":
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in user_message:
                if msg.type == "text":
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == "file":
                    base64_image = await self._convert_image_to_base64(msg.file_url.url)
                    user_content.append(
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image,
                            },
                        }
                    )

            # Generate response
            response = await client.messages.create(
                model=prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "model"
                ],
                max_tokens=prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "max_tokens"
                ],
                temperature=prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "temp"
                ],
                system=system_message,
                messages=messages + [{"role": "user", "content": user_content}],
            )

            response_text = response.content[0].text

            # Update summary if using summarized memory
            if memory_type == "summarizedMemory":
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Claude chat error: {str(e)}")

    async def _generate_summary(
        self, model: Any, messages: List[Dict[str, Any]]
    ) -> str:
        """Generate a summary of the conversation"""
        try:
            if isinstance(model, genai.GenerativeModel):
                # Gemini summary generation
                messages.append({"role": "user", "parts": [{"text": SUMMARY_PROMPT}]})
                response = await model.generate_content(messages)
                return response.text

            elif isinstance(model, openai.AsyncOpenAI):
                # OpenAI summary generation
                messages.append({"role": "user", "content": SUMMARY_PROMPT})
                response = await model.chat.completions.create(
                    model="gpt-4", messages=messages, temperature=0.7, max_tokens=250
                )
                return response.choices[0].message.content

            elif isinstance(model, Anthropic):
                # Claude summary generation
                messages.append({"role": "user", "content": SUMMARY_PROMPT})
                response = await model.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=250,
                    temperature=0.7,
                    messages=messages,
                )
                return response.content[0].text

            else:
                raise ValueError(
                    f"Unsupported model type for summary generation: {type(model)}"
                )

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Summary generation error: {str(e)}"
            )
        # """Convert image URL to base64 string"""
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(image_url) as response:
        #         image_data = await response.read()
        #         return base64.b64encode(image_data).decode("utf-8")
