# Campaign Trends

Compare campaign performance normalized by day of campaign run (Day 1 = launch day).

```sql daily_by_campaign_day
select
    TRIM(SPLIT_PART(campaign, ' - ', 2)) as display_name,
    date,
    impressions,
    ROUND(spend / NULLIF(impressions, 0) * 1000, 2) as daily_cpm,
    DATEDIFF('day', MIN(date) OVER (PARTITION BY campaign), date) + 1 as campaign_day,
    SUM(impressions) OVER (PARTITION BY campaign ORDER BY date) as cumulative_impressions
from google_ads.daily_campaigns
order by campaign_day, display_name
```

### Daily Impressions by Campaign

<LineChart
    data={daily_by_campaign_day}
    x=campaign_day
    y=impressions
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="Impressions"
/>

### Cumulative Impressions by Campaign

<LineChart
    data={daily_by_campaign_day}
    x=campaign_day
    y=cumulative_impressions
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="Cumulative Impressions"
/>

### Daily CPM by Campaign

<LineChart
    data={daily_by_campaign_day}
    x=campaign_day
    y=daily_cpm
    series=display_name
    xAxisTitle="Day of Campaign"
    yAxisTitle="CPM ($)"
/>

[← Back to Overview](/youtube)
