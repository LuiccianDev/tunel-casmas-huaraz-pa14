---
name: excel-reader
description: Read Excel (.xlsx, .xls) files and extract data using Python with uv. Use this skill whenever the user mentions spreadsheets, data extraction from Excel, column/row data, or wants to read values from any Excel file. Make sure to use this skill whenever the user mentions Excel files, spreadsheets, data lookup, or needs to extract values from any .xlsx or .xls file, even if they don't explicitly ask for a 'skill'.
---
# Excel Reader Skill

This skill reads Excel (.xlsx and .xls) files and extracts data using Python with **uv** (Astral's fast Python package manager and runtime).

## When to use

- User mentions "Excel file", "spreadsheet", ".xlsx", ".xls"
- User wants to "read", "extract", "get data from" an Excel file
- User mentions specific columns, rows, or data lookup in a spreadsheet
- User needs to convert Excel data to CSV, JSON, or other formats

## What it does

- Reads Excel files using Python with `uv`
- Extracts data from worksheets, rows, and columns
- Supports converting to CSV, JSON, or returning as a table
- Handles multiple sheets within a single workbook

## Usage

```bash
# The skill will be automatically triggered when Claude determines it's appropriate
# based on the description above. No manual invocation needed.
```

## Scripts

This skill bundles a Python script for reading Excel files:

- `scripts/read_excel.py` - Read and extract data from Excel files using `uv` and `openpyxl`/`pandas`

## Example

To read an Excel file and extract data:

```
Input: A path to an Excel file (e.g., "data/sales.xlsx")
Output: Extracted data including sheet names, row data, column headers, and values
```