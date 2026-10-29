# AI Prompt Log

This log records the AI-assisted charting workflow for Section 3. Review it and adjust it to accurately reflect the prompts and checks you personally perform before submission.

## Initial prompt

> Write a Python script that loads `output/device_summary.json` and uses Matplotlib to create a bar chart comparing `average_temperature` for each `device_id`. Include a title and axis labels, save the chart as a PNG, and handle a missing or empty JSON file gracefully.

## Issue found during review

A common first-draft layout issue in a chart with multiple devices is that long device labels overlap or become difficult to read, and the bars may be clipped if the y-axis ends at the maximum value.

## Follow-up prompt

> Improve the chart layout so device labels remain readable and the temperature values are not clipped. Add value labels above bars, rotate and right-align the x-axis labels, leave headroom above the tallest bar, use a clear title and axis labels, and handle an empty list without raising an exception.

## Review and changes applied

- Used `constrained_layout=True` and a wider figure to reduce clipping.
- Rotated and right-aligned device labels.
- Added numeric labels above bars and y-axis headroom.
- Added title, axis labels, a subtle horizontal grid, and an empty-data message.
- Validated the JSON structure and temperature values before plotting.
- Used Matplotlib's non-interactive `Agg` backend so the script also works in headless environments.

## Before submitting

Run `python -m src.chart` and inspect `output/average_temperature.png`. Replace the “common first-draft layout issue” wording with the exact issue you observe if your own first attempt differs. The assessment asks for an honest record of your actual AI prompts and review.
