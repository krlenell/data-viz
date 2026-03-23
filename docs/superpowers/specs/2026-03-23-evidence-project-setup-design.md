# Evidence Project Setup — Design Spec

## Overview

Set up an Evidence framework project within the existing `data-viz` repo to serve as the visualization layer for TikTok ad metrics. Evidence will read CSV data via DuckDB and render SQL+Markdown dashboard pages.

## Context

- **Goal:** POC dashboard for TikTok follows data (Skills JAM0909 account)
- **Data source:** Windsor.ai → Python pull script → CSVs → Evidence/DuckDB
- **This spec covers:** Evidence project scaffolding and configuration only (not the data pull script or dashboard pages)

## Project Structure

```
data-viz/
├── evidence/                    # Evidence project (scaffolded from template)
│   ├── pages/                   # Dashboard pages (SQL + Markdown)
│   │   └── index.md             # Minimal entry point (example pages removed)
│   ├── sources/                 # Data source configs
│   │   └── tiktok/              # DuckDB source reading CSVs from ../data/
│   │       ├── connection.yaml
│   │       └── follows.sql       # SQL query to read CSV into a table
│   ├── package.json
│   └── evidence.config.yaml
├── scripts/                     # Python data pull script (empty for now)
├── data/                        # CSVs output by scripts, read by Evidence
│   ├── .gitkeep
│   └── tiktok_follows_sample.csv
├── data-viz-project-context.md
└── .gitignore
```

## Approach

**Scaffold method:** `npx degit evidence-dev/template evidence`

This pulls the official Evidence template into the `evidence/` subdirectory. We then:

1. Remove all example/demo pages
2. Replace with a minimal `index.md` entry point
3. Configure a DuckDB data source pointing at `../data/`

## Data Source Configuration

- **Source name:** `tiktok`
- **Type:** DuckDB, reading CSV files
- **Config file:** `evidence/sources/tiktok/connection.yaml`

**`connection.yaml` contents:**

```yaml
name: tiktok
type: duckdb
options:
  filename: ':memory:'
```

Uses an in-memory DuckDB instance. The actual CSV reading happens in the SQL query file.

**`follows.sql` contents:**

```sql
select * from read_csv_auto('../data/tiktok_follows_sample.csv')
```

This exposes the CSV data as a queryable table named `follows` (derived from the filename) that Evidence pages can reference.

**Note:** The `../data/` relative path resolves from the Evidence project root where `npm run dev` runs.

## Sample Data

A small sample CSV (`data/tiktok_follows_sample.csv`) with synthetic data matching the expected schema:

| Column      | Type    | Description                    |
|-------------|---------|--------------------------------|
| date        | date    | Daily granularity (YYYY-MM-DD) |
| campaign    | string  | Campaign name                  |
| follows     | integer | Daily follow count             |
| impressions | integer | Daily impression count         |
| spend       | float   | Daily spend in USD             |
| clicks      | integer | Daily click count              |

~10 rows of representative data so `npm run dev` renders something immediately.

## Minimal index.md

The entry point page will contain a basic query and table to verify the data source works:

````markdown
# TikTok Follows Dashboard

```sql follows_summary
select * from tiktok.follows
```

<DataTable data={follows_summary} />
````

This is intentionally minimal — dashboard design is out of scope for this spec.

## .gitignore Additions

```
# Evidence build artifacts
evidence/.evidence/
evidence/node_modules/

# Real data files (keep sample)
data/*.csv
!data/tiktok_follows_sample.csv
```

## What's Cleaned Out From Template

- All example pages in `pages/` (replaced with minimal `index.md`)
- Any example source configurations (replaced with `tiktok` DuckDB source)
- Example content is removed, Evidence config files are kept as-is

## Success Criteria

1. `cd evidence && npm install && npm run dev` starts a working dev server
2. The dev server renders an `index.md` page that queries the sample CSV
3. DuckDB source correctly reads from `../data/tiktok_follows_sample.csv`
4. Project structure is clean — no leftover example content

## Out of Scope

- Python data pull script (future step)
- Dashboard page design and layout (future step)
- Production hosting and authentication (post-POC)
- CI/CD pipeline
