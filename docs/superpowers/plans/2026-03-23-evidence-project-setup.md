# Evidence Project Setup Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold an Evidence framework project with DuckDB, configured to read TikTok ad data from CSVs, with sample data rendering on a minimal dashboard page.

**Architecture:** Evidence project lives in `evidence/` subdirectory. A shared `data/` directory at repo root holds CSVs. Evidence's DuckDB connector reads CSVs via `read_csv_auto()`. A `scripts/` directory is stubbed out for the future Python data pull script.

**Tech Stack:** Evidence framework, DuckDB, Node.js/npm

**Spec:** `docs/superpowers/specs/2026-03-23-evidence-project-setup-design.md`

**Worktree:** `.worktrees/evidence-setup` (branch: `feature/evidence-setup`)

---

## Chunk 1: Project scaffolding and configuration

### Task 1: Create shared directories and sample data

**Files:**
- Create: `data/.gitkeep`
- Create: `data/tiktok_follows_sample.csv`
- Create: `scripts/.gitkeep`

- [ ] **Step 1: Create `data/` directory with `.gitkeep`**

```bash
mkdir -p data
touch data/.gitkeep
```

- [ ] **Step 2: Create sample CSV**

Create `data/tiktok_follows_sample.csv` with 10 rows of synthetic data matching the expected schema:

```csv
date,campaign,follows,impressions,spend,clicks
2026-03-01,Q1 2026 Follow Campaign,412,18500,248.50,0
2026-03-02,Q1 2026 Follow Campaign,387,17200,251.00,0
2026-03-03,Q1 2026 Follow Campaign,455,19800,249.75,0
2026-03-04,Q1 2026 Follow Campaign,1073,32100,252.00,0
2026-03-05,Q1 2026 Follow Campaign,998,29400,250.50,0
2026-03-06,Q1 2026 Follow Campaign,523,20100,248.00,0
2026-03-07,Q1 2026 Follow Campaign,341,16800,247.25,0
2026-03-08,BR Traffic Spark,0,12400,150.00,0
2026-03-09,BR Traffic Spark,0,11800,148.50,0
2026-03-10,Q1 2026 Follow Campaign,478,19200,251.75,0
```

- [ ] **Step 3: Create `scripts/` directory with `.gitkeep`**

```bash
mkdir -p scripts
touch scripts/.gitkeep
```

- [ ] **Step 4: Commit**

```bash
git add data/.gitkeep data/tiktok_follows_sample.csv scripts/.gitkeep
git commit -m "feat: add sample TikTok data and stub scripts directory"
```

---

### Task 2: Scaffold Evidence project

**Files:**
- Create: `evidence/` (entire directory via degit)

- [ ] **Step 1: Scaffold Evidence template**

```bash
npx degit evidence-dev/template evidence
```

This creates the `evidence/` directory with the full template. The `degit.json` in the template auto-removes `.devcontainer`, `.github`, and `scripts` directories.

Expected output: directory `evidence/` with `pages/`, `sources/`, `package.json`, `evidence.config.yaml`, etc.

- [ ] **Step 2: Verify scaffold**

```bash
ls evidence/
```

Expected: `pages/`, `sources/`, `package.json`, `evidence.config.yaml`, `.gitignore`, etc.

- [ ] **Step 3: Commit scaffolded template as-is**

```bash
git add evidence/
git commit -m "feat: scaffold Evidence project from official template"
```

Committing the unmodified template first creates a clean diff for subsequent changes.

---

### Task 3: Clean out example content

**Files:**
- Delete: `evidence/pages/index.md` (will be replaced)
- Delete: `evidence/sources/needful_things/` (entire directory)

- [ ] **Step 1: Remove example pages**

```bash
rm evidence/pages/index.md
```

Check for any other files in `pages/`:

```bash
ls evidence/pages/
```

If other `.md` files exist, remove them too. Keep the directory itself.

- [ ] **Step 2: Remove example data source**

```bash
rm -rf evidence/sources/needful_things/
```

- [ ] **Step 3: Commit cleanup**

```bash
git add -A evidence/pages/ evidence/sources/
git commit -m "chore: remove example pages and data source from template"
```

---

### Task 4: Configure DuckDB data source

**Files:**
- Create: `evidence/sources/tiktok/connection.yaml`
- Create: `evidence/sources/tiktok/follows.sql`

- [ ] **Step 1: Create tiktok source directory**

```bash
mkdir -p evidence/sources/tiktok
```

- [ ] **Step 2: Create `connection.yaml`**

Create `evidence/sources/tiktok/connection.yaml`:

```yaml
name: tiktok
type: duckdb
options:
  filename: ':memory:'
```

Note: Uses `options.filename` format matching Evidence's DuckDB connector convention (as seen in the template's `needful_things` example).

- [ ] **Step 3: Create `follows.sql`**

Create `evidence/sources/tiktok/follows.sql`:

```sql
select * from read_csv_auto('../data/tiktok_follows_sample.csv')
```

This makes the CSV data available as `tiktok.follows` in Evidence pages.

- [ ] **Step 4: Commit**

```bash
git add evidence/sources/tiktok/
git commit -m "feat: configure DuckDB source for TikTok CSV data"
```

---

### Task 5: Create minimal dashboard page

**Files:**
- Create: `evidence/pages/index.md`

- [ ] **Step 1: Create `index.md`**

Create `evidence/pages/index.md`:

````markdown
# TikTok Follows Dashboard

```sql follows_summary
select * from tiktok.follows
```

<DataTable data={follows_summary} />
````

- [ ] **Step 2: Commit**

```bash
git add evidence/pages/index.md
git commit -m "feat: add minimal dashboard page with data table"
```

---

### Task 6: Update .gitignore

**Files:**
- Modify: `.gitignore` (repo root)

- [ ] **Step 1: Update root `.gitignore`**

Replace the current `.gitignore` contents with:

```
.worktrees/

# Evidence build artifacts
evidence/.evidence/
evidence/node_modules/

# Real data files (keep sample)
data/*.csv
!data/tiktok_follows_sample.csv
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: update .gitignore for Evidence and data files"
```

---

### Task 7: Install dependencies and verify

- [ ] **Step 1: Install npm dependencies**

```bash
cd evidence && npm install
```

Expected: Successful install with no errors. `node_modules/` created.

- [ ] **Step 2: Run dev server and verify**

```bash
cd evidence && npm run dev
```

Expected: Dev server starts (usually on `http://localhost:3000`). The page should render showing:
- "TikTok Follows Dashboard" heading
- A data table with 10 rows of sample data (columns: date, campaign, follows, impressions, spend, clicks)

Verify by checking the terminal output for a successful start message (no errors).

- [ ] **Step 3: Stop dev server (Ctrl+C) and commit any generated files if needed**

Evidence may generate a `.evidence/` directory on first run. This is already gitignored.

No commit needed for this step unless Evidence modified config files during first run.

---

## Verification Checklist

After all tasks complete, verify:

- [ ] `cd evidence && npm run dev` starts without errors
- [ ] Dashboard page renders at localhost with sample data table
- [ ] No leftover example content (no `needful_things`, no example pages)
- [ ] `data/tiktok_follows_sample.csv` is tracked in git
- [ ] `data/*.csv` (other CSVs) are gitignored
- [ ] `scripts/` directory exists with `.gitkeep`
- [ ] Clean `git status` (no untracked files except `.evidence/` and `node_modules/`)
