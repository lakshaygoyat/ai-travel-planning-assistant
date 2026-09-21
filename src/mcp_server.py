from __future__ import annotations

from datetime import date
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("travel-live-data")

SINGAPORE_LATITUDE = 1.3521
SINGAPORE_LONGITUDE = 103.8198
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
CURRENCY_URL = "https://api.frankfurter.app/latest"


def _weather_label(code: int) -> str:
    if code == 0:
        return "clear sky"
    if code in {1, 2, 3}:
        return "partly cloudy or overcast"
    if code in {45, 48}:
        return "fog"
    if code in {51, 53, 55, 56, 57}:
        return "drizzle"
    if code in {61, 63, 65, 66, 67, 80, 81, 82}:
        return "rain or showers"
    if code in {71, 73, 75, 77, 85, 86}:
        return "snow"
    if code in {95, 96, 99}:
        return "thunderstorm"
    return "unclassified conditions"


async def fetch_weather(days: int) -> dict[str, Any]:
    safe_days = min(max(days, 1), 7)
    params = {
        "latitude": SINGAPORE_LATITUDE,
        "longitude": SINGAPORE_LONGITUDE,
        "timezone": "Asia/Singapore",
        "forecast_days": safe_days,
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max"
        ),
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(WEATHER_URL, params=params)
        response.raise_for_status()
        payload = response.json()

    daily = payload["daily"]
    forecast = []
    for index, forecast_date in enumerate(daily["time"]):
        code = int(daily["weather_code"][index])
        forecast.append(
            {
                "date": forecast_date,
                "condition": _weather_label(code),
                "weather_code": code,
                "min_c": daily["temperature_2m_min"][index],
                "max_c": daily["temperature_2m_max"][index],
                "rain_probability_percent": daily[
                    "precipitation_probability_max"
                ][index],
            }
        )
    return {
        "status": "success",
        "location": "Singapore",
        "generated_for": date.today().isoformat(),
        "provider": "Open-Meteo",
        "provider_url": "https://open-meteo.com/",
        "forecast": forecast,
    }


async def fetch_currency(amount: float, from_currency: str, to_currency: str) -> dict[str, Any]:
    source = from_currency.upper().strip()
    target = to_currency.upper().strip()
    if amount < 0:
        raise ValueError("Amount must be zero or greater.")
    if len(source) != 3 or len(target) != 3:
        raise ValueError("Currencies must use three-letter ISO codes, for example INR and SGD.")

    params = {"amount": amount, "from": source, "to": target}
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(CURRENCY_URL, params=params)
        response.raise_for_status()
        payload = response.json()

    if target not in payload.get("rates", {}):
        raise RuntimeError("The currency provider did not return the requested conversion.")
    converted = float(payload["rates"][target])
    return {
        "status": "success",
        "amount": amount,
        "from_currency": source,
        "to_currency": target,
        "converted_amount": round(converted, 2),
        "rate": round(converted / amount, 6) if amount else 0,
        "rate_date": payload.get("date"),
        "provider": "Frankfurter (reference rates)",
        "provider_url": "https://frankfurter.app/",
    }


@mcp.tool()
async def get_singapore_weather(days: int = 3) -> dict[str, Any]:
    """Get the current Singapore forecast for 1–7 days from Open-Meteo."""
    try:
        return await fetch_weather(days)
    except Exception as exc:
        return {
            "status": "error",
            "provider": "Open-Meteo",
            "message": f"Weather service unavailable: {type(exc).__name__}",
        }


@mcp.tool()
async def convert_currency(
    amount: float, from_currency: str, to_currency: str
) -> dict[str, Any]:
    """Convert an amount between ISO currencies using recent reference rates."""
    try:
        return await fetch_currency(amount, from_currency, to_currency)
    except Exception as exc:
        return {
            "status": "error",
            "provider": "Frankfurter",
            "message": f"Currency conversion failed: {exc}",
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")
