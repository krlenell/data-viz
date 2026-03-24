# Campaign Trends

Compare campaign performance normalized by day of campaign run (Day 1 = launch day).

```sql campaign_types
select 'All' as campaign_type
union all select 'Shorts'
union all select 'Full Length'
```

<Dropdown data={campaign_types} name=type_filter value=campaign_type defaultValue="All" title="Campaign Type" />

```sql daily_by_campaign_day
select
    REGEXP_REPLACE(campaign, '^\d{4}-\d{2}-\d{2}\s*-?\s*', '') as display_name,
    CASE
        WHEN REGEXP_REPLACE(campaign, '^\d{4}-\d{2}-\d{2}\s*-?\s*', '') ILIKE '%Full Length%'
          OR REGEXP_REPLACE(campaign, '^\d{4}-\d{2}-\d{2}\s*-?\s*', '') ILIKE '%Long Form%'
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
where '${inputs.type_filter.value}' = 'All' OR campaign_type = '${inputs.type_filter.value}'
```

### Daily Views by Campaign

<LineChart
    data={filtered_trends}
    x=campaign_day
    y=views
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="Views"
/>

### Cumulative Views by Campaign

<LineChart
    data={filtered_trends}
    x=campaign_day
    y=cumulative_views
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="Cumulative Views"
/>

### Daily CPV by Campaign

<LineChart
    data={filtered_trends}
    x=campaign_day
    y=daily_cpv
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="CPV ($)"
/>

[← Back to Overview](/youtube)
