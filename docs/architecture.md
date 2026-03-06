## Repository Structure Overview

This project follows a modular architecture separating infrastructure, ingestion pipelines, transformations, and analytics delivery layers.

### infrastructure/

Contains Terraform configurations used to provision cloud resources such as GCS buckets, BigQuery datasets, and IAM permissions.

### pipelines/

Contains Airflow DAGs and Python modules responsible for ingesting, validating, and loading market data.

### dbt/

Contains analytics engineering models used to compute technical indicators, signal events, and portfolio risk metrics.

### monitoring/

Contains SQL models used to track operational KPIs such as data freshness, pipeline reliability, and validation failure rates.

### dashboard/

Contains the Streamlit application used to visualize signal analytics and pipeline health metrics.