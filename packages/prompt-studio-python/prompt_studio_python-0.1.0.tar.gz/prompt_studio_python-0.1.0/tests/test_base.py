import pytest
from fastapi import HTTPException
from prompt_studio_python.base import Base


@pytest.mark.asyncio
async def test_base_initialization():
    base = Base(api_key="test_key", env="test")
    assert base.api_key == "test_key"
    assert base.env == "test"
    assert base.base_url == "https://api.playground.promptstudio.dev/api/v1"


@pytest.mark.asyncio
async def test_base_prod_url():
    base = Base(api_key="test_key", env="prod")
    assert base.base_url == "https://api.promptstudio.dev/api/v1"


@pytest.mark.asyncio
async def test_invalid_request():
    base = Base(api_key="invalid_key", env="test")
    with pytest.raises(HTTPException):
        await base.request("/invalid_endpoint")
