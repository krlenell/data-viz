---
title: YouTube Campaigns
sidebar_position: 2
---

# YouTube Video Campaigns

## Distilling Philanthropy — Campaign Performance

```sql campaign_types
select 'All' as campaign_type
union all select 'Shorts'
union all select 'Full Length'
```

<ButtonGroup data={campaign_types} name=type_filter value=campaign_type defaultValue="All" title="Campaign Type" />

```sql campaign_summary
select
    REGEXP_REPLACE(campaign, '^\d{4}-\d{2}-\d{2}\s*-?\s*', '') as display_name,
    campaign as raw_campaign,
    campaign_status as status,
    CASE
        WHEN REGEXP_REPLACE(campaign, '^\d{4}-\d{2}-\d{2}\s*-?\s*', '') ILIKE '%Full Length%'
          OR REGEXP_REPLACE(campaign, '^\d{4}-\d{2}-\d{2}\s*-?\s*', '') ILIKE '%Long Form%'
        THEN 'Full Length'
        ELSE 'Shorts'
    END as campaign_type,
    MIN(date) as launch_date,
    DATEDIFF('day', MIN(date), MAX(date)) + 1 as days_live,
    SUM(video_trueview_views) as total_views,
    ROUND(SUM(video_trueview_views) * 1.0 / (DATEDIFF('day', MIN(date), MAX(date)) + 1), 0) as avg_daily_views,
    SUM(impressions) as total_impressions,
    ROUND(SUM(spend), 2) as total_spend,
    ROUND(SUM(spend) / NULLIF(SUM(video_trueview_views), 0), 4) as avg_cpv,
    ROUND(SUM(video_trueview_views) * 1.0 / NULLIF(SUM(impressions), 0), 2) as view_rate
from google_ads.daily_campaigns
group by 1, 2, 3
order by avg_daily_views desc
```

```sql filtered_campaigns
select * from ${campaign_summary}
where '${inputs.type_filter}' = 'All' OR campaign_type = '${inputs.type_filter}'
```

```sql totals
select
    SUM(total_views) as total_views,
    ROUND(SUM(total_spend), 2) as total_spend,
    COUNT(DISTINCT CASE WHEN status = 'ENABLED' THEN raw_campaign END) as campaign_count,
    ROUND(SUM(total_spend) / NULLIF(SUM(total_views), 0), 4) as avg_cpv
from ${filtered_campaigns}
```

<BigValue
    data={totals}
    value=total_views
    title="Total Views"
    fmt="#,##0"
/>

<BigValue
    data={totals}
    value=total_spend
    title="Total Spend"
    fmt="$#,##0.00"
/>

<BigValue
    data={totals}
    value=campaign_count
    title="Active Campaigns"
/>

<BigValue
    data={totals}
    value=avg_cpv
    title="Avg CPV"
    fmt="$#,##0.000"
/>

### Campaign Comparison

_Avg Daily Views normalizes for different launch dates — total views divided by days since campaign launch._

```sql campaign_links
select
    *,
    '/youtube/campaign/' || display_name as campaign_link
from ${filtered_campaigns}
```

<DataTable data={campaign_links} link=campaign_link search=true>
    <Column id=display_name title="Campaign" />
    <Column id=campaign_type title="Type" />
    <Column id=status />
    <Column id=launch_date fmt="mmm d, yyyy" />
    <Column id=days_live title="Days Live" />
    <Column id=total_views title="Total Views" fmt="#,##0" />
    <Column id=avg_daily_views title="Avg Daily Views" fmt="#,##0" />
    <Column id=view_rate title="View Rate" fmt="#,##0.0%" />
    <Column id=total_spend title="Total Spend" fmt="$#,##0.00" />
    <Column id=avg_cpv title="Avg CPV" fmt="$#,##0.000" />
</DataTable>

[View Trends →](/youtube/trends)
