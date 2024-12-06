import pytest
import os
from unittest.mock import Mock, patch
from promptstudio_sdk.prompt import (
    PromptManager,
    Memory,
    MessageType,
    MessageContent,
    RequestPayload,
    FileUrl,
)
from promptstudio_sdk.cache import PromptCache

# Test configurations
TEST_API_KEY = "nDBabew4CGIKD8uKnOqOajG8AZgczzgW"
TEST_PROMPT_ID = "671f7ea3895439853685b020"
TEST_SESSION_ID = "test_session_123"


@pytest.fixture
def prompt_manager():
    config = {"api_key": TEST_API_KEY, "env": "test", "bypass": False}
    return PromptManager(config=config)


@pytest.fixture
def mock_cache():
    with patch("promptstudio_sdk.prompt.PromptCache") as mock:
        yield mock


@pytest.mark.asyncio
async def test_chat_with_prompt_basic(prompt_manager):
    # Test basic text message
    request_payload = RequestPayload(
        user_message=[
            MessageContent(type=MessageType.TEXT, text="Hello, how are you?")
        ],
        memory_type=Memory.FULL_MEMORY,
        window_size=10,
        session_id=TEST_SESSION_ID,
        variables={},
        version=None,
    )

    with patch("promptstudio_sdk.base.Base.request") as mock_request:
        mock_request.return_value = {
            "message": "Success",
            "data": {
                "message": "AI interaction saved successfully",
                "response": "I'm doing well, thank you!",
                "session_id": TEST_SESSION_ID,
            },
        }

        response = await prompt_manager.chat_with_prompt(
            TEST_PROMPT_ID, request_payload
        )
        assert response["message"] == "Success"
        assert "response" in response["data"]


@pytest.mark.asyncio
async def test_chat_with_prompt_image(prompt_manager):
    # Test message with image
    request_payload = RequestPayload(
        user_message=[
            MessageContent(
                type=MessageType.FILE,
                file_url=FileUrl(url="https://example.com/test.jpg"),
            )
        ],
        memory_type=Memory.WINDOW_MEMORY,
        window_size=5,
        session_id=TEST_SESSION_ID,
        variables={},
        version=None,
    )

    with patch("promptstudio_sdk.base.Base.request") as mock_request:
        mock_request.return_value = {
            "message": "Success",
            "data": {
                "message": "AI interaction saved successfully",
                "response": "I see the image you shared.",
                "session_id": TEST_SESSION_ID,
            },
        }

        response = await prompt_manager.chat_with_prompt(
            TEST_PROMPT_ID, request_payload
        )
        assert response["message"] == "Success"
        assert "response" in response["data"]


@pytest.mark.asyncio
async def test_get_prompt_details(prompt_manager):
    with patch("promptstudio_sdk.base.Base.request") as mock_request:
        mock_request.return_value = {
            "data": {
                "result": {
                    "prompt": {"ai_platform": {"platform": "openai", "model": "gpt-4"}}
                }
            }
        }

        response = await prompt_manager.get_prompt_details(TEST_PROMPT_ID)
        assert "data" in response
        assert "result" in response["data"]


@pytest.mark.asyncio
async def test_memory_types(prompt_manager):
    # Test different memory types
    memory_types = [Memory.FULL_MEMORY, Memory.WINDOW_MEMORY, Memory.SUMMARIZED_MEMORY]

    for memory_type in memory_types:
        request_payload = RequestPayload(
            user_message=[MessageContent(type=MessageType.TEXT, text="Test message")],
            memory_type=memory_type,
            window_size=10,
            session_id=TEST_SESSION_ID,
            variables={},
            version=None,
        )

        with patch("promptstudio_sdk.base.Base.request") as mock_request:
            mock_request.return_value = {
                "message": "Success",
                "data": {
                    "message": "AI interaction saved successfully",
                    "response": "Test response",
                    "session_id": TEST_SESSION_ID,
                },
            }

            response = await prompt_manager.chat_with_prompt(
                TEST_PROMPT_ID, request_payload
            )
            assert response["message"] == "Success"
