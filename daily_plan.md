# Phase 1 (Days 1–5)

Foundation & Infrastructure

Goal:
Cloud environment + repo ready.

Tasks:

[x] Day 1

    [x] Create GitHub repo
    [x] Add README skeleton
    [x] Setup project folder structure
    [x] Install Python environment

[x] Day 2

    [x] Setup Terraform
    [x] Create GCS buckets
    [x] Create BigQuery dataset

[x] Day 3

    [x] Setup Airflow locally (Docker)
    [x] Create first DAG skeleton

[x] Day 4: notebooks/market_data_prototype.py

    [x] Pull stock data from Yahoo Finance
    [x] Convert data to pandas DataFrame
    [x] Save data as parquet locally

[] Day 5: extend notebook

    [] Upload parquet file to GCS
    [] Organize path structure
        raw/market_prices/year=YYYY/month=MM/day=DD/

Outcome:

```
API → GCS Raw Layer
```

---

# Phase 2 (Days 6–10)

Data Lake & Validation

Goal:
Convert prototype to production pipeline.

[] Day 6: Convert notebook to pipeline module.
    Create: pipelines/ingestion/fetch_market_data.py

    [] fetch_market_data()
    [] save_parquet()
    [] upload_to_gcs()

[] Day 7: Validation Framework

    [] Implement schema validation
    [] Detect missing values
    [] Detect duplicate timestamps

[] Day 8: Quarantine logic

    [] Write invalid rows to quarantine/
    [] Generate validation metrics

[] Day 9: Validated dataset

    [] Save validated dataset
        validated/market_prices/

[] Day 10: Airflow orchestration
    Update DAG to call pipepline functions.

    [] extract_market_data
    [] store_raw_data
    [] validate_market_data
    [] load_to_bigquery

Outcome:

```
API → Raw → Validated
```

---

# Phase 3 (Days 11–16)

Warehouse & dbt

Goal:
Analytics-ready warehouse.

[] Day 11: BigQuery ingestion

    [] Load validated parquet to BigQuery
        Create fact_market_prices table
        DATE(timestamp)
        Cluster: symbol

[] Day 12: Setup dbt project

    [] Initialize dbt project
    [] Configure BigQuery profile


[] Day 13: Staging model

    [] stg_market_prices

```
EMA
RSI
ATR
```

[] Day 14

    [] Indicators model
        ```
        EMA
        RSI
        ATR
        ```

[] Day 15: Signal detection

    [] Create fact_signals

[] Day 16: Portfolio risk mart

    [] Create mart_portfolio_risk

Outcome:

```
BigQuery analytics layer ready
```

---

# Phase 4 (Days 17–21)

Dashboard & Monitoring

Goal:
Visualization + pipeline monitoring

[] Day 17

    [] Build Streamlit dashboard skeleton > dashboard/app.py

[] Day 18: Signal analytics visualization

    [] Add signal analytics chart

[] Day 19: Portfolio risk visualization

    [] Chart: Volatility distribution

[] Day 20

    [] Create monitoring tables

        ```
        mart_pipeline_quality
        mart_freshness_monitor
        ```
    Metrics:
    - data freshness
    - row counts
    - validation failures

[] Day 21

    [] Add Streamlit page: Pipeline health

---

# Phase 5 (Days 22–25)

Polish & Documentation

[] Day 22

    [] Add dbt tests

    Example:
    ```
    not_null
    unique
    accepted_values
    ```

[] Day 23

    [] Write architecture documentation

    Explain:
    - pipeline design
    - data model
    - technology choices

[] Day 24

    [] Create system architecture diagram

    Architecture:
    ```
    Yahoo Finance > Airflow > GCS (Raw > Validated) > BigQuery > dbt > Streamlit
    ```

[] Day 25

    [] Improve README
        Include:
        - problem statement
        - architecture diagram
        - pipeline explanation
        - dashboard screenshots

---

# Phase 6 (Days 26–30)

Finalization

[] Day 26

    [] Performance optimization
        Examples:
        - partitioning
        - clustering
        - batch sizes

[] Day 27

    [] Terraform cleanup
    [] Parametrize configs

[] Day 28

    [] End-to-end pipeline testing

[] Day 29

    [] Record demo video
        Show:
        - Airflow DAG
        - BigQuery Tables
        - Dashboard

[] Day 30

    [] Submit project

---

# Final Timeline

| Phase | Focus          |
| ----- | -------------- |
| 1     | Infrastructure |
| 2     | Production Pipeline      |
| 3     | Warehouse & dbt     |
| 4     | Dashboard      |
| 5     | Documentation  |
| 6     | Final polish   |

Total timeline: **30 days**

You will finish **before April 21**.


