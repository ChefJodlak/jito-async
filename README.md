# Jito Async SDK

An async Python SDK for interacting with Jito Block Engine.

## Installation

```bash
pip install jito-async
```

Or with Poetry:

```bash
poetry add jito-async
```

## Usage

Here's a simple example of how to use the SDK:

```python
import asyncio
from jito_async import JitoJsonRpcSDK

async def main():
    # Initialize the SDK
    async with JitoJsonRpcSDK("https://your-jito-endpoint.com") as jito:
        # Get tip accounts
        tip_accounts = await jito.get_tip_accounts()
        print(tip_accounts)
        
        # Get a random tip account
        random_account = await jito.get_random_tip_account()
        print(random_account)
        
        # Send a transaction
        txn_result = await jito.send_txn(params={"your": "transaction_data"})
        print(txn_result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- Async/await support
- Context manager for proper resource cleanup
- Type hints for better IDE support
- Proper error handling with custom exceptions
- Support for all Jito Block Engine endpoints:
  - Get tip accounts
  - Get bundle statuses
  - Send bundles
  - Get inflight bundle statuses
  - Send transactions

## Authentication

To use authentication, you can pass an environment variable name that contains your UUID:

```python
jito = JitoJsonRpcSDK("https://your-jito-endpoint.com", uuid_var="JITO_UUID")
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

## License

MIT License