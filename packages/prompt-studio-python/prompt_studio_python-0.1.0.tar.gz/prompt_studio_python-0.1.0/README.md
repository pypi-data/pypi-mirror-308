# PromptStudio Python SDK

A Python SDK for interacting with PromptStudio's API, providing seamless integration with various AI models including OpenAI, Google's Gemini, and Anthropic's Claude.

## Installation

You can install the PromptStudio SDK using pip:

```bash
pip install promptstudio-sdk
```

Or using poetry:

```bash
poetry add promptstudio-sdk
```

## Features

- Support for multiple AI platforms (OpenAI, Gemini, Claude)
- Local model integration with bypass mode
- Multiple memory management strategies
- Built-in caching system
- Async/await support
- Type safety with Pydantic
- Support for text and file inputs
- Conversation summarization

## Quick Start

Here's a simple example to get you started:

```python
import asyncio
from promptstudio import PromptManager
from promptstudio.prompt.types import MessageType, Memory, MessageContent

async def main():
    # Initialize the SDK
    prompt_manager = PromptManager(
        api_key="your_api_key_here",
        env="test"  # or "prod" for production
    )

    # Create a request
    request = {
        "user_message": [
            {
                "type": "text",
                "text": "What is artificial intelligence?"
            }
        ],
        "memory_type": "summarizedMemory",
        "window_size": 10,
        "session_id": "test_session",
        "variables": {},
        "version": 1.0
    }

    try:
        response = await prompt_manager.chat_with_prompt(
            "your_prompt_id_here",
            request
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

### Using Bypass Mode

Bypass mode allows direct interaction with AI models:

```python
prompt_manager = PromptManager(
    api_key="your_api_key_here",
    env="test",
    bypass=True  # Enable local model integration
)
```

### Memory Types

The SDK supports three types of memory management:

1. Full Memory

```python
request = {
    "memory_type": "fullMemory",
    "window_size": -1,
    # ... other parameters
}
```

2. Window Memory

```python
request = {
    "memory_type": "windowMemory",
    "window_size": 10,
    # ... other parameters
}
```

3. Summarized Memory

```python
request = {
    "memory_type": "summarizedMemory",
    "window_size": 12,
    # ... other parameters
}
```

### Working with Files

You can include files (images) in your messages:

```python
request = {
    "user_message": [
        {
            "type": "text",
            "text": "Describe this image"
        },
        {
            "type": "file",
            "file_url": {
                "url": "https://example.com/image.jpg"
            }
        }
    ],
    # ... other parameters
}
```

## Configuration

### Environment Variables

You can set these environment variables:

```bash
PROMPTSTUDIO_API_KEY=your_api_key
PROMPTSTUDIO_ENV=test  # or prod
```

### Development Setup

For development, install with extra dependencies:

```bash
pip install "promptstudio-sdk[dev]"
```

This includes:

- pytest for testing
- black for formatting
- mypy for type checking
- flake8 for linting

## API Reference

### PromptManager

Main class for interacting with PromptStudio:

```python
class PromptManager:
    def __init__(
        self,
        api_key: str,
        env: str = "prod",
        bypass: bool = False
    )

    async def chat_with_prompt(
        self,
        prompt_id: str,
        request: RequestPayload
    ) -> Dict[str, Any]
```

### Types

```python
from promptstudio.prompt.types import (
    MessageType,
    Memory,
    MessageContent,
    RequestPayload
)
```

## Error Handling

The SDK uses FastAPI's HTTPException for error handling:

```python
try:
    response = await prompt_manager.chat_with_prompt(prompt_id, request)
except HTTPException as e:
    print(f"HTTP Error {e.status_code}: {e.detail}")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@promptstudio.dev or open an issue on GitHub.
