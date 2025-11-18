"""Pydantic models for request/response validation."""

from decimal import Decimal
from typing import Dict, Optional

from pydantic import BaseModel, Field, field_validator


class PaymentRequest(BaseModel):
    """Model for payment link generation."""

    out_sum: Decimal = Field(..., description="Payment amount")
    description: str = Field(..., description="Payment description")
    inv_id: Optional[int] = Field(None, description="Invoice ID (optional)")
    email: Optional[str] = Field(None, description="Customer email")
    culture: Optional[str] = Field("ru", description="Language (ru, en)")
    encoding: Optional[str] = Field("utf-8", description="Encoding")
    is_test: Optional[int] = Field(None, description="Test mode flag (1 for test)")
    expiration_date: Optional[str] = Field(None, description="Payment expiration date")
    user_parameters: Optional[Dict[str, str]] = Field(
        None, description="Additional user parameters"
    )

    @field_validator("out_sum")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate payment amount is positive."""
        if v <= 0:
            raise ValueError("Payment amount must be positive")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Validate description is not empty."""
        if not v.strip():
            raise ValueError("Description cannot be empty")
        return v


class ResultURLNotification(BaseModel):
    """Model for ResultURL notification from RoboKassa."""

    out_sum: str = Field(..., description="Payment amount")
    inv_id: str = Field(..., description="Invoice ID")
    signature_value: str = Field(..., alias="SignatureValue", description="Signature")
    shp_params: Optional[Dict[str, str]] = Field(None, description="Additional parameters")

    class Config:
        populate_by_name = True


class SuccessURLNotification(BaseModel):
    """Model for SuccessURL redirect from RoboKassa."""

    out_sum: str = Field(..., description="Payment amount")
    inv_id: str = Field(..., description="Invoice ID")
    signature_value: str = Field(..., alias="SignatureValue", description="Signature")
    shp_params: Optional[Dict[str, str]] = Field(None, description="Additional parameters")

    class Config:
        populate_by_name = True


class InvoiceRequest(BaseModel):
    """Model for invoice creation via XML API."""

    merchant_login: str = Field(..., description="Merchant login")
    out_sum: Decimal = Field(..., description="Payment amount")
    description: str = Field(..., description="Payment description")
    inv_id: Optional[int] = Field(None, description="Invoice ID")
    email: Optional[str] = Field(None, description="Customer email")
    expiration_date: Optional[str] = Field(None, description="Payment expiration date")
    user_parameters: Optional[Dict[str, str]] = Field(None, description="Additional parameters")

    @field_validator("out_sum")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate payment amount is positive."""
        if v <= 0:
            raise ValueError("Payment amount must be positive")
        return v


class RefundRequest(BaseModel):
    """Model for refund request."""

    invoice_id: int = Field(..., description="Invoice ID to refund")
    amount: Optional[Decimal] = Field(None, description="Refund amount (full if not specified)")

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Validate refund amount is positive if specified."""
        if v is not None and v <= 0:
            raise ValueError("Refund amount must be positive")
        return v
