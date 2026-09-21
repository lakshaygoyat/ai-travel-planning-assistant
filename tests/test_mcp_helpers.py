from src.mcp_server import _weather_label


def test_weather_code_mapping() -> None:
    assert _weather_label(0) == "clear sky"
    assert _weather_label(63) == "rain or showers"
    assert _weather_label(95) == "thunderstorm"
