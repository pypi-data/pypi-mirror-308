import asyncio
from promptstudio import PromptManager
from promptstudio.prompt.types import (
    MessageType,
    Memory,
    MessageContent,
    FileUrl,
    RequestPayload,
)


async def main():
    # Initialize the SDK
    prompt_manager = PromptManager(api_key="your_api_key_here", env="test", bypass=True)

    # Create request payload
    request = RequestPayload(
        user_message=[
            MessageContent(
                type=MessageType.TEXT, text="What is artificial intelligence?"
            )
        ],
        memory_type=Memory.SUMMARIZED_MEMORY,
        window_size=10,
        session_id="test_session",
        variables={},
        version=1.0,
    )

    try:
        # Chat with a prompt
        response = await prompt_manager.chat_with_prompt("your_prompt_id_here", request)
        print("Response:", response)
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    asyncio.run(main())


async def test_with_bypass():
    """Test using local model integration (bypass=True)"""
    prompt_manager = PromptManager(
        api_key="your_api_key_here",
        env="test",
        bypass=True,  # Use local model integration
    )

    request = RequestPayload(
        user_message=[
            MessageContent(
                type=MessageType.TEXT, text="What is artificial intelligence?"
            )
        ],
        memory_type=Memory.SUMMARIZED_MEMORY,
        window_size=10,
        session_id="test_session_bypass",
        variables={},
        version=1.0,
    )

    try:
        response = await prompt_manager.chat_with_prompt("your_prompt_id_here", request)
        print("Bypass Mode Response:", response)
    except Exception as e:
        print("Bypass Mode Error:", str(e))


async def test_without_bypass():
    """Test using direct API calls (bypass=False)"""
    prompt_manager = PromptManager(
        api_key="your_api_key_here", env="test", bypass=False  # Use direct API calls
    )

    request = RequestPayload(
        user_message=[
            MessageContent(
                type=MessageType.TEXT, text="What is artificial intelligence?"
            )
        ],
        memory_type=Memory.SUMMARIZED_MEMORY,
        window_size=10,
        session_id="test_session_api",
        variables={},
        version=1.0,
    )

    try:
        response = await prompt_manager.chat_with_prompt("your_prompt_id_here", request)
        print("API Mode Response:", response)
    except Exception as e:
        print("API Mode Error:", str(e))


async def main():
    # Test both modes
    print("\n=== Testing Bypass Mode (Local Model Integration) ===")
    await test_with_bypass()

    print("\n=== Testing API Mode (Direct API Calls) ===")
    await test_without_bypass()


if __name__ == "__main__":
    asyncio.run(main())
