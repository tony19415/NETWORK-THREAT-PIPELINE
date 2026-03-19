# Enterprise Network Threat Intelligence Pipeline (ELT)

## Project Overview
An automated, end-to-end ELT data pipeline designed to ingest, pseudonymize, and model raw network traffic logs for security analytics. This project demonstrates enterprise-grade data engineering practices, including real-time schema drift handling, GDPR-compliant data masking, and containerized orchestration.

## Architecture & Tech Stack
* **Extraction & Masking:** Python, Pandas, hashlib
* **Orchestration:** Apache Airflow (Dockerized)
* **Data Warehouse:** PostgreSQL (Dockerized)
* **Transformation:** dbt (Data Build Tool)
* **Visualization:** PowerBI

## Key Engineering Features

### 1. Dynamic Schema Drift Resolution
Network traffic logs (like the CIC-IDS-2017 dataset) are notorious for inconsistent headers across different server mirrors. The Python extraction layer features a defensive mapping algorithm that cleans, standardizes, and safely bypasses missing IP columns without crashing the pipeline, logging the drift for downstream review.

### 2. GDPR-Compliant PII Pseudonymization
To adhere to strict data privacy governance, all personally identifiable information (PII) is masked *in-flight*. The pipeline applies a SHA-256 hashing algorithm with a secure salt to `source_ip` and `destination_ip` columns before the data is ever loaded into the PostgreSQL data warehouse, ensuring raw IPs never hit the disk.

### 3. Containerized Orchestration (Airflow)
The pipeline is fully automated using a custom Apache Airflow environment. By pinning a Python 3.11 image and utilizing Airflow's native `_PIP_ADDITIONAL_REQUIREMENTS`, the environment dynamically resolves C++ compiler dependencies for Pandas and SQLAlchemy, bypassing standard Alpine Linux limitations.

### 4. Modular Data Transformation (dbt)
Raw data loaded into the `public` schema is transformed via dbt into a clean `analytics` schema. 
* **Staging (`stg_network_logs`):** Standardizes data types and introduces boolean business logic flags for malicious traffic.
* **Data Marts:**
  * `mart_threat_summary`: Aggregates 100,000+ raw packet logs into distinct threat actor profiles, calculating a behavioral `threat_percentage`.
  * `mart_threats_over_time`: Truncates millisecond-level event timestamps into 1-minute intervals to map the chronological density of malicious network spikes.

## The Visualization Layer
The final Data Marts feed directly into a PowerBI SOC (Security Operations Center) dashboard. The dashboard utilizes quadrant-based information design (Scatter Plot) to map attacker behavior and a dynamic time-series topology (Line Chart) to visualize exact moments of network compromise.

[image](Security_Operations_Center.png)

## How to Run Locally
1. Clone the repository.
2. Initialize the infrastructure: `docker-compose up -d`
3. Access Airflow at `http://localhost:8080` to trigger the `network_threat_ingestion` DAG.
4. Run transformations: `dbt run` inside the `threat_models` directory.
5. Connect your BI tool to `localhost:5433`.