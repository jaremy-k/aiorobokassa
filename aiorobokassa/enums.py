"""Enums for RoboKassa API."""

from enum import Enum


class SignatureAlgorithm(str, Enum):
    """Supported signature algorithms."""

    MD5 = "MD5"
    SHA256 = "SHA256"
    SHA512 = "SHA512"

    @classmethod
    def from_string(cls, value: str) -> "SignatureAlgorithm":
        """Convert string to enum, case-insensitive."""
        value_upper = value.upper()
        for alg in cls:
            if alg.value == value_upper:
                return alg
        raise ValueError(
            f"Unsupported algorithm: {value}. Supported: {', '.join(a.value for a in cls)}"
        )


class Culture(str, Enum):
    """Supported languages."""

    RU = "ru"
    EN = "en"
