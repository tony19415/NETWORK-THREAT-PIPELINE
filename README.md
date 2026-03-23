# Governed Network Threat Intelligence Pipeline
Multi-Cloud Medallion Architecture with Zero Trust Ingestion

## Project Overview
Enterprise grade data pipeline designed to ingest, govern and analyze 547k+ network telemetry records to detect DDoS attacks. Built using a **Multi-Cloud Lakehouse** approach (GCP + Databricks), this project implements a **Zero Trust Governance Layer** to ensure compliance with GDPR and the EU AI Act.

## Technical Architecture
The pipeline follows the **Medallion Architecture** (Bronze -> Silver -> Gold) with integrated governance gates:
1. **Infrastructure (Terraform):** Automated provisioning of GCS buckets and BigQuery datasets
2. **Ingestion (Pandas Bridge):** Secure cross-cloud data transfer using gcsfs and OAuth2 tokens to bypass Serverless JVM/Hadoop restrictions
3. **Governance (Zero Trust):** 
* Data Contracts: Strict schema enforcement via PySpark StructType
* Dead Letter Queue (DLQ): Quarantine of malformed records to prevent data poisoning
* PII Masking: Salted SHA-256 pseudonymization of Source/Destination IPs for GDPR compliance
* Traceability: Automated metadata injection for AI Act audit trails
4. **Analysis (Governed Views):** RBAC simulated SQL views providing filtered access to security analysts
5. **Visualization:** PowerBI

<img width="1446" height="679" alt="Image" src="https://github.com/user-attachments/assets/221e5b24-2fec-4622-8c82-00913ccd299e" />

## Tech Stack
* Infrastructure: Terraform, Google Cloud CLI
* Cloud Platforms: Google Cloud Platforms (GCS, BigQuery, IAM), Databricks
* Processing: PySpark, SQL (SparkSQL), Pandsa
* Compliance: GDPR (Article 25), EU AI Act (Data Provenance)

## Troubleshooting
* The 42K0I Security Block: Overcame Databricks Serverless restrictions on global Spark configurations by implementing a driver-level "Pandas Bridge."
* Schema Positional Mismatch: Resolved Arrow conversion errors by implementing explicit column selection to align the Pandas source with the strcit PySpark Data Contract
* Identity Resolution: Implemented cryptographic salting to ensure PII hashes remain unique for behavioral tracking while preventing reverse engineering


