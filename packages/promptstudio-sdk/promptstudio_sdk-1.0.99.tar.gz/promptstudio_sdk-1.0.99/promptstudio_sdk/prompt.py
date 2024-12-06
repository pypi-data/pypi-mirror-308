import base64
import aiohttp
from typing import List, Dict, Any, Optional, Union
from fastapi import HTTPException
import google.generativeai as genai
from anthropic import Anthropic
import openai

# from promptstudio_sdk.types import (
#     Memory,
#     MessageType,
#     MessageContent,
#     RequestPayload,
#     FileUrl,
#     Message,
#     AIPlatform,
#     PromptDetail,
#     PromptResponse,
# )
from promptstudio_sdk.cache import PromptCache
from promptstudio_sdk.base import Base


from typing import List, Dict, Union, Optional
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


SUMMARY_PROMPT = """Summarize the above conversation in a detailed, concise, and well-structured manner. 
ensuring the summary does not exceed 250 words. Capture the key points and context, including important 
questions, answers, and relevant follow-up, while avoiding unnecessary repetition."""


class PromptManager(Base):
    def __init__(self, config: Dict[str, Any]):
        """Initialize PromptManager with configuration"""
        super().__init__(config)
        self.cache = PromptCache()

    async def chat_with_prompt(
        self, prompt_id: str, request: RequestPayload
    ) -> Dict[str, Any]:
        """
        Chat with a prompt using either direct API calls or local model integration.

        Args:
            prompt_id: The ID of the prompt to use
            request: The request payload containing message and configuration

        Returns:
            Dict containing the response and metadata
        """
        if self.bypass:
            # Local model integration path
            try:
                # Get prompt details
                prompt_details = await self.get_prompt_details(
                    prompt_id, request.version
                )

                # Handle different AI platforms locally
                platform = prompt_details["data"]["result"]["prompt"]["ai_platform"][
                    "platform"
                ].lower()

                if platform == "gemini":
                    response = await self._handle_gemini_chat(prompt_details, request)
                elif platform == "openai":
                    response = await self._handle_openai_chat(prompt_details, request)
                elif platform == "claude":
                    response = await self._handle_claude_chat(prompt_details, request)
                else:
                    raise ValueError(f"Unsupported AI platform: {platform}")

                # Save to local cache
                await self.cache.save_to_cache(
                    request.session_id, request.user_message, response["response"]
                )

                return {
                    "message": "AI interactions log saved successfully",
                    "data": {
                        "message": f"AI interaction saved successfully for memory type: {request.memory_type}",
                        "user_prompt_id": prompt_id,
                        "response": response["response"],
                        "session_id": request.session_id,
                    },
                }

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        else:
            # Direct API call path
            try:
                # Convert request to dict and add additional fields
                request_dict = request.dict()
                payload = {
                    "user_message": [msg.dict() for msg in request.user_message],
                    "memory_type": request.memory_type.value,
                    "window_size": request.window_size,
                    "session_id": request.session_id,
                    "variables": request.variables,
                    "version": request.version,
                    "request_from": "python_sdk",
                    "env": self.env,
                }

                # Make direct API call
                response = await self.request(
                    f"/chat_with_prompt_version/{prompt_id}",
                    method="POST",
                    data=payload,
                )

                return response

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"API call failed: {str(e)}"
                )

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
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(image_url) as response:
        #             image_data = await response.read()
        #             return base64.b64encode(image_data).decode("utf-8")

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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
        # return base64.b64encode(image_data).decode("utf-8")

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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

    async def _handle_gemini_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )

                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "parts": [
                                        {
                                            "text": f"Previous conversation summary: {summary}\n\nNew message: {request.user_message}"
                                        }
                                    ],
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_message_parts = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_message_parts.append({"text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "parts": [{"text": response.text}]}
                ]
                new_summary = await self._generate_summary(model, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response.text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini chat error: {str(e)}")

    async def _handle_openai_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
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
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        window_size = request.window_size or 10
                        start_idx = max(0, len(cached_messages) - window_size)
                        messages.extend(cached_messages[start_idx:])
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "assistant", "content": response_text}
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

            return {"response": response_text}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI chat error: {str(e)}")

    async def _handle_claude_chat(
        self, prompt_details: Dict, request: RequestPayload
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
            if request.session_id:
                cached_messages = await self.cache.get_cached_response(
                    request.session_id
                )
                if cached_messages:
                    if request.memory_type == Memory.SUMMARIZED_MEMORY:
                        summary = await self.cache.get_cached_summary(
                            request.session_id
                        )
                        if summary:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": f"Previous conversation summary: {summary}",
                                }
                            )
                    elif request.memory_type == Memory.WINDOW_MEMORY:
                        raise ValueError(
                            "Window memory is not supported for Claude. Use summarizedMemory or fullMemory."
                        )
                    else:  # FULL_MEMORY
                        messages.extend(cached_messages)

            # Add new user message
            user_content = []
            for msg in request.user_message:
                if msg.type == MessageType.TEXT:
                    user_content.append({"type": "text", "text": msg.text})
                elif msg.type == MessageType.FILE:
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
            if request.memory_type == Memory.SUMMARIZED_MEMORY:
                summary_messages = messages + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text},
                ]
                new_summary = await self._generate_summary(client, summary_messages)
                await self.cache.save_summary_to_cache(request.session_id, new_summary)

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
