import pytest
from prompt_studio_python.prompt.cache import PromptCache
from prompt_studio_python.prompt.types import MessageType, MessageContent


@pytest.fixture
def cache():
    return PromptCache()


@pytest.mark.asyncio
async def test_cache_initialization(cache):
    await cache.init_cache()
    assert cache.cache is not None


@pytest.mark.asyncio
async def test_save_and_get_cache(cache):
    session_id = "test_session"
    user_message = [MessageContent(type=MessageType.TEXT, text="Test message")]
    response = "Test response"

    await cache.save_to_cache(session_id, user_message, response)
    cached_response = await cache.get_cached_response(session_id)

    assert cached_response is not None
    assert len(cached_response) == 2  # User message and response
    assert cached_response[1].content[0].text == response


@pytest.mark.asyncio
async def test_clear_cache(cache):
    session_id = "test_session"
    user_message = [MessageContent(type=MessageType.TEXT, text="Test message")]
    response = "Test response"

    await cache.save_to_cache(session_id, user_message, response)
    await cache.clear_cache()

    cached_response = await cache.get_cached_response(session_id)
    assert cached_response is None
