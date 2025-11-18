"""Utility functions for aiorobokassa."""

from typing import Dict, Optional
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse


def build_url(base_url: str, params: Dict[str, Optional[str]]) -> str:
    """
    Build URL with query parameters.

    Args:
        base_url: Base URL
        params: Dictionary of query parameters (None values are skipped)

    Returns:
        URL with query string
    """
    # Filter out None values
    filtered_params = {k: str(v) for k, v in params.items() if v is not None}

    if not filtered_params:
        return base_url

    parsed = urlparse(base_url)

    # Parse existing query parameters
    existing_params = parse_qs(parsed.query, keep_blank_values=True)

    # Update with new parameters (convert to list format for urlencode)
    for key, value in filtered_params.items():
        existing_params[key] = [value]

    # Rebuild URL
    new_query_string = urlencode(existing_params, doseq=True)
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query_string,
            parsed.fragment,
        )
    )


def parse_shp_params(params: Dict[str, str]) -> Dict[str, str]:
    """
    Parse Shp_* parameters from request.

    Args:
        params: Dictionary of all parameters

    Returns:
        Dictionary with only Shp_* parameters (with Shp_ prefix removed)
    """
    shp_params = {}
    for key, value in params.items():
        if key.startswith("Shp_"):
            shp_key = key[4:]  # Remove "Shp_" prefix
            shp_params[shp_key] = value
    return shp_params
