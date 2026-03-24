# {params.campaign_name}

```sql campaign_detail
select
    date,
    impressions,
    spend,
    ROUND(spend / NULLIF(impressions, 0) * 1000, 2) as daily_cpm,
    SUM(impressions) OVER (ORDER BY date) as cumulative_impressions
from google_ads.daily_campaigns
where TRIM(SPLIT_PART(campaign, ' - ', 2)) = '${params.campaign_name}'
order by date
```

```sql campaign_stats
select
    MIN(date) as launch_date,
    DATEDIFF('day', MIN(date), MAX(date)) + 1 as days_live,
    SUM(impressions) as total_impressions,
    ROUND(SUM(impressions) * 1.0 / (DATEDIFF('day', MIN(date), MAX(date)) + 1), 0) as avg_daily_impressions,
    ROUND(SUM(spend), 2) as total_spend,
    ROUND(SUM(spend) / SUM(impressions) * 1000, 2) as avg_cpm
from google_ads.daily_campaigns
where TRIM(SPLIT_PART(campaign, ' - ', 2)) = '${params.campaign_name}'
```

<BigValue data={campaign_stats} value=total_impressions title="Total Impressions" fmt="#,##0" />
<BigValue data={campaign_stats} value=total_spend title="Total Spend" fmt="$#,##0.00" />
<BigValue data={campaign_stats} value=avg_cpm title="Avg CPM" fmt="$#,##0.00" />
<BigValue data={campaign_stats} value=days_live title="Days Live" />
<BigValue data={campaign_stats} value=avg_daily_impressions title="Avg Daily Impressions" fmt="#,##0" />

### Daily Impressions

<BarChart
    data={campaign_detail}
    x=date
    y=impressions
    xAxisTitle="Date"
    yAxisTitle="Impressions"
/>

### Spend vs Impressions

<LineChart
    data={campaign_detail}
    x=date
    y=impressions
    y2=spend
    yAxisTitle="Impressions"
    y2AxisTitle="Spend ($)"
/>

### CPM Trend

<LineChart
    data={campaign_detail}
    x=date
    y=daily_cpm
    xAxisTitle="Date"
    yAxisTitle="CPM ($)"
/>

### Daily Data

<DataTable data={campaign_detail} search=true>
    <Column id=date fmt="mmm d, yyyy" />
    <Column id=impressions fmt="#,##0" />
    <Column id=spend fmt="$#,##0.00" />
    <Column id=daily_cpm title="CPM" fmt="$#,##0.00" />
</DataTable>

[← Back to Overview](/youtube)
