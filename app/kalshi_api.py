import reflex as rx
import httpx
import os
import logging


async def get_markets(
    api_key: str,
    status: str = "open",
    limit: int = 20,
    series_ticker: str | None = None,
) -> dict:
    """Fetches markets from the Kalshi API."""
    base_url = "https://demo-api.kalshi.co"
    path = f"/trade-api/v2/markets?status={status}&limit={limit}"
    if series_ticker:
        path += f"&series_ticker={series_ticker}"
    headers = {}
    if api_key and api_key.strip():
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + path, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.exception(f"HTTP error occurred: {e}")
        return {
            "error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        }
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return {"error": str(e)}


async def get_market(api_key: str, market_id: str) -> dict:
    """Fetches a single market from the Kalshi API."""
    base_url = "https://demo-api.kalshi.co"
    path = f"/trade-api/v2/markets/{market_id}"
    headers = {}
    if api_key and api_key.strip():
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url + path, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.exception(f"HTTP error occurred while fetching market {market_id}: {e}")
        return {
            "error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        }
    except Exception as e:
        logging.exception(
            f"An unexpected error occurred while fetching market {market_id}: {e}"
        )
        return {"error": str(e)}