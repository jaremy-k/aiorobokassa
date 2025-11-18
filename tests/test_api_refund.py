"""Tests for RefundMixin."""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch
from xml.etree import ElementTree as ET

from aiorobokassa.enums import SignatureAlgorithm


class TestRefundMixin:
    """Tests for RefundMixin."""

    @pytest.mark.asyncio
    async def test_create_refund_full(self, client):
        """Test creating full refund."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value='<?xml version="1.0"?><Response><Code>0</Code><Description>Success</Description></Response>'
        )
        mock_response.close = MagicMock()

        with patch.object(client, "_post", return_value=mock_response):
            result = await client.create_refund(invoice_id=12345)

            assert result["Code"] == "0"
            assert result["Description"] == "Success"

    @pytest.mark.asyncio
    async def test_create_refund_partial(self, client):
        """Test creating partial refund."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value='<?xml version="1.0"?><Response><Code>0</Code></Response>'
        )
        mock_response.close = MagicMock()

        with patch.object(client, "_post", return_value=mock_response):
            result = await client.create_refund(invoice_id=12345, amount=Decimal("50.25"))

            assert result["Code"] == "0"

    @pytest.mark.asyncio
    async def test_create_refund_xml_structure(self, client):
        """Test that refund XML has correct structure."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value='<?xml version="1.0"?><Response><Code>0</Code></Response>'
        )
        mock_response.close = MagicMock()

        with patch.object(client, "_post", return_value=mock_response) as mock_post:
            await client.create_refund(invoice_id=12345, amount=Decimal("50.25"))

            assert mock_post.called
            call_args = mock_post.call_args
            xml_data = call_args[1]["data"]

            root = ET.fromstring(xml_data)
            assert root.tag == "RefundRequest"
            assert root.find("MerchantLogin").text == client.merchant_login
            assert root.find("InvoiceID").text == "12345"
            assert root.find("Amount").text == "50.25"
            assert root.find("SignatureValue") is not None

    @pytest.mark.asyncio
    async def test_create_refund_without_amount(self, client):
        """Test creating refund without amount (full refund)."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value='<?xml version="1.0"?><Response><Code>0</Code></Response>'
        )
        mock_response.close = MagicMock()

        with patch.object(client, "_post", return_value=mock_response) as mock_post:
            await client.create_refund(invoice_id=12345)

            call_args = mock_post.call_args
            xml_data = call_args[1]["data"]
            root = ET.fromstring(xml_data)

            # Amount should not be present for full refund
            assert root.find("Amount") is None

    @pytest.mark.asyncio
    async def test_get_refund_status(self, client):
        """Test getting refund status."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value='<?xml version="1.0"?><Response><Code>0</Code><State>5</State></Response>'
        )
        mock_response.close = MagicMock()

        with patch.object(client, "_post", return_value=mock_response):
            result = await client.get_refund_status(invoice_id=12345)

            assert result["Code"] == "0"
            assert result["State"] == "5"

    @pytest.mark.asyncio
    async def test_get_refund_status_xml_structure(self, client):
        """Test that refund status XML has correct structure."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value='<?xml version="1.0"?><Response><Code>0</Code></Response>'
        )
        mock_response.close = MagicMock()

        with patch.object(client, "_post", return_value=mock_response) as mock_post:
            await client.get_refund_status(invoice_id=12345)

            assert mock_post.called
            call_args = mock_post.call_args
            xml_data = call_args[1]["data"]

            root = ET.fromstring(xml_data)
            assert root.tag == "RefundStatusRequest"
            assert root.find("MerchantLogin").text == client.merchant_login
            assert root.find("InvoiceID").text == "12345"
            assert root.find("SignatureValue") is not None

    @pytest.mark.asyncio
    async def test_refund_different_algorithms(self, client):
        """Test refund operations with different signature algorithms."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(
            return_value='<?xml version="1.0"?><Response><Code>0</Code></Response>'
        )
        mock_response.close = MagicMock()

        with patch.object(client, "_post", return_value=mock_response) as mock_post:
            await client.create_refund(
                invoice_id=12345, signature_algorithm=SignatureAlgorithm.SHA512
            )

            call_args = mock_post.call_args
            xml_data = call_args[1]["data"]
            root = ET.fromstring(xml_data)
            signature = root.find("SignatureValue").text

            # SHA512 signature should be 128 characters
            assert len(signature) == 128

    @pytest.mark.asyncio
    async def test_create_refund_v2_full(self, client_with_password3):
        """Test creating full refund via v2 API."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "success": True,
                "requestId": "test-request-id-123",
            }
        )
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_post", return_value=mock_response):
            result = await client_with_password3.create_refund_v2(op_key="test-op-key-123")

            assert result.success is True
            assert result.request_id == "test-request-id-123"
            assert result.message is None

    @pytest.mark.asyncio
    async def test_create_refund_v2_partial(self, client_with_password3):
        """Test creating partial refund via v2 API."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "success": True,
                "requestId": "test-request-id-456",
            }
        )
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_post", return_value=mock_response):
            result = await client_with_password3.create_refund_v2(
                op_key="test-op-key-456",
                refund_sum=Decimal("50.25"),
            )

            assert result.success is True
            assert result.request_id == "test-request-id-456"

    @pytest.mark.asyncio
    async def test_create_refund_v2_with_invoice_items(self, client_with_password3):
        """Test creating refund via v2 API with invoice items."""
        from aiorobokassa.models.requests import RefundItem
        from aiorobokassa.enums import TaxRate

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "success": True,
                "requestId": "test-request-id-789",
            }
        )
        mock_response.close = MagicMock()

        refund_items = [
            RefundItem(
                name="Item 1",
                quantity=1,
                cost=50.0,
                tax=TaxRate.VAT20,
            )
        ]

        with patch.object(client_with_password3, "_post", return_value=mock_response):
            result = await client_with_password3.create_refund_v2(
                op_key="test-op-key-789",
                refund_sum=Decimal("50.00"),
                invoice_items=refund_items,
            )

            assert result.success is True
            assert result.request_id == "test-request-id-789"

    @pytest.mark.asyncio
    async def test_create_refund_v2_jwt_structure(self, client_with_password3):
        """Test that refund v2 JWT has correct structure."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True, "requestId": "test-id"})
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_post", return_value=mock_response) as mock_post:
            await client_with_password3.create_refund_v2(
                op_key="test-op-key",
                refund_sum=Decimal("50.00"),
            )

            # Verify POST was called
            assert mock_post.called
            call_args = mock_post.call_args

            # Verify endpoint
            assert "Create" in call_args[0][0]

            # Verify JWT token is sent using json= parameter
            jwt_token = call_args[1]["json"]
            assert isinstance(jwt_token, str)
            assert len(jwt_token.split(".")) == 3  # JWT has 3 parts

    @pytest.mark.asyncio
    async def test_create_refund_v2_error(self, client_with_password3):
        """Test refund v2 creation error handling."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "success": False,
                "message": "Invalid operation key",
            }
        )
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_post", return_value=mock_response):
            from aiorobokassa.exceptions import APIError

            with pytest.raises(APIError, match="Refund creation failed"):
                await client_with_password3.create_refund_v2(op_key="invalid-key")

    @pytest.mark.asyncio
    async def test_create_refund_v2_no_password3(self, client):
        """Test that create_refund_v2 raises error if password3 is not configured."""
        from aiorobokassa.exceptions import ConfigurationError

        with pytest.raises(ConfigurationError, match="password3 is required"):
            await client.create_refund_v2(op_key="test-op-key")

    @pytest.mark.asyncio
    async def test_create_refund_v2_different_algorithms(self, client_with_password3):
        """Test creating refund v2 with different signature algorithms."""
        from aiorobokassa.enums import SignatureAlgorithm

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True, "requestId": "test-id"})
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_post", return_value=mock_response):
            result = await client_with_password3.create_refund_v2(
                op_key="test-op-key",
                signature_algorithm=SignatureAlgorithm.SHA512,
            )

            assert result.success is True

    @pytest.mark.asyncio
    async def test_get_refund_status_v2(self, client_with_password3):
        """Test getting refund status via v2 API."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "requestId": "test-request-id-123",
                "amount": 50.25,
                "label": "finished",
            }
        )
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_get", return_value=mock_response):
            result = await client_with_password3.get_refund_status_v2(
                request_id="test-request-id-123"
            )

            assert result.request_id == "test-request-id-123"
            assert result.amount == Decimal("50.25")
            assert result.label == "finished"
            assert result.message is None

    @pytest.mark.asyncio
    async def test_get_refund_status_v2_processing(self, client_with_password3):
        """Test getting refund status when refund is processing."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "requestId": "test-request-id-456",
                "label": "processing",
            }
        )
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_get", return_value=mock_response):
            result = await client_with_password3.get_refund_status_v2(
                request_id="test-request-id-456"
            )

            assert result.request_id == "test-request-id-456"
            assert result.label == "processing"

    @pytest.mark.asyncio
    async def test_get_refund_status_v2_error(self, client_with_password3):
        """Test refund status v2 error handling."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "message": "Request not found",
            }
        )
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_get", return_value=mock_response):
            from aiorobokassa.exceptions import APIError

            with pytest.raises(APIError, match="Failed to get refund status"):
                await client_with_password3.get_refund_status_v2(request_id="invalid-id")

    @pytest.mark.asyncio
    async def test_get_refund_status_v2_get_request(self, client_with_password3):
        """Test that get_refund_status_v2 uses GET request with correct params."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"requestId": "test-id", "label": "finished"})
        mock_response.close = MagicMock()

        with patch.object(client_with_password3, "_get", return_value=mock_response) as mock_get:
            await client_with_password3.get_refund_status_v2(request_id="test-request-id")

            # Verify GET was called
            assert mock_get.called
            call_args = mock_get.call_args

            # Verify endpoint
            assert "GetState" in call_args[0][0]

            # Verify params
            assert call_args[1]["params"]["id"] == "test-request-id"
