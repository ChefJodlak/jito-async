"""Pytest configuration file."""
import pytest


@pytest.fixture(autouse=True)
def anyio_backend():
    """Configure the anyio backend for pytest-asyncio."""
    return "asyncio" 