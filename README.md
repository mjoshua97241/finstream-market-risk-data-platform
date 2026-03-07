# FinStream: Cloud-Native Market Signal & Risk Monitoring Data Platform

## 1. Project Overview

FinStream is a cloud-native financial data platform designed to ingest hourly stock market data, compute technical trading signals, monitor portfolio-level risk metrics, and track historical signal performance.

The system demonstrates production-grade financial data engineering practices by implementing structured ingestion, data validation gates, partition-optimized warehousing, scalable signal computation, and operational monitoring.

The platform simulates backend infrastructure that could power financial analytics products used by active traders, quantitative analysts, and small investment firms.

---

# 2. Problem Statement

Active traders and small investment firms often rely on fragmented tools such as brokerage dashboards, charting software, and spreadsheets to monitor market signals and portfolio exposure.

These fragmented systems introduce several limitations:

### Lack of centralized signal monitoring

Traders track dozens or hundreds of stocks manually. Important technical signals such as moving average crossovers, RSI extremes, and volatility spikes may be missed.

### No historical signal performance intelligence

Most platforms generate alerts but do not track how signals historically performed. Users cannot measure win rates or average returns following signals.

### Limited portfolio-level risk visibility

Traders lack consolidated metrics such as rolling volatility, maximum drawdown, Sharpe ratio, or sector concentration.

### Lack of operational data reliability

Many systems lack defined data freshness SLAs and monitoring for pipeline failures or validation errors.

FinStream addresses these challenges by building a cloud-native data platform that centralizes market data ingestion, signal computation, portfolio risk analytics, and operational data engineering monitoring.

---

# 3. Target Users

FinStream Capital is designed for:

* Active retail traders managing $100K–$2M portfolios
* Boutique investment firms managing $5M–$250M AUM
* Quant-oriented individual traders
* Small funds without internal data engineering teams

---

# 4. Quantified Business Context

Assume a small investment firm manages a **$10M portfolio**.

If:

* 30% of capital ($3M) is concentrated in correlated technology stocks
* Market volatility causes a **4% drawdown**

Potential loss:

```
$3,000,000 × 4% = $120,000
```

If signal monitoring and volatility analytics reduce exposure by **25%**, avoided loss becomes:

```
$750,000 × 4% = $30,000
```

Centralized signal intelligence and risk monitoring can materially improve portfolio risk management.

---

# 5. System Architecture

The system follows the **Financial Data Engineering Lifecycle (FDEL)**:

1. Ingestion
2. Storage
3. Transformation & Delivery
4. Monitoring

Architecture:

```
Market Data API (Yahoo Finance)
        ↓
Airflow (Hourly DAG)
        ↓
Raw Data Lake (GCS)
        ↓
Validated Data Layer
        ↓
BigQuery Warehouse
        ↓
dbt Transformations
        ↓
Signal & Risk Analytics
        ↓
Streamlit Dashboard
```

*(Insert architecture diagram here)*

---

# 6. Data Pipeline Design

The pipeline follows a **Raw → Validated → Curated** architecture.

### Raw Layer

Stores immutable API responses.

Example structure:

```
gs://finstream/landing/prices/year=YYYY/month=MM/day=DD/hour=HH/
```

### Validated Layer

Filters corrupted or invalid records before warehouse ingestion.

Validation checks include:

* Non-null symbol
* Valid timestamps
* Numeric OHLC values
* Non-negative volume
* Duplicate removal

### Curated Layer

Analytics-ready BigQuery tables.

---

# 7. Data Model

Core warehouse tables include:

### fact_prices

Hourly OHLCV stock market data.

Partitioned by:

```
DATE(timestamp)
```

Clustered by:

```
symbol
```

---

### fact_signals

Generated signal events.

Columns include:

* signal_id
* symbol
* timestamp
* signal_type
* signal_strength
* volatility_regime

---

### fact_signal_performance

Tracks signal outcomes:

* entry_price
* price_after_1h
* price_after_1d
* return_1d
* win_flag

---

### mart_portfolio_risk

Portfolio risk analytics:

* rolling volatility
* maximum drawdown
* Sharpe ratio
* sector exposure
* signal concentration risk

---

# 8. Data Engineering Operational KPIs

The system is evaluated using production-style operational metrics.

### Data Freshness

Target: ≤ 10 minutes lag after hourly ingestion.

### Pipeline Reliability

Target: ≥ 99% successful Airflow DAG runs.

### Validation Integrity

Target: < 1% validation failure rate.

### End-to-End Latency

Target: < 15 minutes from ingestion to curated signal tables.

### Query Optimization

Target: ≥ 60% scan reduction using partitioning and clustering.

### Transformation Runtime

Target: < 3 minutes for full dbt pipeline execution.

### Scalability

Architecture supports scaling from **50 to 500 tickers** without schema redesign.

---

# 9. Monitoring and Observability

FinStream implements monitoring for:

### Pipeline Reliability

Tracked via Airflow DAG metrics.

### Data Quality

Validation failure rates stored in monitoring tables.

### Data Freshness

Curated tables monitored using freshness SLA checks.

Example monitoring tables:

* mart_pipeline_quality
* mart_freshness_monitor

---

# 10. Dashboard

The Streamlit dashboard provides two primary views.

### Market Signal Analytics

Displays:

* Signal distribution by sector
* Signal frequency by indicator
* Historical signal performance

### Portfolio Risk Monitoring

Displays:

* Rolling volatility
* Portfolio drawdown
* Sector exposure distribution

---

# 11. Technology Stack

| Layer           | Technology           |
| --------------- | -------------------- |
| Cloud           | GCP                  |
| Data Lake       | Google Cloud Storage |
| Data Warehouse  | BigQuery             |
| Orchestration   | Apache Airflow       |
| Transformations | dbt                  |
| Infrastructure  | Terraform            |
| Dashboard       | Streamlit            |
| Optional ML     | Scikit-learn         |

---

# 12. Repository Structure

```
finstream-market-risk-data-platform/

├── infrastructure/terraform/
├── pipelines/
├── dbt/
├── warehouse/
├── monitoring/
├── dashboard/
├── docs/
└── tests/
```

See `docs/architecture.md` for detailed system design.

---

# 13. Future Extensions

This architecture supports future AI capabilities including:

* AI signal interpretation
* LLM-generated risk narratives
* RAG-based trading assistants
* ML-based signal confidence scoring

---

# 14. Key Engineering Principles

The platform follows best practices used in financial data engineering systems:

* Immutable raw data storage
* Structured validation gates
* Partition-optimized warehouse design
* Operational monitoring and SLAs
* Scalable modular architecture
* Cost-efficient analytics queries

---

# 15. How to Run the Project

### 1. Provision infrastructure

```
terraform apply
```

### 2. Start Airflow

```
docker-compose up airflow
```

### 3. Run dbt transformations

```
dbt run
```

### 4. Launch dashboard

```
streamlit run dashboard/app.py
```

---

# 16. References

Financial Data Engineering principles referenced from:

* Financial Data Engineering Lifecycle (FDEL)
* Financial risk metrics such as Sharpe ratio and volatility analytics
* Data lake governance best practices

---

# ⭐ Project Highlights

This project demonstrates:

* Cloud-native financial data engineering
* Production-style data pipeline architecture
* Operational monitoring and SLAs
* Market signal analytics infrastructure
* Portfolio risk monitoring