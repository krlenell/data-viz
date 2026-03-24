# {params.campaign_name}

```sql campaign_detail
select
    date,
    video_trueview_views as views,
    impressions,
    spend,
    ROUND(spend / NULLIF(video_trueview_views, 0), 4) as daily_cpv,
    ROUND(video_trueview_views * 1.0 / NULLIF(impressions, 0), 2) as view_rate,
    SUM(video_trueview_views) OVER (ORDER BY date) as cumulative_views
from google_ads.daily_campaigns
where TRIM(SPLIT_PART(campaign, ' - ', 2)) = '${params.campaign_name}'
order by date
```

```sql campaign_stats
select
    MIN(date) as launch_date,
    DATEDIFF('day', MIN(date), MAX(date)) + 1 as days_live,
    SUM(video_trueview_views) as total_views,
    ROUND(SUM(video_trueview_views) * 1.0 / (DATEDIFF('day', MIN(date), MAX(date)) + 1), 0) as avg_daily_views,
    ROUND(SUM(spend), 2) as total_spend,
    ROUND(SUM(spend) / NULLIF(SUM(video_trueview_views), 0), 4) as avg_cpv,
    ROUND(SUM(video_trueview_views) * 1.0 / NULLIF(SUM(impressions), 0), 2) as view_rate
from google_ads.daily_campaigns
where TRIM(SPLIT_PART(campaign, ' - ', 2)) = '${params.campaign_name}'
```

<BigValue data={campaign_stats} value=total_views title="Total Views" fmt="#,##0" />
<BigValue data={campaign_stats} value=total_spend title="Total Spend" fmt="$#,##0.00" />
<BigValue data={campaign_stats} value=avg_cpv title="Avg CPV" fmt="$#,##0.000" />
<BigValue data={campaign_stats} value=days_live title="Days Live" />
<BigValue data={campaign_stats} value=avg_daily_views title="Avg Daily Views" fmt="#,##0" />

### Daily Views

<BarChart
    data={campaign_detail}
    x=date
    y=views
    xAxisTitle="Date"
    yAxisTitle="Views"
/>

### Spend vs Views

<LineChart
    data={campaign_detail}
    x=date
    y=views
    y2=spend
    yAxisTitle="Views"
    y2AxisTitle="Spend ($)"
/>

### CPV Trend

<LineChart
    data={campaign_detail}
    x=date
    y=daily_cpv
    xAxisTitle="Date"
    yAxisTitle="CPV ($)"
/>

### Daily Data

<DataTable data={campaign_detail} search=true>
    <Column id=date fmt="mmm d, yyyy" />
    <Column id=views fmt="#,##0" />
    <Column id=impressions fmt="#,##0" />
    <Column id=view_rate title="View Rate" fmt="#,##0.0%" />
    <Column id=spend fmt="$#,##0.00" />
    <Column id=daily_cpv title="CPV" fmt="$#,##0.000" />
</DataTable>

[← Back to Overview](/youtube)
