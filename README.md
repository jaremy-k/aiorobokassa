# aiorobokassa

Async Python library for RoboKassa payment gateway integration.

## Features

- ✅ Async/await support with `aiohttp`
- ✅ Payment link generation
- ✅ Notification handling (ResultURL, SuccessURL)
- ✅ Invoice creation via XML API
- ✅ Refund operations
- ✅ Signature verification (MD5, SHA256, SHA512)
- ✅ Type hints and Pydantic validation
- ✅ Test mode support
- ✅ Clean architecture (SOLID, DRY, KISS)

## Installation

```bash
pip install aiorobokassa
```

## Quick Start

### Basic Payment Link Generation

```python
import asyncio
from decimal import Decimal
from aiorobokassa import RoboKassaClient

async def main():
    # Initialize client
    client = RoboKassaClient(
        merchant_login="your_merchant_login",
        password1="password1",
        password2="password2",
        test_mode=True,  # Use test mode for development
    )

    # Create payment URL
    payment_url = await client.create_payment_url(
        out_sum=Decimal("100.00"),
        description="Test payment",
        inv_id=123,
        email="customer@example.com",
    )

    print(f"Payment URL: {payment_url}")

    # Close client session
    await client.close()

asyncio.run(main())
```

### Using Context Manager

```python
import asyncio
from decimal import Decimal
from aiorobokassa import RoboKassaClient

async def main():
    async with RoboKassaClient(
        merchant_login="your_merchant_login",
        password1="password1",
        password2="password2",
        test_mode=True,
    ) as client:
        payment_url = await client.create_payment_url(
            out_sum=Decimal("100.00"),
            description="Test payment",
        )
        print(f"Payment URL: {payment_url}")

asyncio.run(main())
```

### Handling Notifications

#### ResultURL (Server-to-Server Notification)

```python
from aiorobokassa import RoboKassaClient, SignatureError

# In your web framework (FastAPI, Django, etc.)
async def handle_result_url(request_params: dict):
    client = RoboKassaClient(
        merchant_login="your_merchant_login",
        password1="password1",
        password2="password2",
    )

    # Parse parameters
    params = client.parse_result_url_params(request_params)

    try:
        # Verify signature
        client.verify_result_url(
            out_sum=params["out_sum"],
            inv_id=params["inv_id"],
            signature_value=params["signature_value"],
            shp_params=params.get("shp_params"),
        )

        # Payment is valid, update order status
        invoice_id = params["inv_id"]
        amount = params["out_sum"]
        # ... update your database

        return "OK" + invoice_id  # RoboKassa expects this response
    except SignatureError:
        # Invalid signature, reject payment
        return "ERROR"
```

#### SuccessURL (User Redirect)

```python
from aiorobokassa import RoboKassaClient, SignatureError

async def handle_success_url(request_params: dict):
    client = RoboKassaClient(
        merchant_login="your_merchant_login",
        password1="password1",
        password2="password2",
    )

    params = client.parse_success_url_params(request_params)

    try:
        client.verify_success_url(
            out_sum=params["out_sum"],
            inv_id=params["inv_id"],
            signature_value=params["signature_value"],
        )

        # Show success page to user
        return "Payment successful!"
    except SignatureError:
        return "Payment verification failed"
```

### Creating Invoice via XML API

```python
import asyncio
from decimal import Decimal
from aiorobokassa import RoboKassaClient

async def main():
    async with RoboKassaClient(
        merchant_login="your_merchant_login",
        password1="password1",
        password2="password2",
        test_mode=True,
    ) as client:
        result = await client.create_invoice(
            out_sum=Decimal("100.00"),
            description="Invoice payment",
            inv_id=123,
            email="customer@example.com",
        )

        print(f"Invoice created: {result}")

asyncio.run(main())
```

### Refunds

```python
import asyncio
from decimal import Decimal
from aiorobokassa import RoboKassaClient

async def main():
    async with RoboKassaClient(
        merchant_login="your_merchant_login",
        password1="password1",
        password2="password2",
        test_mode=True,
    ) as client:
        # Create full refund
        refund_result = await client.create_refund(
            invoice_id=123,
        )

        # Or partial refund
        partial_refund = await client.create_refund(
            invoice_id=123,
            amount=Decimal("50.00"),
        )

        # Check refund status
        status = await client.get_refund_status(
            invoice_id=123,
        )

        print(f"Refund status: {status}")

asyncio.run(main())
```

## API Reference

### RoboKassaClient

Main client class for RoboKassa API.

```python
RoboKassaClient(
    merchant_login: str,
    password1: str,
    password2: str,
    test_mode: bool = False,
    session: Optional[aiohttp.ClientSession] = None,
    timeout: aiohttp.ClientTimeout = None,
)
```

**Parameters:**

- `merchant_login`: Your RoboKassa merchant login
- `password1`: Password #1 for signature calculation
- `password2`: Password #2 for ResultURL verification
- `test_mode`: Enable test mode (default: False)
- `session`: Optional aiohttp session (auto-created if not provided)
- `timeout`: Optional timeout for requests

### Methods

#### `create_payment_url()`

Generate payment URL for redirecting user to RoboKassa.

```python
async client.create_payment_url(
    out_sum: Decimal,
    description: str,
    inv_id: Optional[int] = None,
    email: Optional[str] = None,
    culture: Optional[str] = None,
    encoding: Optional[str] = None,
    is_test: Optional[int] = None,
    expiration_date: Optional[str] = None,
    user_parameters: Optional[Dict[str, str]] = None,
    signature_algorithm: str = "MD5",
) -> str
```

#### `verify_result_url()`

Verify ResultURL notification signature.

```python
client.verify_result_url(
    out_sum: str,
    inv_id: str,
    signature_value: str,
    shp_params: Optional[Dict[str, str]] = None,
    signature_algorithm: str = "MD5",
) -> bool
```

#### `verify_success_url()`

Verify SuccessURL redirect signature.

```python
client.verify_success_url(
    out_sum: str,
    inv_id: str,
    signature_value: str,
    shp_params: Optional[Dict[str, str]] = None,
    signature_algorithm: str = "MD5",
) -> bool
```

#### `parse_result_url_params()`

Parse ResultURL parameters from request (static method).

```python
RoboKassaClient.parse_result_url_params(params: Dict[str, str]) -> Dict[str, str]
```

#### `parse_success_url_params()`

Parse SuccessURL parameters from request (static method).

```python
RoboKassaClient.parse_success_url_params(params: Dict[str, str]) -> Dict[str, str]
```

#### `create_invoice()`

Create invoice via XML API.

```python
async client.create_invoice(
    out_sum: Decimal,
    description: str,
    inv_id: Optional[int] = None,
    email: Optional[str] = None,
    expiration_date: Optional[str] = None,
    user_parameters: Optional[Dict[str, str]] = None,
    signature_algorithm: str = "MD5",
) -> Dict[str, str]
```

#### `create_refund()`

Create refund for invoice.

```python
async client.create_refund(
    invoice_id: int,
    amount: Optional[Decimal] = None,
    signature_algorithm: str = "MD5",
) -> Dict[str, str]
```

#### `get_refund_status()`

Get refund status for invoice.

```python
async client.get_refund_status(
    invoice_id: int,
    signature_algorithm: str = "MD5",
) -> Dict[str, str]
```

## Exceptions

- `RoboKassaError`: Base exception for all errors
- `SignatureError`: Signature verification failed
- `APIError`: API request failed
- `ValidationError`: Data validation failed
- `ConfigurationError`: Client configuration is invalid

## Requirements

- Python 3.8+
- aiohttp >= 3.8.0
- pydantic >= 2.0.0

## License

MIT License

## Documentation

For more information about RoboKassa API, visit [official documentation](https://docs.robokassa.ru/).
