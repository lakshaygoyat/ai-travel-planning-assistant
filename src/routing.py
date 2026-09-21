from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class Route:
    use_rag: bool
    use_weather: bool
    use_currency: bool


WEATHER_TERMS = {
    "weather",
    "forecast",
    "rain",
    "rainy",
    "temperature",
    "outdoor",
    "indoor tomorrow",
}
TRAVEL_TERMS = {
    "itinerary",
    "attraction",
    "visit",
    "singapore",
    "family",
    "children",
    "culture",
    "cultural",
    "food",
    "transport",
    "neighbourhood",
    "neighborhood",
    "activity",
    "activities",
}
CURRENCY_AMOUNT_FIRST_PATTERN = re.compile(
    r"(?P<amount>\d[\d,]*(?:\.\d+)?)\s*(?P<source>[A-Za-z]{3})\b.*?(?:to|in|into)\s*(?P<target>[A-Za-z]{3})\b",
    re.IGNORECASE,
)
CURRENCY_CODE_FIRST_PATTERN = re.compile(
    r"(?P<source>[A-Za-z]{3})\s*(?P<amount>\d[\d,]*(?:\.\d+)?)\b.*?(?:to|in|into)\s*(?P<target>[A-Za-z]{3})\b",
    re.IGNORECASE,
)


def classify_request(question: str) -> Route:
    lowered = question.lower()
    has_weather = any(term in lowered for term in WEATHER_TERMS)
    has_currency = bool(
        CURRENCY_AMOUNT_FIRST_PATTERN.search(question)
        or CURRENCY_CODE_FIRST_PATTERN.search(question)
    ) or any(term in lowered for term in ("currency", "exchange rate", "convert"))
    has_travel = any(term in lowered for term in TRAVEL_TERMS)
    # Weather plus activity planning needs destination knowledge; pure forecasts do not.
    use_rag = has_travel or (not has_weather and not has_currency)
    return Route(use_rag=use_rag, use_weather=has_weather, use_currency=has_currency)


def parse_currency(question: str) -> dict[str, Any] | None:
    match = CURRENCY_AMOUNT_FIRST_PATTERN.search(question)
    if not match:
        match = CURRENCY_CODE_FIRST_PATTERN.search(question)
    if not match:
        return None
    return {
        "amount": float(match.group("amount").replace(",", "")),
        "from_currency": match.group("source").upper(),
        "to_currency": match.group("target").upper(),
    }


def infer_forecast_days(question: str) -> int:
    match = re.search(r"\b([1-7])[- ]?day", question.lower())
    if match:
        return int(match.group(1))
    if "week" in question.lower():
        return 7
    return 3
