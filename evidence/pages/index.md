# TikTok Follows Dashboard

```sql summary_stats
select
  sum(follows) as total_follows,
  sum(spend) as total_spend,
  sum(spend) / sum(follows) as avg_cost_per_follow,
  sum(follows) * 1.0 / sum(impressions) as follow_rate
from tiktok.follows
where follows > 0
  and date >= current_date - interval '30 days'
```

```sql daily_metrics
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

<BigValue data={summary_stats} value=total_follows title="Total Follows" fmt=num0 />
<BigValue data={summary_stats} value=total_spend title="Total Spend" fmt=usd0 />
<BigValue data={summary_stats} value=avg_cost_per_follow title="Avg Cost / Follow" fmt=usd2 />
<BigValue data={summary_stats} value=follow_rate title="Follow Rate" fmt=pct1 />

## Daily Follows & Cost per Follow

<BarChart
    data={daily_metrics}
    x=date
    y=follows
    y2=cost_per_follow
    y2SeriesType=line
    y2Fmt=usd2
/>

## Daily Breakdown

<DataTable data={daily_metrics} rows=all>
  <Column id=date />
  <Column id=follows fmt=num0 />
  <Column id=impressions fmt=num0 />
  <Column id=spend fmt=usd2 />
  <Column id=cost_per_follow title="Cost / Follow" fmt=usd2 />
  <Column id=follow_rate title="Follow Rate" fmt=pct1 />
</DataTable>
