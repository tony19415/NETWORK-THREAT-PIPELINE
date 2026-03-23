# Data Governance Policy: Network Threat Intelligence

## 1. Purpose & Scope
This policy establishes the data trust and compliance framework for the Network Threat Intelligence pipeline. It ensures that all security telemetry processed within the **Databricks/GCP** ecosystem adheres to **GDPR (Article 25)** and the **EU AI Act** requirements for high-quality, traceable data.

## 2. Data Contract Standards (Shift-Left Quality)
To prevent downstream "data poisoning" and model hallucination, a strict **Data Contract** is enforced at the ingestion point:
* **Schema Enforcement:** All incoming logs must match the `network_contract` StructType.
* **Null-Value Rejection:** Critical identity fields (IPs, Timestamps) are non-nullable.
* **Dead Letter Queue (DLQ):** Any data violating the contract is quarantined in a isolated GCS bucket for forensic audit rather than entering the processing stream.

## 3. Privacy & Compliance (GDPR)
In accordance with **Data Minimization** principles:
* **Pseudonymization:** All Personally Identifiable Information (PII), specifically Source and Destination IPs, must be masked using **SHA-256 Cryptographic Hashing** with an added salt.
* **Data Retention:** Raw PII is dropped immediately after the Silver transformation layer to reduce organizational liability.

## 4. AI Act & Traceability (Lineage)
To support transparency requirements for automated decision-making:
* **Metadata Injection:** Every record is tagged with `data_provenance`, `compliance_version`, and `processing_timestamp`.
* **Version Control:** All governance logic (masking algorithms and contracts) is stored in GitHub and verified via automated unit tests before deployment.

## 5. Roles & Access (RBAC)
* **Production:** Only the automated service identity has write-access to Gold tables.
* **Analysts:** Access is granted via **SQL Views** that expose only masked, aggregated threat metrics, ensuring "Least Privilege" access.