import csv
import json
import tempfile
import unittest
from pathlib import Path

from src.summarizer import summarize_csv, TelemetryError


class SummarizerTests(unittest.TestCase):
    def test_aggregation_filter_and_json_export(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_path = root / "input.csv"
            output_path = root / "output.json"
            rows = [
                ["DEV_A", "ACTIVE", "40"],
                ["DEV_A", "ERROR", "60"],
                ["DEV_B", "WARNING", "90"],
                ["DEV_B", "ERROR", "100"],
                ["DEV_C", "ERROR", "bad"],
                ["DEV_C", "ACTIVE", "50"],
            ]
            with input_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["device_id", "status", "temperature"])
                writer.writerows(rows)

            result = summarize_csv(input_path, output_path)
            self.assertEqual(result, [
                {"device_id": "DEV_A", "record_count": 2, "average_temperature": 50.0, "error_count": 1},
                {"device_id": "DEV_C", "record_count": 1, "average_temperature": 50.0, "error_count": 0},
            ])
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), result)

    def test_missing_file_raises_helpful_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(TelemetryError, "not found"):
                summarize_csv(Path(temp_dir) / "missing.csv", Path(temp_dir) / "out.json")


if __name__ == "__main__":
    unittest.main()
