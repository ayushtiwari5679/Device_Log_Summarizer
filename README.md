# Device Log Summarizer CLI

A small Python CLI project for the Software Engineering Intern assessment. It cleans mixed sensor readings, aggregates device telemetry from CSV, exports JSON, and creates a Matplotlib bar chart.

## Requirements

- Python 3.9+
- `matplotlib` (only needed for chart generation)

## Project layout

```text
device_log_summarizer/
├── data/
│   └── device_telemetry.csv
├── output/
│   ├── device_summary.json
│   └── average_temperature.png
├── src/
│   ├── cleaning.py
│   ├── summarizer.py
│   └── chart.py
├── tests/
│   ├── test_cleaning.py
│   └── test_summarizer.py
├── PROMPT_LOG.md
├── requirements.txt
└── README.md
```

## Setup (Windows PowerShell)

```powershell
cd device_log_summarizer
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` in place of `python`, or activate the environment using Command Prompt's `.venv\Scripts\activate.bat`.

## Run the assessment

From the project root:

```powershell
python -m src.summarizer --input data/device_telemetry.csv --output output/device_summary.json
python -m src.chart --input output/device_summary.json --output output/average_temperature.png
```

Optional threshold override:

```powershell
python -m src.summarizer --threshold 75
```

The filter keeps devices whose average temperature is **less than or equal to 80.0°C** by default. A device with average above 80.0°C is excluded.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Section 1: cleaning function

`src/cleaning.py` defines `clean_sensor_readings(values)`. It converts values to floats when possible, drops `None`, invalid values, negative readings, NaN, and infinities, then caps values above 500 at 500. Empty or fully invalid inputs return an empty list.

## Section 2: aggregation rules

- Required CSV columns: `device_id`, `status`, `temperature`.
- Rows with blank device IDs, invalid temperatures, or non-finite temperatures are skipped with a warning.
- Record count and ERROR count include only rows with valid temperatures and non-empty device IDs.
- Status matching is case-insensitive after trimming whitespace.
- Results are sorted by device ID for stable output.
- JSON output includes `device_id`, `record_count`, `average_temperature`, and `error_count`.

## Error handling

The CLI prints a clear error and exits with status code 1 if the input file is missing, required columns are absent, or input/output cannot be read/written. Malformed individual data rows are skipped rather than crashing the run.

## Submission checklist

1. Run the scripts and tests from the project root.
2. Confirm `output/device_summary.json` and `output/average_temperature.png` exist.
3. Keep `PROMPT_LOG.md` and this README in the submission.
4. Push the project to a GitHub repository, or ZIP the folder.
5. Include the repository URL in your submission form/email if required.

Do not commit the `.venv` folder. If you add a `.gitignore`, include `.venv/`, `__pycache__/`, and `*.pyc`.
