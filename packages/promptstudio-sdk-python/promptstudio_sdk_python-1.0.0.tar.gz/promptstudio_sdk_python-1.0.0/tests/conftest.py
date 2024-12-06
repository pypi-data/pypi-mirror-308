import pytest
import os
from promptstudio import PromptManager
from promptstudio.prompt.types import (
    MessageType,
    Memory,
    MessageContent,
    RequestPayload,
)


@pytest.fixture
def api_key():
    return "test_api_key"


@pytest.fixture
def prompt_manager(api_key):
    return PromptManager(api_key=api_key, env="test")


@pytest.fixture
def bypass_prompt_manager(api_key):
    return PromptManager(api_key=api_key, env="test", bypass=True)


@pytest.fixture
def sample_request():
    return RequestPayload(
        user_message=[MessageContent(type=MessageType.TEXT, text="Test message")],
        memory_type=Memory.SUMMARIZED_MEMORY,
        window_size=10,
        session_id="test_session",
        variables={},
        version=1.0,
    )


@pytest.fixture
def sample_image_request():
    return RequestPayload(
        user_message=[
            MessageContent(type=MessageType.TEXT, text="Describe this image"),
            MessageContent(
                type=MessageType.FILE, file_url={"url": "https://example.com/test.jpg"}
            ),
        ],
        memory_type=Memory.SUMMARIZED_MEMORY,
        window_size=10,
        session_id="test_session",
        variables={},
        version=1.0,
    )
