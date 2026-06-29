"""Thin client for the Open Food Facts API.

Used only for barcode-triggered prefill in intake — never as authoritative data.
Falls back gracefully: if the API is down or the product is not found, returns None.
"""

import logging
import httpx

logger = logging.getLogger(__name__)

_BASE = "https://world.openfoodfacts.org/api/v0/product"
_TIMEOUT = 5.0


async def lookup_barcode(gtin: str) -> dict | None:
    """Returns a dict with prefill fields or None if not found / error."""
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            r = await client.get(f"{_BASE}/{gtin}.json")
        if r.status_code != 200:
            return None
        data = r.json()
        if data.get("status") != 1:
            return None
        product = data.get("product", {})
        return {
            "gtin": gtin,
            "display_name": product.get("product_name") or product.get("product_name_es") or "",
            "brand": product.get("brands", "").split(",")[0].strip() or None,
            "category": "FOOD",
        }
    except Exception as exc:
        logger.warning("Open Food Facts lookup failed for %s: %s", gtin, exc)
        return None
