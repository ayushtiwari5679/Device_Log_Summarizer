"""Generate a bar chart from the JSON summary produced by summarizer.py."""
import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")  # Supports headless/CI environments.
import matplotlib.pyplot as plt


def load_summary(path: Path) -> List[Dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"Summary JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Summary JSON must contain a list of device records.")

    validated = []
    for index, row in enumerate(data):
        if not isinstance(row, dict) or "device_id" not in row or "average_temperature" not in row:
            raise ValueError(f"Record {index + 1} must contain device_id and average_temperature.")
        try:
            temperature = float(row["average_temperature"])
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"Record {index + 1} has an invalid average_temperature.") from exc
        if not math.isfinite(temperature):
            raise ValueError(f"Record {index + 1} has a non-finite average_temperature.")
        validated.append({"device_id": str(row["device_id"]), "average_temperature": temperature})
    return validated


def create_chart(json_path: Path, output_path: Path) -> None:
    records = load_summary(json_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5.5), constrained_layout=True)
    if records:
        labels = [record["device_id"] for record in records]
        values = [record["average_temperature"] for record in records]
        bars = ax.bar(labels, values)
        ax.bar_label(bars, fmt="%.1f", padding=3)
        ax.set_ylim(0, max(values) * 1.15 if max(values) > 0 else 1)
        ax.tick_params(axis="x", labelrotation=25)
        for label in ax.get_xticklabels():
            label.set_horizontalalignment("right")
    else:
        ax.text(0.5, 0.5, "No devices passed the temperature filter",
                ha="center", va="center", transform=ax.transAxes)
        ax.set_xticks([])

    ax.set_title("Average Temperature by Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="Chart average device temperatures from summary JSON.")
    parser.add_argument("--input", type=Path, default=Path("output/device_summary.json"))
    parser.add_argument("--output", type=Path, default=Path("output/average_temperature.png"))
    args = parser.parse_args()
    try:
        create_chart(args.input, args.output)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Chart saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
