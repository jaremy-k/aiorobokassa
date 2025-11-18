Refund Operations
==================

This guide explains how to process refunds for payments.

Full Refund
-----------

Create a full refund for an invoice:

.. code-block:: python

   from aiorobokassa import RoboKassaClient

   async with RoboKassaClient(
       merchant_login="your_merchant_login",
       password1="password1",
       password2="password2",
   ) as client:
       result = await client.create_refund(
           invoice_id=12345,
       )
       
       print(f"Refund result: {result}")

Partial Refund
--------------

Create a partial refund by specifying the amount:

.. code-block:: python

   from decimal import Decimal

   result = await client.create_refund(
       invoice_id=12345,
       amount=Decimal("50.00"),  # Refund only 50.00
   )

Check Refund Status
-------------------

Get the status of a refund:

.. code-block:: python

   status = await client.get_refund_status(
       invoice_id=12345,
   )
   
   print(f"Refund status: {status}")

Response Format
---------------

Refund operations return a dictionary with response data:

.. code-block:: python

   {
       "Code": "0",  # 0 = success
       "Description": "Refund processed",
       "State": "5",  # Refund state code
       # ... other fields
   }

Refund States
-------------

Common refund state codes:

- ``5`` - Refund processed successfully
- Other codes indicate different states (check RoboKassa documentation)

Error Handling
--------------

Handle errors when processing refunds:

.. code-block:: python

   from aiorobokassa import APIError

   try:
       result = await client.create_refund(
           invoice_id=12345,
           amount=Decimal("50.00"),
       )
   except APIError as e:
       print(f"Refund failed: {e.status_code} - {e.response}")

Refund API v2 (JWT-based)
--------------------------

The modern Refund API uses JWT tokens and provides better error handling and response models.

**Important:** Refund API v2 requires ``password3`` to be configured when initializing the client.

Create Refund v2
~~~~~~~~~~~~~~~~

Create a refund using the modern API:

.. code-block:: python

   from decimal import Decimal
   from aiorobokassa import RoboKassaClient

   async with RoboKassaClient(
       merchant_login="your_merchant_login",
       password1="password1",
       password2="password2",
       password3="password3",  # Required for refund v2
   ) as client:
       # Full refund
       refund = await client.create_refund_v2(
           op_key="operation_key_from_payment",
       )
       
       print(f"Refund request ID: {refund.request_id}")

Partial Refund v2
~~~~~~~~~~~~~~~~~

Create a partial refund by specifying the amount:

.. code-block:: python

   refund = await client.create_refund_v2(
       op_key="operation_key_from_payment",
       refund_sum=Decimal("50.00"),  # Partial refund amount
   )

Refund with Invoice Items
~~~~~~~~~~~~~~~~~~~~~~~~~~

Specify which invoice items to refund:

.. code-block:: python

   from aiorobokassa.models.requests import RefundItem
   from aiorobokassa.enums import TaxRate

   refund_items = [
       RefundItem(
           name="Item 1",
           quantity=1,
           cost=50.0,
           tax=TaxRate.VAT20,
       )
   ]

   refund = await client.create_refund_v2(
       op_key="operation_key_from_payment",
       refund_sum=Decimal("50.00"),
       invoice_items=refund_items,
   )

Get Refund Status v2
~~~~~~~~~~~~~~~~~~~~~

Get the status of a refund created via v2 API:

.. code-block:: python

   refund_status = await client.get_refund_status_v2(
       request_id=refund.request_id,
   )
   
   print(f"Refund status: {refund_status.label}")
   print(f"Refund amount: {refund_status.amount}")

Refund Status Labels
~~~~~~~~~~~~~~~~~~~~~

Common refund status labels:

- ``finished`` - Refund completed successfully
- ``processing`` - Refund is being processed
- ``canceled`` - Refund was canceled

Response Models
~~~~~~~~~~~~~~~

Refund v2 API returns Pydantic models:

.. code-block:: python

   # RefundCreateResponse
   {
       "success": True,
       "request_id": "guid-string",
       "message": None
   }

   # RefundStatusResponse
   {
       "request_id": "guid-string",
       "amount": Decimal("50.00"),
       "label": "finished",
       "message": None
   }

Error Handling v2
~~~~~~~~~~~~~~~~~

Handle errors when using refund v2 API:

.. code-block:: python

   from aiorobokassa import APIError, ConfigurationError

   try:
       refund = await client.create_refund_v2(
           op_key="operation_key",
       )
   except ConfigurationError:
       print("password3 is required for refund v2 operations")
   except APIError as e:
       print(f"Refund failed: {e}")

Best Practices
--------------

1. **Always verify invoice exists** before creating refund
2. **Check refund status** after creation to confirm processing
3. **Handle partial refunds carefully** - ensure amount doesn't exceed original payment
4. **Log all refund operations** for audit purposes
5. **Update your database** after successful refund
6. **Use refund v2 API** for new integrations - it provides better error handling and response models
7. **Store operation keys** from payments to use for refunds

