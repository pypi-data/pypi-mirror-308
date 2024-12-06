import pytest
from promptstudio import PromptManager
from promptstudio.prompt.types import (
    MessageType,
    Memory,
    MessageContent,
    RequestPayload,
)
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_chat_with_prompt(prompt_manager, sample_request):
    try:
        response = await prompt_manager.chat_with_prompt(
            "671f7ea3895439853685b020", sample_request
        )
        assert response is not None
        assert "message" in response
    except HTTPException as e:
        pytest.skip(f"Skipping due to API error: {e.detail}")


@pytest.mark.asyncio
async def test_bypass_mode(bypass_prompt_manager, sample_request):
    try:
        response = await bypass_prompt_manager.chat_with_prompt(
            "671f7ea3895439853685b020", sample_request
        )
        assert response is not None
        assert "data" in response
        assert "response" in response["data"]
    except HTTPException as e:
        pytest.skip(f"Skipping due to API error: {e.detail}")


@pytest.mark.asyncio
async def test_image_handling(bypass_prompt_manager, sample_image_request):
    try:
        response = await bypass_prompt_manager.chat_with_prompt(
            "671f7ea3895439853685b020", sample_image_request
        )
        assert response is not None
        assert "data" in response
        assert "response" in response["data"]
    except HTTPException as e:
        pytest.skip(f"Skipping due to API error: {e.detail}")


@pytest.mark.asyncio
async def test_memory_types(bypass_prompt_manager):
    memory_types = [Memory.FULL_MEMORY, Memory.WINDOW_MEMORY, Memory.SUMMARIZED_MEMORY]

    for memory_type in memory_types:
        request = RequestPayload(
            user_message=[MessageContent(type=MessageType.TEXT, text="Test message")],
            memory_type=memory_type,
            window_size=10,
            session_id="test_session",
            variables={},
            version=1.0,
        )

        try:
            response = await bypass_prompt_manager.chat_with_prompt(
                "671f7ea3895439853685b020", request
            )
            assert response is not None
            assert "data" in response
        except HTTPException as e:
            pytest.skip(f"Skipping {memory_type} due to API error: {e.detail}")
