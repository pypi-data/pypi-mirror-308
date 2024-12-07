# PDF to ICS Calendar Converter

Convert basketball schedule PDFs to ICS calendar files.
## Features

- Converts PDF basketball schedules to ICS calendar format
- Handles various time formats including TBD games
- Automatically sets appropriate time zones (Eastern Time/Indiana)
- Creates calendar events with:
  - Team names and opponents
  - Game locations
  - 2-hour duration for timed games
  - Full-day events for TBD times
- Robust error handling for various PDF formats

## Usage
```bash
pdf2ics <path_to_pdf>
```
### Example
```bash
pdf2ics basketball_schedule.pdf
```
## Requirements
- Python 3.6 or higher
- PDF must contain a table with columns for:
  - Date (MM/DD/YY format)
  - Time
  - Team
  - Opponent
  - Location

## Installation
```bash
pip install pdf2ics
```

