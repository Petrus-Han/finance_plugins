# Employee Roster Plugin

Manage employee roster data with finance department mappings, using Google Sheets as backend storage.

## Overview

This plugin helps finance teams maintain an employee roster with department categorization. It stores employee records in Google Sheets and provides tools for querying, importing, and mapping departments.

## Tools

### 1. Query Employee Roster

Search for employees by name or email with fuzzy matching.

**Parameters:**
- `query` (required): Employee name or email to search for (partial match supported)

**Returns:** Matching employee records with finance department assignment, job title, employment type, and status.

### 2. Import Roster from CSV

Batch import employee data from CSV exports. Supports smart column mapping for common HR system export formats, deduplication by employee ID and email, and preserves manually edited fields (`finance_department`, `notes`).

**Parameters:**
- `csv_content` (required): CSV text content with header row
- `source` (required): Source system identifier (`feishu` or `deel`)
- `dry_run` (optional): Preview changes without writing (default: false)

**Returns:** Summary of records added, updated, skipped, and any errors.

### 3. Get Department Mapping

View or filter the mapping table from source departments to finance departments.

**Parameters:**
- `source_department` (optional): Filter by department name (fuzzy match)

**Returns:** List of department mappings with source system info.

## Authentication

Two methods supported (configure one):

**OAuth2** — Users authorize via Google login. Requires OAuth Client ID and Client Secret from Google Cloud Console.

**Service Account** — For automated/headless use. Requires a GCP Service Account JSON key. Share the spreadsheet with the service account email.

## Setup

1. **Create a Google Spreadsheet** — The plugin auto-initializes three sheets on first use:
   - `Roster` — Employee records (name, email, department, job title, etc.)
   - `Department_Mapping` — Source department to finance department mappings
   - `Sync_Log` — Import audit trail

2. **Enable Google Sheets API** in [Google Cloud Console](https://console.cloud.google.com/)

3. **Configure credentials** — Set up OAuth Client or Service Account (see Authentication above)

4. **Install the plugin** in Dify and enter:
   - **Spreadsheet ID** (from the URL: `https://docs.google.com/spreadsheets/d/{ID}/edit`)
   - OAuth credentials or Service Account JSON

## Usage

```yaml
# Search for an employee
Tool: Query Employee Roster
  query: "jane.doe@company.com"

# Preview a CSV import
Tool: Import Roster from CSV
  csv_content: "<CSV text>"
  source: "deel"
  dry_run: true

# Look up department mappings
Tool: Get Department Mapping
  source_department: "Engineering"
```
