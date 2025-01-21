"""Jito Block Engine Async SDK.

This module provides an async client for interacting with Jito Block Engine.
"""
from __future__ import annotations

import os
import random
from typing import Any, Dict, List, Optional, Union

import aiohttp
from aiohttp import ClientSession


DEFAULT_BLOCK_ENGINE_URL = "https://mainnet.block-engine.jito.wtf"


class JitoError(Exception):
    """Base exception for Jito SDK errors."""
    pass


class JitoConnectionError(JitoError):
    """Raised when there are connection issues."""
    pass


class JitoResponseError(JitoError):
    """Raised when the API returns an error response."""
    pass


class JitoJsonRpcSDK:
    """Async client for interacting with Jito Block Engine."""

    def __init__(self, url: Optional[str] = None, uuid_var: Optional[str] = None) -> None:
        """Initialize the Jito Block Engine client.
        
        Args:
            url: The base URL for the Block Engine API. Defaults to mainnet Block Engine.
            uuid_var: Optional environment variable name containing the UUID for authentication.
        """
        self.url = (url or DEFAULT_BLOCK_ENGINE_URL).rstrip('/')
        self.uuid_var = self.__get_uuid(uuid_var) if uuid_var else None
        self.session: Optional[ClientSession] = None

    def __get_uuid(self, uuid_var: str) -> Optional[str]:
        """Get UUID from environment variable."""
        return os.getenv(uuid_var)

    async def __ensure_session(self) -> ClientSession:
        """Ensure we have an active session."""
        if self.session is None or self.session.closed:
            self.session = ClientSession()
        return self.session

    async def __close_session(self) -> None:
        """Close the session if it exists."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def __send_request(self, endpoint: str, method: str, params: Any = None) -> Dict:
        """Send a request to the Block Engine using JSON-RPC.
        
        Args:
            endpoint: API endpoint path.
            method: JSON-RPC method name.
            params: Optional parameters for the method.

        Returns:
            Dict containing the response data or error information.

        Raises:
            JitoConnectionError: If there are connection issues.
            JitoResponseError: If the API returns an error response.
        """
        if not endpoint:
            raise ValueError("Please enter a valid endpoint.")

        headers = {
            'Content-Type': 'application/json',
            "accept": "application/json"
        }

        if self.uuid_var:
            headers["x-jito-auth"] = self.uuid_var

        data = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": method,
            "params": [params] if params is not None else []
        }

        session = await self.__ensure_session()

        try:
            async with session.post(f"{self.url}{endpoint}", headers=headers, json=data) as response:
                await response.raise_for_status()
                result = await response.json()
                return {"success": True, "data": result}

        except aiohttp.ClientResponseError as e:
            raise JitoResponseError(f"HTTP Error: {e.status} - {e.message}")
        except aiohttp.ClientConnectionError as e:
            raise JitoConnectionError(f"Connection Error: {str(e)}")
        except aiohttp.ClientError as e:
            raise JitoError(f"Client Error: {str(e)}")
        except Exception as e:
            raise JitoError(f"An unexpected error occurred: {str(e)}")
        finally:
            if not self.session or self.session.closed:
                await self.__close_session()

    async def get_tip_accounts(self) -> Dict:
        """Get tip accounts from the Block Engine.
        
        Returns:
            Dict containing the tip accounts information.
        """
        endpoint = "/bundles"
        if self.uuid_var:
            endpoint += f"?uuid={self.uuid_var}"
        return await self.__send_request(endpoint=endpoint, method="getTipAccounts")

    async def get_random_tip_account(self) -> Optional[str]:
        """Get a random tip account.
        
        Returns:
            A randomly selected tip account or None if no accounts are available.
        """
        try:
            response = await self.get_tip_accounts()
            tip_accounts = response['data']['result']
            return random.choice(tip_accounts) if tip_accounts else None
        except (KeyError, IndexError):
            return None

    async def get_bundle_statuses(self, bundle_uuids: Union[str, List[str]]) -> Dict:
        """Get bundle statuses.
        
        Args:
            bundle_uuids: Single UUID or list of UUIDs to check status for.

        Returns:
            Dict containing the bundle statuses.
        """
        endpoint = "/bundles"
        if self.uuid_var:
            endpoint += f"?uuid={self.uuid_var}"

        bundle_uuids_list = [bundle_uuids] if isinstance(bundle_uuids, str) else bundle_uuids
        return await self.__send_request(endpoint=endpoint, method="getBundleStatuses", params=bundle_uuids_list)

    async def send_bundle(self, params: Any = None) -> Dict:
        """Send a bundle to the Block Engine.
        
        Args:
            params: Bundle parameters.

        Returns:
            Dict containing the response from sending the bundle.
        """
        endpoint = "/bundles"
        if self.uuid_var:
            endpoint += f"?uuid={self.uuid_var}"
        return await self.__send_request(endpoint=endpoint, method="sendBundle", params=params)

    async def get_inflight_bundle_statuses(self, bundle_uuids: Union[str, List[str]]) -> Dict:
        """Get inflight bundle statuses.
        
        Args:
            bundle_uuids: Single UUID or list of UUIDs to check status for.

        Returns:
            Dict containing the inflight bundle statuses.
        """
        endpoint = "/bundles"
        if self.uuid_var:
            endpoint += f"?uuid={self.uuid_var}"

        bundle_uuids_list = [bundle_uuids] if isinstance(bundle_uuids, str) else bundle_uuids
        return await self.__send_request(endpoint=endpoint, method="getInflightBundleStatuses", params=bundle_uuids_list)

    async def send_txn(self, params: Any = None, bundle_only: bool = False) -> Dict:
        """Send a transaction to the Block Engine.
        
        Args:
            params: Transaction parameters.
            bundle_only: Whether to only create a bundle without submitting.

        Returns:
            Dict containing the response from sending the transaction.
        """
        ep = "/transactions"
        query_params = []

        if bundle_only:
            query_params.append("bundleOnly=true")

        if self.uuid_var:
            query_params.append(f"uuid={self.uuid_var}")

        if query_params:
            ep += "?" + "&".join(query_params)

        return await self.__send_request(endpoint=ep, method="sendTransaction", params=params)

    async def __aenter__(self) -> 'JitoJsonRpcSDK':
        """Async context manager entry."""
        await self.__ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.__close_session() 