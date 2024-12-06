"""
PromptStudio SDK
~~~~~~~~~~~~~~~

A Python SDK for interacting with PromptStudio's API, providing seamless integration 
with various AI models including OpenAI, Google's Gemini, and Anthropic's Claude.

Basic usage:

    >>> import asyncio
    >>> from promptstudio import PromptManager
    >>> from promptstudio.prompt.types import MessageType, Memory, MessageContent
    >>> 
    >>> async def main():
    ...     prompt_manager = PromptManager(
    ...         api_key="your_api_key_here",
    ...         env="test"
    ...     )
    ...     
    ...     request = {
    ...         "user_message": [{
    ...             "type": "text",
    ...             "text": "What is artificial intelligence?"
    ...         }],
    ...         "memory_type": "summarizedMemory",
    ...         "window_size": 10,
    ...         "session_id": "test_session",
    ...         "variables": {},
    ...         "version": 1.0
    ...     }
    ...     
    ...     response = await prompt_manager.chat_with_prompt(
    ...         "your_prompt_id_here",
    ...         request
    ...     )
    ...     print(response)
    >>> 
    >>> asyncio.run(main())

For more information, please see the documentation:
https://docs.promptstudio.dev
"""

from .prompt import PromptManager
from .prompt.types import (
    MessageType,
    Memory,
    MessageContent,
    FileUrl,
    RequestPayload,
    PromptResponse,
    PromptDetail,
    AIPlatform,
)

__version__ = "1.0.0"
__author__ = "PromptStudio"
__license__ = "MIT"
__copyright__ = "Copyright 2024 PromptStudio"

__all__ = [
    "PromptManager",
    "MessageType",
    "Memory",
    "MessageContent",
    "FileUrl",
    "RequestPayload",
    "PromptResponse",
    "PromptDetail",
    "AIPlatform",
]

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
