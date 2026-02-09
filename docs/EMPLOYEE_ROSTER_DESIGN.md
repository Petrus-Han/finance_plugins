# Employee Roster Plugin (员工花名册) — Design & Workflow

## Overview

The Employee Roster plugin manages employee-to-finance-department mappings for the finance team's bookkeeping needs. It replaces the manual process of cross-referencing Feishu and Deel exports to classify employees into finance departments.

**Backend**: Google Sheets (single spreadsheet, three worksheets)
**Auth**: OAuth2 (recommended for interactive use) or Service Account (for automation)
**Interface**: 3 Dify tools callable by AI Agent or Workflow nodes

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Dify Platform                     │
│                                                      │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Agent /  │  │  query_      │  │  import_      │  │
│  │  Workflow │──│  roster      │  │  roster_csv   │  │
│  │          │  └──────┬───────┘  └──────┬────────┘  │
│  │          │  ┌──────┴───────┐  ┌──────┴────────┐  │
│  │          │──│  get_dept_   │  │  Provider     │  │
│  │          │  │  mapping     │  │  (OAuth/SA)   │  │
│  └──────────┘  └──────┬───────┘  └──────┬────────┘  │
└───────────────────────┼─────────────────┼────────────┘
                        │                 │
                        ▼                 ▼
               ┌─────────────────────────────────┐
               │       Google Sheets API          │
               │   (gspread + google-auth)        │
               └──────────────┬──────────────────┘
                              ▼
               ┌─────────────────────────────────┐
               │       Google Spreadsheet         │
               │                                  │
               │  ┌─────────┐ ┌──────────────┐   │
               │  │ Roster  │ │ Dept_Mapping │   │
               │  └─────────┘ └──────────────┘   │
               │  ┌──────────┐                    │
               │  │ Sync_Log │                    │
               │  └──────────┘                    │
               └─────────────────────────────────┘
```

## Authentication (Dual Mode)

### OAuth2 (Recommended for interactive use)

The admin configures a GCP OAuth Client (client_id + client_secret) in the Dify plugin settings. When a user enables the plugin, they go through Google's consent screen to grant access. The plugin stores `access_token` and `refresh_token`, and auto-refreshes when expired.

**Scopes**: `spreadsheets`, `drive.readonly`, `userinfo.email`

### Service Account (For automation / CI)

The admin provides a Service Account JSON key in the provider config. The Service Account must be shared as an editor on the target spreadsheet. No user interaction needed — good for scheduled workflows.

### Client Selection Logic (`get_gspread_client`)

```
if access_token exists → use OAuth token
elif service_account_json exists → use Service Account
else → raise error
```

## Google Sheets Structure

The plugin auto-creates these sheets on first use via `ensure_sheets_initialized()`:

### Sheet: Roster

| Column | Purpose |
|--------|---------|
| full_name | Employee full name |
| email | Work email address |
| source | Data origin: `feishu` or `deel` |
| source_id | Employee/contract ID in source system |
| source_department | Department name in source system |
| job_title | Job title |
| employment_type | Full-time, contractor, etc. |
| **finance_department** | **Finance team's classification (manually edited, never overwritten by import)** |
| status | Employment status |
| **notes** | **Finance team's notes (manually edited, never overwritten by import)** |
| last_synced | Last import/update timestamp (UTC ISO 8601) |

### Sheet: Department_Mapping

| Column | Purpose |
|--------|---------|
| source_department | Department name in source system |
| finance_department | Mapped finance department |
| source | Which source system (`feishu` / `deel`) |

This mapping table is maintained manually by the finance team in Google Sheets.

### Sheet: Sync_Log

| Column | Purpose |
|--------|---------|
| timestamp | Import timestamp (UTC ISO 8601) |
| source | feishu / deel |
| records_added | Count of new records |
| records_updated | Count of updated records |
| records_skipped | Count of unchanged records |

## Tool Workflows

### 1. query_roster — Query Employee

**Use case**: Agent asks "Which finance department does Zhang San belong to?"

```
Input: query="张三" (or "zhangsan@company.com")
        ↓
1. Connect to Google Sheets via get_gspread_client()
2. Read all rows from Roster sheet
3. Fuzzy match: case-insensitive substring search on full_name and email
4. Return matching employees with finance_department
        ↓
Output: [{ full_name, email, finance_department, ... }]
```

### 2. import_roster_csv — Import from Feishu / Deel

**Use case**: Finance team exports CSV from Feishu, pastes content for batch import.

```
Input: csv_content="姓名,邮箱,工号,...\n张三,..." source="feishu" dry_run=false
        ↓
1. Parse CSV with DictReader
2. Smart column mapping:
   - Feishu: 姓名→full_name, 邮箱→email, 工号→source_id, 部门→source_department ...
   - Deel: name→full_name, email→email, contract_id→source_id, team→source_department ...
3. For each row:
   a. Map CSV headers to canonical fields
   b. Dedup: look up by (source, source_id), then by email
   c. If existing:
      - Update changed fields (name, email, department, title, type, status)
      - PRESERVE finance_department and notes (finance team edits)
      - Skip if no real changes
   d. If new: append row with empty finance_department/notes
4. Batch write updates + append new rows
5. Write audit entry to Sync_Log
        ↓
Output: { added: 5, updated: 3, skipped: 12, errors: [] }
```

**Key design: finance edits are never overwritten.** The `finance_department` and `notes` columns are only empty on new records — once the finance team fills them in, subsequent imports leave them untouched.

### 3. get_department_mapping — View Department Mappings

**Use case**: Agent asks "How do Feishu departments map to finance departments?"

```
Input: source_department="技术" (optional filter)
        ↓
1. Read Department_Mapping sheet
2. Optionally filter by source_department (fuzzy match)
3. Return mapping list
        ↓
Output: [{ source_department: "技术部", finance_department: "R&D", source: "feishu" }]
```

## Typical Workflow

1. **Initial Setup**: Admin creates a Google Spreadsheet, configures the plugin with OAuth or Service Account credentials, enters the Spreadsheet ID.

2. **First Import**: Finance team exports employee list from Feishu → pastes CSV into the `import_roster_csv` tool → roster is populated.

3. **Manual Classification**: Finance team opens the Google Sheet, fills in `finance_department` for each employee, maintains `Department_Mapping` table.

4. **Ongoing Use**:
   - AI Agent queries `query_roster` to look up employees during expense categorization
   - Periodic re-imports from Feishu/Deel update employee info without touching finance classifications
   - `get_department_mapping` helps the agent understand the mapping rules

5. **Audit**: Every import is logged in `Sync_Log` for traceability.

## File Structure

```
employee_roster_plugin/
├── _assets/icon.svg                  # Plugin icon
├── manifest.yaml                     # Plugin metadata (v0.0.1)
├── main.py                           # Entrypoint
├── pyproject.toml                    # Dependencies
├── .gitignore                        # Excludes .venv, __pycache__, etc.
├── provider/
│   ├── employee_roster.yaml          # Credentials config (OAuth + SA)
│   └── employee_roster.py            # OAuth flow, get_gspread_client(), ensure_sheets_initialized()
└── tools/
    ├── query_roster.yaml             # Tool definition
    ├── query_roster.py               # Fuzzy search implementation
    ├── import_roster_csv.yaml        # Tool definition
    ├── import_roster_csv.py          # CSV import with dedup & preserve logic
    ├── get_department_mapping.yaml   # Tool definition
    └── get_department_mapping.py     # Department mapping query
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| dify-plugin | >=0.6.0 | Dify plugin SDK |
| gspread | >=6.0.0 | Google Sheets client |
| google-auth | >=2.0.0 | Google authentication (OAuth2 + Service Account) |
| httpx | >=0.27.0 | HTTP client for OAuth token exchange |
