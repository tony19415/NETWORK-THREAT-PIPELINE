# Enterprise Network Threat Intelligence Pipeline (ELT)

## Project Overview
Resilient, end to end data engineering pipeline designed to ingest, transform, and analyze high velocity network traffic logs to identify security threats (DDoS and PortScans). It demonstrates a Multi Cloud Lakehouse approach, moving data from Google Cloud Storage and BigQuery into a Databricks Serverless environment for advanced spark processing.

## Technical Architecture
The pipeline follows the Medallion Architecture to ensure data quality and lineage:
1. **Infrastructure (IaC):** Deployed via Terraform to ensure reproducible, unique cloud environments
2. **Bronze (Raw):** Ingested dirty CSV logs from GCS/BigQuery into Spark DataFrames
3. **Silver (Cleaned):** Standardized legacy AM/PM timestamps and handled Infinity numeric outliers using PySpark
4. **Gold (Curated):** Aggregated security incident summaries and exported final audits back to BigQuery
5. **Visualization:** PowerBI

<img width="1446" height="679" alt="Image" src="https://github.com/user-attachments/assets/221e5b24-2fec-4622-8c82-00913ccd299e" />

## Tech Stack
* Infrastructure: Terraform, Google Cloud CLI
* Cloud Platforms: Google Cloud Platforms (GCS, BigQuery, IAM), Databricks
* Languages: Python, SQL (SparkSQL)
* Libraries: PySpark, Pandas, gcsfs, Google BigQuery Python Client

