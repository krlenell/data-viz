# Dashboard Pages — Design Spec

## Overview

Build the TikTok Follows dashboard as a single scrollable Evidence page with summary stats, a dual-axis chart, and a data table.

## Context

- **Data source:** `tiktok.follows` — CSV loaded via DuckDB (`evidence/sources/tiktok/follows.sql`)
- **Data shape:** 149 rows, columns: `date`, `campaign`, `follows`, `impressions`, `spend`, `clicks`
- **Active campaign:** "Q1 2026 Follow Campaign" is the only campaign generating follows
- **Other campaigns** (BR Traffic Spark, SkillsUSA, etc.) have zero follows — filtered out

## Page Layout

Single file: `evidence/pages/index.md`

Top to bottom:

### 1. Title

"TikTok Follows Dashboard"

### 2. Summary Stats Row

Four big number cards in a row using Evidence's `<BigValue>` component:

| Metric | Computation | Format |
|--------|-------------|--------|
| Total Follows | `SUM(follows)` | `num0` |
| Total Spend | `SUM(spend)` | `usd0` |
| Avg Cost per Follow | `SUM(spend) / SUM(follows)` | `usd2` |
| Follow Rate | `SUM(follows) / SUM(impressions)` | `pct1` |

Usage: `<BigValue data={summary_stats} value=total_follows title="Total Follows" fmt=num0 />`

### 3. Combined Dual-Axis Chart

- **Bars:** Daily follows count (left y-axis)
- **Line overlay:** Cost per follow per day (right y-axis, `y2`)
- **X-axis:** Date
- Uses Evidence's `<BarChart>` with `y2` props for the secondary axis:

```html
<BarChart
    data={daily_metrics}
    x=date
    y=follows
    y2=cost_per_follow
    y2SeriesType=line
    y2Fmt=usd2
/>
```

### 4. Data Table

Daily breakdown table using `<DataTable>`:

| Column | Source |
|--------|--------|
| Date | `date` |
| Follows | `follows` |
| Impressions | `impressions` |
| Spend | `spend` (formatted USD) |
| Cost/Follow | `cost_per_follow` (formatted USD) |
| Follow Rate | `follow_rate` (formatted %) |

## SQL Queries

Three named queries in the page:

**`summary_stats`** — aggregated totals for BigValue cards:
```sql
select
  sum(follows) as total_follows,
  sum(spend) as total_spend,
  sum(spend) / sum(follows) as avg_cost_per_follow,
  sum(follows) * 1.0 / sum(impressions) as follow_rate
from tiktok.follows
where follows > 0
  and date >= current_date - interval '30 days'
```

**`daily_metrics`** — daily aggregates for the chart and table:
```sql
select
  date,
  sum(follows) as follows,
  sum(impressions) as impressions,
  sum(spend) as spend,
  case when sum(follows) > 0 then sum(spend) / sum(follows) else null end as cost_per_follow,
  case when sum(impressions) > 0 then sum(follows) * 1.0 / sum(impressions) else null end as follow_rate
from tiktok.follows
where follows > 0
  and date >= current_date - interval '30 days'
group by date
order by date
```

**Note:** Both queries filter to `follows > 0` (excludes traffic-only campaigns) and last 30 days.

## Evidence Components Used

- `<BigValue>` — summary stat cards (with `data`, `value`, `title`, `fmt` props)
- `<BarChart>` with `y2` / `y2SeriesType=line` — dual-axis combined chart
- `<DataTable>` — sortable data table

## Files Modified

- `evidence/pages/index.md` — complete rewrite (currently a minimal placeholder)

## Success Criteria

1. `npm run dev` renders the dashboard at localhost
2. Summary stats show correct aggregated values
3. Dual-axis chart displays follows as bars and cost/follow as a line
4. Data table shows daily rows with derived metrics
5. Only follow-generating campaign data is shown
6. Default view covers last 30 days

## Out of Scope

- Multi-page navigation
- Campaign comparison views (only one active follow campaign)
- Date range picker / interactive filters
- Production hosting / auth
