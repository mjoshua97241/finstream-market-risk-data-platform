# Phase 1 (Days 1–5)

Foundation & Infrastructure

Goal:
Cloud environment + repo ready.

Tasks:

[] Day 1

    [x] Create GitHub repo
    [x] Add README skeleton
    [x] Setup project folder structure
    [x] Install Python environment

[] Day 2

    [x] Setup Terraform
    [x] Create GCS buckets
    [x] Create BigQuery dataset

[] Day 3

    [] Setup Airflow locally (Docker)
    [] Create first DAG skeleton

[] Day 4

    [] Write ingestion script for Yahoo Finance
    [] Test pulling stock data

[] Day 5

    [] Write GCS upload logic
    [] Store data in raw layer

Outcome:

```
API → GCS Raw Layer
```

---

# Phase 2 (Days 6–10)

Data Lake & Validation

Goal:
Implement Raw → Validated pipeline.

[] Day 6

    [] Implement schema validation

[] Day 7

    [] Implement quarantine logic

[] Day 8

    [] Write validated dataset output

[] Day 9

    [] Load validated data to BigQuery

[] Day 10

    [] Automate pipeline in Airflow

Outcome:

```
API → Raw → Validated → BigQuery
```

---

# Phase 3 (Days 11–16)

Warehouse & dbt

Goal:
Analytics models.

[] Day 11

    [] Setup dbt project

[] Day 12

    [] Create staging model

```
stg_prices
```

[] Day 13

    [] Compute indicators

```
EMA
RSI
ATR
```

[] Day 14

    [] Create signal detection model

```
fact_signals
```

[] Day 15

    [] Implement signal performance table

[] Day 16

    [] Create portfolio risk mart

Outcome:

```
BigQuery analytics layer ready
```

---

# Phase 4 (Days 17–21)

Dashboard & Monitoring

[] Day 17

    [] Build Streamlit dashboard skeleton

[] Day 18

    [] Add signal analytics chart

[] Day 19

    [] Add portfolio risk chart

[] Day 20

    [] Create monitoring tables

```
mart_pipeline_quality
mart_freshness_monitor
```

[] Day 21

    [] Build pipeline health dashboard page

---

# Phase 5 (Days 22–25)

Polish & Documentation

[] Day 22

    [] Add dbt tests

[] Day 23

    [] Write architecture documentation

[] Day 24

    [] Create system architecture diagram

[] Day 25

    [] Improve README

---

# Phase 6 (Days 26–30)

Finalization

[] Day 26

    [] Performance optimization

[] Day 27

    [] Terraform cleanup

[] Day 28

    [] Testing

[] Day 29

    [] Record demo video

[] Day 30

    [] Submit project

---

# Final Timeline

| Phase | Focus          |
| ----- | -------------- |
| 1     | Infrastructure |
| 2     | Data Lake      |
| 3     | dbt Models     |
| 4     | Dashboard      |
| 5     | Documentation  |
| 6     | Final polish   |

Total timeline: **30 days**

You will finish **before April 21**.