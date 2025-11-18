"""Async Python library for RoboKassa payment gateway."""

from aiorobokassa.client import RoboKassaClient
from aiorobokassa.enums import SignatureAlgorithm
from aiorobokassa.exceptions import (
    APIError,
    ConfigurationError,
    InvalidSignatureAlgorithmError,
    RoboKassaError,
    SignatureError,
    ValidationError,
    XMLParseError,
)

__version__ = "0.1.0"

__all__ = [
    "RoboKassaClient",
    "SignatureAlgorithm",
    "RoboKassaError",
    "APIError",
    "SignatureError",
    "ValidationError",
    "ConfigurationError",
    "InvalidSignatureAlgorithmError",
    "XMLParseError",
]
