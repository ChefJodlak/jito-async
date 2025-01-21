"""Tests for the Jito Block Engine SDK."""
import os
from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import ClientResponseError, ClientSession

from jito_async import JitoConnectionError, JitoJsonRpcSDK, JitoResponseError


@pytest.fixture
async def sdk():
    """Create a SDK instance for testing."""
    async with JitoJsonRpcSDK("https://test-url.com") as sdk:
        yield sdk


@pytest.mark.asyncio
async def test_get_tip_accounts(sdk):
    """Test getting tip accounts."""
    mock_response = {"result": ["account1", "account2"]}
    
    with patch.object(ClientSession, 'post') as mock_post:
        mock_post.return_value.__aenter__.return_value.json = AsyncMock(
            return_value=mock_response
        )
        mock_post.return_value.__aenter__.return_value.raise_for_status = AsyncMock()
        
        result = await sdk.get_tip_accounts()
        assert result["success"] is True
        assert result["data"] == mock_response


@pytest.mark.asyncio
async def test_get_random_tip_account(sdk):
    """Test getting a random tip account."""
    mock_response = {"result": ["account1", "account2"]}
    
    with patch.object(ClientSession, 'post') as mock_post:
        mock_post.return_value.__aenter__.return_value.json = AsyncMock(
            return_value=mock_response
        )
        mock_post.return_value.__aenter__.return_value.raise_for_status = AsyncMock()
        
        result = await sdk.get_random_tip_account()
        assert result in mock_response["result"]


@pytest.mark.asyncio
async def test_send_bundle(sdk):
    """Test sending a bundle."""
    mock_response = {"result": "success"}
    test_params = {"test": "data"}
    
    with patch.object(ClientSession, 'post') as mock_post:
        mock_post.return_value.__aenter__.return_value.json = AsyncMock(
            return_value=mock_response
        )
        mock_post.return_value.__aenter__.return_value.raise_for_status = AsyncMock()
        
        result = await sdk.send_bundle(params=test_params)
        assert result["success"] is True
        assert result["data"] == mock_response


@pytest.mark.asyncio
async def test_error_handling(sdk):
    """Test error handling."""
    with patch.object(ClientSession, 'post') as mock_post:
        mock_post.return_value.__aenter__.return_value.raise_for_status = AsyncMock(
            side_effect=ClientResponseError(None, None, status=400, message="Bad Request")
        )
        mock_post.return_value.__aenter__.return_value.json = AsyncMock()
        
        with pytest.raises(JitoResponseError):
            await sdk.get_tip_accounts()


@pytest.mark.asyncio
async def test_context_manager():
    """Test context manager functionality."""
    async with JitoJsonRpcSDK("https://test-url.com") as sdk:
        assert isinstance(sdk, JitoJsonRpcSDK)
        assert sdk.session is not None
        
    assert sdk.session.closed is True


def test_uuid_from_env():
    """Test UUID from environment variable."""
    test_uuid = "test-uuid"
    os.environ["TEST_UUID"] = test_uuid
    
    sdk = JitoJsonRpcSDK("https://test-url.com", uuid_var="TEST_UUID")
    assert sdk.uuid_var == test_uuid 