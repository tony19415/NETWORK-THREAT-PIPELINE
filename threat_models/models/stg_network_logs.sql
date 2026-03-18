{{ config(materialized='table') }}

with raw_logs as (
    select * from {{ source('raw_network_data', 'raw_network_logs') }}
)

select
    flow_id,
    src_ip_hashed as source_ip,
    src_port as source_port,
    dst_ip_hashed as destination_ip,
    dst_port as destination_port,
    protocol,
    timestamp as event_timestamp,
    total_fwd_packet as fwd_packets,
    total_bwd_packets as bwd_packets,
    label as threat_classification,

    -- Boolean flag for BI filtering
    case
        when label = 'BENIGN' then false
        else true
    end as is_malicious

from raw_logs