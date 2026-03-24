---
title: Trends
sidebar_position: 2
---

# Campaign Trends

Compare campaign performance normalized by day of campaign run (Day 1 = launch day).

```sql campaign_types
select 'All' as campaign_type
union all select 'Shorts'
union all select 'Full Length'
```

<ButtonGroup data={campaign_types} name=type_filter value=campaign_type defaultValue="All" title="Campaign Type" />

```sql daily_by_campaign_day
select
    REGEXP_REPLACE(campaign, '^[0-9]{4}-[0-9]{2}-[0-9]{2}[ ]*-?[ ]*', '') as display_name,
    CASE
        WHEN REGEXP_REPLACE(campaign, '^[0-9]{4}-[0-9]{2}-[0-9]{2}[ ]*-?[ ]*', '') ILIKE '%Full Length%'
          OR REGEXP_REPLACE(campaign, '^[0-9]{4}-[0-9]{2}-[0-9]{2}[ ]*-?[ ]*', '') ILIKE '%Long Form%'
        THEN 'Full Length'
        ELSE 'Shorts'
    END as campaign_type,
    date,
    video_trueview_views as views,
    impressions,
    ROUND(spend / NULLIF(video_trueview_views, 0), 4) as daily_cpv,
    DATEDIFF('day', MIN(date) OVER (PARTITION BY campaign), date) + 1 as campaign_day,
    SUM(video_trueview_views) OVER (PARTITION BY campaign ORDER BY date) as cumulative_views
from google_ads.daily_campaigns
order by campaign_day, display_name
```

```sql filtered_trends
select * from ${daily_by_campaign_day}
where '${inputs.type_filter}' = 'All' OR campaign_type = '${inputs.type_filter}'
```

### Daily Views by Campaign

<LineChart
    data={filtered_trends}
    x=campaign_day
    y=views
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="Views"
    echartsOptions={{legend: {orient: 'vertical', right: 0, top: 'middle'}, grid: {right: '25%'}}}
/>

### Cumulative Views by Campaign

<LineChart
    data={filtered_trends}
    x=campaign_day
    y=cumulative_views
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="Cumulative Views"
    echartsOptions={{legend: {orient: 'vertical', right: 0, top: 'middle'}, grid: {right: '25%'}}}
/>

### Daily CPV by Campaign

<LineChart
    data={filtered_trends}
    x=campaign_day
    y=daily_cpv
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="CPV ($)"
    echartsOptions={{legend: {orient: 'vertical', right: 0, top: 'middle'}, grid: {right: '25%'}}}
/>

[← Back to Overview](/youtube)
