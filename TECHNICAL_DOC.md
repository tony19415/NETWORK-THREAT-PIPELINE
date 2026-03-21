# Technical Document of Troubleshooting

## Phase 0: Infrastructure & Environment Setup (Foundation)
Project began with local environment configuration and Infrastructure as Code (IaC) deployment.

| Error                                        | Root Cause                                                                                                      | Solution                                                                                                         |
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| GCP Project ID Collisions                    | Bucket names and Project IDs must be globally unique across all of Google Cloud.                                | Implemented Terraform Random Providers to generate a unique UUID suffix (-05eca0e0...) for all resources.        |
| gcloud Application Default Credentials (ADC) | Terraform couldn't "see" the login from the browser because the quota project wasn't set.                       | Used gcloud auth application-default login to link the local terminal to the specific GCP project billing.       |
| IAM Propagation Delay                        | Assigning the "Owner" role doesn't always automatically grant specific "BigQuery Admin" API access immediately. | Manually attached the BigQuery Admin and Storage Admin roles to the user identity to bypass service-link delays. |

---

## Phase 1: BigQuery CLI Ingestion (Bronze Layer)
Moving 540k+ row dataset from GCS into structured BigQuery table

| Error                                      | Root Cause                                                                                               | Solution                                                                                                                 |
|--------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| Special Character Rejection (Flow Bytes/s) | Headers containing / or spaces violate standard BigQuery SQL naming conventions.                         | Utilized the Character Map V2 flag (--column_name_character_map=V2) to auto-replace illegal characters with underscores. |
| Positional Argument Error                  | Multi-line Bash commands with backslashes (\) often break in Cloud Shell due to hidden trailing spaces.  | Refactored the bq load into a "Clean One-Liner" to ensure the shell interpreted flags and paths correctly.               |
| Numeric Overflow (Infinity values)         | The raw dataset uses the string "Infinity" for zero-division errors, which is incompatible with FLOAT64. | Implemented a "Bad Record Tolerance" strategy (--max_bad_records=1000) to skip dirty rows for later cleaning in Spark.   |
| Timestamp Parsing (AM/PM format)           | BigQuery’s TIMESTAMP type only accepts ISO-8601 strings.                                                 | Ingested the column as a STRING first (Schema-on-Read), deferring the conversion to the Silver transformation layer.     |

---

## Phrase 2: Databricks Serverless Engineering
Transition from local development to Databricks Serverless (Free Edition) environment.

| Error                          | Root Cause                                                                                                      | Solution                                                                                                                      |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| CONFIG_NOT_AVAILABLE           | Serverless compute blocks global spark.conf.set commands to protect the shared environment.                     | Switched to Local Option Passing, injecting credentials directly into the .read.format("bigquery") method.                    |
| JVM_ATTRIBUTE_NOT_SUPPORTED    | The _jsc attribute (Java Spark Context) is restricted in serverless mode to prevent low-level JVM manipulation. | Abandoned Hadoop-level configurations in favor of Python-native library bridges.                                              |
| Metadata 404 (Table Not Found) | The Spark-BigQuery Storage API struggled to resolve project/dataset locations across clouds (AWS to GCP).       | Implemented the "Pandas Bridge": used the gcsfs library to read data into the driver memory, then parallelized it into Spark. |

---

## Phase 3: Data Transformation (Silver to Gold)
Turning 540k rows of raw traffic into security intelligence
- Data Imputation: Handled Infinity strings by casting them to Double and capping them at a high constant (999999999) to allow for mathematical modeling.

- Temporal Formatting: Used Spark's to_timestamp() with a custom pattern (dd/MM/yyyy hh:mm a) to convert legacy strings into searchable time-series objects.

- The Gold Layer: Aggregated 213 minutes of distinct attack windows and exported the results back to BigQuery using the Reverse Pandas Bridge for permanent storage.

