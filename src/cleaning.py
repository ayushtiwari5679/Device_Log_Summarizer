"""Utilities for cleaning mixed sensor readings."""
from typing import Iterable, List, Any


def clean_sensor_readings(values: Iterable[Any]) -> List[float]:
    """Convert valid readings to floats, discard invalid/negative values, and cap at 500."""
    cleaned: List[float] = []
    if values is None:
        return cleaned

    for value in values:
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            continue

        # Ignore NaN and infinities; they are not meaningful sensor readings.
        if not __import__("math").isfinite(number) or number < 0:
            continue

        cleaned.append(min(number, 500.0))

    return cleaned
