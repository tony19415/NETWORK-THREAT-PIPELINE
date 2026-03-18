{{ config(materialized='table') }}

with staged_logs as (
    select * from {{ ref('stg_network_logs') }}
),

time_series as (
    select
        date_trunc('minute', event_timestamp::timestamp) as activity_minute,
        sum(case when is_malicious then 1 else 0 end) as malicious_packet_count,
        count(flow_id) as total_packet_count
    from staged_logs
    group by 1
)

select
    *,
    round((malicious_packet_count::numeric / total_packet_count::numeric) *100, 2) as threat_density
from time_series
order by activity_minute desc