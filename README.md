# Jito Async SDK

<div align="center">

[![PyPI version](https://badge.fury.io/py/jito-async.svg)](https://badge.fury.io/py/jito-async)
[![Python](https://img.shields.io/pypi/pyversions/jito-async.svg)](https://pypi.org/project/jito-async/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🚀 A modern, async Python SDK for interacting with Jito Block Engine
</div>

## Features

- 🔄 **Full async/await support** with proper resource management
- 🛡️ **Type hints** for better IDE support and code safety
- 🎯 **Simple, intuitive API** for all Block Engine endpoints
- 🔒 **Built-in authentication** via environment variables
- 🐛 **Comprehensive error handling** with custom exceptions
- 📦 **Zero configuration needed** - works out of the box with mainnet

## Installation

```bash
pip install jito-async
```

Or with Poetry (recommended):

```bash
poetry add jito-async
```

## Quick Start

```python
import asyncio
from jito_async import JitoJsonRpcSDK

async def main():
    # Initialize with default mainnet URL
    async with JitoJsonRpcSDK() as jito:
        # Get tip accounts
        tip_accounts = await jito.get_tip_accounts()
        print(f"Found {len(tip_accounts['data']['result'])} tip accounts")
        
        # Get a random tip account
        random_account = await jito.get_random_tip_account()
        print(f"Random tip account: {random_account}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Authentication

To use authentication, pass an environment variable name containing your UUID:

```python
# Set your UUID in environment
import os
os.environ["JITO_AUTH_TOKEN"] = "your-uuid-here"

# Use it in the SDK
jito = JitoJsonRpcSDK(uuid_var="JITO_AUTH_TOKEN")
```

## API Reference

### Initialization

```python
JitoJsonRpcSDK(
    url: Optional[str] = None,  # Defaults to mainnet: https://mainnet.block-engine.jito.wtf
    uuid_var: Optional[str] = None  # Environment variable name for auth token
)
```

### Methods

#### Get Tip Accounts
```python
async def get_tip_accounts() -> Dict:
    """Get tip accounts from the Block Engine."""
```

#### Get Random Tip Account
```python
async def get_random_tip_account() -> Optional[str]:
    """Get a random tip account."""
```

#### Get Bundle Statuses
```python
async def get_bundle_statuses(bundle_uuids: Union[str, List[str]]) -> Dict:
    """Get bundle statuses."""
```

#### Send Bundle
```python
async def send_bundle(params: Any = None) -> Dict:
    """Send a bundle to the Block Engine."""
```

#### Get Inflight Bundle Statuses
```python
async def get_inflight_bundle_statuses(bundle_uuids: Union[str, List[str]]) -> Dict:
    """Get inflight bundle statuses."""
```

#### Send Transaction
```python
async def send_txn(params: Any = None, bundle_only: bool = False) -> Dict:
    """Send a transaction to the Block Engine."""
```

## Error Handling

The SDK provides custom exceptions for better error handling:

```python
from jito_async import JitoError, JitoConnectionError, JitoResponseError

try:
    result = await jito.send_bundle(params={"your": "bundle_data"})
except JitoConnectionError as e:
    print(f"Connection error: {e}")
except JitoResponseError as e:
    print(f"API error: {e}")
except JitoError as e:
    print(f"General error: {e}")
```

## Development

Clone the repository and install dependencies:

```bash
git clone https://github.com/ChefJodlak/jito-async.git
cd jito-async
poetry install
```

Run tests:
```bash
poetry run pytest
```

Format code:
```bash
poetry run black .
poetry run isort .
```

Type check:
```bash
poetry run mypy .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.