# Employee Roster Plugin

Employee Roster plugin for Dify - Manage employee roster data with finance department mappings using Google Sheets as a backend.

## Overview

This plugin provides tools to manage an employee roster stored in Google Sheets, designed for finance teams that need to categorize employees by finance department. It supports importing employee data from Feishu and Deel CSV exports, querying employees by name or email, and viewing department-to-finance-department mappings.

Key capabilities:
- Query employees with fuzzy matching by name or email
- Import employee records from Feishu or Deel CSV exports with deduplication
- View and filter source-department-to-finance-department mappings

## Tools Included

### 1. Query Employee Roster

Search for employees by name or email to find their finance department assignment and other details.

**Parameters:**
- `query` (required): Employee name or email to search for (supports partial/fuzzy matching)

**Returns:**
- List of matching employees with:
  - Full name and email
  - Data source (feishu/deel)
  - Source department and job title
  - Employment type
  - Finance department assignment
  - Status and notes
- Total count of matches

### 2. Import Roster from CSV

Import employee data from Feishu or Deel CSV exports into the roster. Supports smart column mapping, deduplication by source+source_id and email, and preserves manual finance department edits.

**Parameters:**
- `csv_content` (required): The full CSV text content to import (include the header row)
- `source` (required): Which system the CSV was exported from (`feishu` or `deel`)
- `dry_run` (optional): Preview changes without actually importing (default: false)

**Returns:**
- Number of records added, updated, and skipped
- List of error messages for any rows that failed
- Whether the operation was a dry run

### 3. Get Department Mapping

View the mapping from source departments (Feishu/Deel) to finance departments.

**Parameters:**
- `source_department` (optional): Department name to filter by (supports fuzzy matching)

**Returns:**
- List of department mappings with:
  - Source department name
  - Mapped finance department
  - Source system (feishu/deel)
- Total count of mappings returned

## Authentication

This plugin supports two authentication methods. You only need to configure one.

### Option A: OAuth2 (Interactive)

Best for individual users who want to authenticate with their own Google account.

- Requires a Google OAuth Client ID and Client Secret
- The user authorizes access through a browser-based OAuth flow
- Tokens are automatically managed (access token + refresh token)

### Option B: Service Account (Headless)

Best for server-to-server or automated workflows where no user interaction is desired.

- Requires a GCP Service Account JSON key
- The service account must be granted access to the target spreadsheet (share the sheet with the service account email)
- No browser-based authorization needed

## Setup

### 1. Prepare the Google Spreadsheet

Create a Google Spreadsheet with the following three sheets (tabs):

#### Sheet: Roster

The main employee data sheet. Expected columns:

| Column | Description |
|--------|-------------|
| full_name | Employee full name |
| email | Employee email address |
| source | Data source (feishu or deel) |
| source_id | Unique ID from the source system |
| source_department | Department name in the source system |
| job_title | Employee job title |
| employment_type | Type of employment |
| finance_department | Assigned finance department (can be manually edited) |
| status | Employee status |
| notes | Additional notes (can be manually edited) |

#### Sheet: Department_Mapping

Maps source system departments to finance departments.

| Column | Description |
|--------|-------------|
| source_department | Department name as it appears in Feishu or Deel |
| finance_department | The corresponding finance department |
| source | Source system (feishu or deel) |

#### Sheet: Sync_Log

Tracks import operations for audit purposes.

| Column | Description |
|--------|-------------|
| timestamp | When the import was run |
| source | Data source imported from |
| added | Number of records added |
| updated | Number of records updated |
| skipped | Number of records skipped |
| errors | Number of errors |

### 2. Configure Google Cloud (OAuth2 Path)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Enable the **Google Sheets API** under APIs & Services
4. Go to **APIs & Services** > **Credentials**
5. Create an **OAuth 2.0 Client ID** (Web application type)
6. Note down the **Client ID** and **Client Secret**

### 3. Configure Google Cloud (Service Account Path)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Enable the **Google Sheets API** under APIs & Services
4. Go to **IAM & Admin** > **Service Accounts**
5. Create a service account and download the JSON key file
6. Share your Google Spreadsheet with the service account email address (found in the JSON key, ending in `@*.iam.gserviceaccount.com`)

### 4. Install Plugin in Dify

1. Upload the `employee_roster.difypkg` to your Dify instance
2. Or use remote debugging (see Development section below)

### 5. Configure Credentials

When adding the plugin, you will be prompted to enter:
- **Google Spreadsheet ID** (required): The ID from your spreadsheet URL (`https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`)
- **Service Account JSON** (optional): Paste the full JSON content of the service account key file (only if using Service Account auth)
- **OAuth Client ID / Client Secret**: Required if using OAuth2 authentication

## Usage Examples

### Example 1: Search for an Employee

```yaml
Workflow Step: Use Tool
Tool: Query Employee Roster
Parameters:
  query: "jane.doe@company.com"
```

Output: Matching employee records with finance department assignment, job title, and source system.

### Example 2: Dry Run a CSV Import

```yaml
Workflow Step: Use Tool
Tool: Import Roster from CSV
Parameters:
  csv_content: "<paste CSV text here>"
  source: "feishu"
  dry_run: true
```

Output: Preview of how many records would be added, updated, or skipped -- without writing anything to the sheet.

### Example 3: Import Employees from Deel

```yaml
Workflow Step: Use Tool
Tool: Import Roster from CSV
Parameters:
  csv_content: "<paste Deel CSV export here>"
  source: "deel"
  dry_run: false
```

Output: Summary of added, updated, and skipped records. Existing finance_department and notes fields are preserved for records that already exist.

### Example 4: Look Up Department Mappings

```yaml
Workflow Step: Use Tool
Tool: Get Department Mapping
Parameters:
  source_department: "Engineering"
```

Output: All department mappings where the source department matches "Engineering" (fuzzy match), showing the corresponding finance department.

### Example 5: Full Workflow -- Import and Verify

```yaml
Step 1: Import Roster from CSV (Tool)
  source: "feishu"
  dry_run: true
  -> Review the preview output

Step 2: Import Roster from CSV (Tool)
  source: "feishu"
  dry_run: false
  -> Perform the actual import

Step 3: Query Employee Roster (Tool)
  query: "new.employee@company.com"
  -> Verify the imported record
```

## Development & Testing

### Local Development

```bash
cd employee_roster_plugin
uv venv
source .venv/bin/activate

uv pip install -r requirements.txt

python main.py
```

### Remote Debugging

Configure `.env` file:
```
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=debug.dify.ai
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=your-debug-key
```

### Package Plugin

```bash
dify plugin package ./employee_roster_plugin
```

## License

Copyright (c) 2026

## Support

For issues or questions, please refer to the Dify plugin documentation.
