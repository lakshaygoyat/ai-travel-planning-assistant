from src.routing import classify_request, infer_forecast_days, parse_currency


def test_destination_question_uses_only_rag() -> None:
    route = classify_request("What are the must-visit attractions in Singapore?")
    assert route.use_rag is True
    assert route.use_weather is False
    assert route.use_currency is False


def test_weather_question_uses_only_weather() -> None:
    route = classify_request("What is the weather forecast for three days?")
    assert route.use_rag is False
    assert route.use_weather is True


def test_combined_question_uses_rag_and_weather() -> None:
    route = classify_request("Plan a three-day Singapore itinerary adjusted for rain.")
    assert route.use_rag is True
    assert route.use_weather is True


def test_currency_parsing() -> None:
    expected = {
        "amount": 50000.0,
        "from_currency": "INR",
        "to_currency": "SGD",
    }
    assert parse_currency("Convert INR 50,000 to SGD") == expected
    assert parse_currency("Convert 50,000 INR to SGD") == expected


def test_forecast_days() -> None:
    assert infer_forecast_days("Give me a 5-day forecast") == 5
    assert infer_forecast_days("Plan for next week") == 7
