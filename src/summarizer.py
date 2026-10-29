"""Read device telemetry CSV, aggregate per device, filter, and export JSON."""
import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any


REQUIRED_COLUMNS = {"device_id", "status", "temperature"}


class TelemetryError(Exception):
    """Raised when telemetry input cannot be processed safely."""


def summarize_csv(input_path: Path, output_path: Path, threshold: float = 80.0) -> List[Dict[str, Any]]:
    """Aggregate telemetry by device and export devices whose mean is <= threshold."""
    if not input_path.is_file():
        raise TelemetryError(f"Input CSV file not found: {input_path}")

    totals = defaultdict(lambda: {"record_count": 0, "temperature_sum": 0.0, "error_count": 0})
    try:
        with input_path.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise TelemetryError("CSV is empty or has no header row.")
            missing = REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing:
                raise TelemetryError("CSV is missing required column(s): " + ", ".join(sorted(missing)))

            for line_number, row in enumerate(reader, start=2):
                device_id = (row.get("device_id") or "").strip()
                status = (row.get("status") or "").strip().upper()
                raw_temperature = (row.get("temperature") or "").strip()

                if not device_id:
                    print(f"Warning: skipping row {line_number}: empty device_id.", file=sys.stderr)
                    continue
                try:
                    temperature = float(raw_temperature)
                except (TypeError, ValueError, OverflowError):
                    print(f"Warning: skipping row {line_number}: invalid temperature.", file=sys.stderr)
                    continue
                if not math.isfinite(temperature):
                    print(f"Warning: skipping row {line_number}: non-finite temperature.", file=sys.stderr)
                    continue

                bucket = totals[device_id]
                bucket["record_count"] += 1
                bucket["temperature_sum"] += temperature
                if status == "ERROR":
                    bucket["error_count"] += 1

    except OSError as exc:
        raise TelemetryError(f"Could not read input CSV: {exc}") from exc
    except csv.Error as exc:
        raise TelemetryError(f"Could not parse input CSV: {exc}") from exc

    results = []
    for device_id in sorted(totals):
        stats = totals[device_id]
        average = stats["temperature_sum"] / stats["record_count"]
        if average <= threshold:
            results.append({
                "device_id": device_id,
                "record_count": stats["record_count"],
                "average_temperature": round(average, 2),
                "error_count": stats["error_count"],
            })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(results, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    except OSError as exc:
        raise TelemetryError(f"Could not write output JSON: {exc}") from exc

    return results


def print_summary(results: List[Dict[str, Any]]) -> None:
    """Print a compact fixed-width summary table."""
    headers = ("DEVICE", "RECORDS", "AVG TEMP", "ERRORS")
    rows = [
        (r["device_id"], str(r["record_count"]), f'{r["average_temperature"]:.2f}', str(r["error_count"]))
        for r in results
    ]
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
              for i in range(len(headers))]
    print(" | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("-+-".join("-" * width for width in widths))
    if not rows:
        print("No devices met the temperature threshold.")
        return
    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(len(headers))))


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize device telemetry CSV data.")
    parser.add_argument("--input", type=Path, default=Path("data/device_telemetry.csv"))
    parser.add_argument("--output", type=Path, default=Path("output/device_summary.json"))
    parser.add_argument("--threshold", type=float, default=80.0)
    args = parser.parse_args()

    try:
        results = summarize_csv(args.input, args.output, args.threshold)
    except TelemetryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print_summary(results)
    print(f"\nWrote {len(results)} device summary record(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
