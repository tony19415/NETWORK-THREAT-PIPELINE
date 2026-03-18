{{ config(materialized='table') }}

with staged_logs as (
    select * from {{ ref('stg_network_logs') }}
),

threat_summary as (
    select
        source_ip,
        count(flow_id) as total_connections,
        sum(case when is_malicious then 1 else 0 end) as malicious_connections,
        sum(fwd_packets) as total_fwd_packets,
        sum(bwd_packets) as total_bwd_packets,
        max(event_timestamp) as last_seen_timestamp
    from staged_logs
    group by source_ip
)

select
    *,
    -- Calculating quick threat severity percentage
    round((malicious_connections::numeric / total_connections::numeric) * 100, 2) as threat_percentage
from threat_summary
where malicious_connections > 0
order by malicious_connections desc