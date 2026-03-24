# YouTube Video Campaigns

## Distilling Philanthropy — Campaign Performance

```sql campaign_summary
select
    TRIM(SPLIT_PART(campaign, ' - ', 2)) as display_name,
    campaign as raw_campaign,
    campaign_status as status,
    MIN(date) as launch_date,
    DATEDIFF('day', MIN(date), MAX(date)) + 1 as days_live,
    SUM(impressions) as total_impressions,
    ROUND(SUM(impressions) * 1.0 / (DATEDIFF('day', MIN(date), MAX(date)) + 1), 0) as avg_daily_impressions,
    ROUND(SUM(spend), 2) as total_spend,
    ROUND(SUM(spend) / SUM(impressions) * 1000, 2) as avg_cpm
from google_ads.daily_campaigns
group by 1, 2, 3
order by avg_daily_impressions desc
```

```sql totals
select
    SUM(impressions) as total_impressions,
    ROUND(SUM(spend), 2) as total_spend,
    COUNT(DISTINCT CASE WHEN campaign_status = 'ENABLED' THEN campaign END) as campaign_count,
    ROUND(SUM(spend) / SUM(impressions) * 1000, 2) as avg_cpm
from google_ads.daily_campaigns
```

<BigValue
    data={totals}
    value=total_impressions
    title="Total Impressions"
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
    value=avg_cpm
    title="Avg CPM"
    fmt="$#,##0.00"
/>

### Campaign Comparison

_Avg Daily Impressions normalizes for different launch dates — total impressions divided by days since campaign launch._

```sql campaign_links
select
    *,
    '/youtube/campaign/' || display_name as campaign_link
from ${campaign_summary}
```

<DataTable data={campaign_links} link=campaign_link search=true>
    <Column id=display_name title="Campaign" />
    <Column id=status />
    <Column id=launch_date fmt="mmm d, yyyy" />
    <Column id=days_live title="Days Live" />
    <Column id=total_impressions title="Total Impressions" fmt="#,##0" />
    <Column id=avg_daily_impressions title="Avg Daily Impressions" fmt="#,##0" />
    <Column id=total_spend title="Total Spend" fmt="$#,##0.00" />
    <Column id=avg_cpm title="Avg CPM" fmt="$#,##0.00" />
</DataTable>

[View Trends →](/youtube/trends)
