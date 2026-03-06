# FinStream: Cloud-Native Market Signal & Risk Monitoring Data Platform

## 1. Project Overview

FinStream is a cloud-native financial data platform designed to ingest hourly stock market data, compute technical trading signals, monitor portfolio-level risk metrics, and track historical signal performance.

The system demonstrates production-grade financial data engineering practices by implementing structured ingestion, data validation gates, partition-optimized warehousing, scalable signal computation, and operational monitoring.

The platform simulates the backend infrastructure that could power financial analytics products used by active traders, quantitative analysts, and small investment firms.

---

# 2. Fictional Company

**FinStream Capital**

FinStream Capital is a fictional financial analytics startup that provides:

* Market signal monitoring
* Historical signal performance tracking
* Portfolio risk analytics
* Volatility regime monitoring

### Target Users

* Active retail traders managing $100K–$2M portfolios
* Boutique investment firms managing $5M–$250M AUM
* Quant-oriented traders and analysts
* Small funds lacking internal data infrastructure

---

# 3. Problem Statement

Active traders and small investment firms often rely on fragmented tools such as brokerage dashboards, charting software, and spreadsheets to monitor market signals and portfolio exposure.

These fragmented systems introduce several limitations:

1. **Lack of centralized signal monitoring**

   * Traders track dozens or hundreds of stocks manually.
   * Important technical signals such as moving average crossovers, RSI extremes, and volatility spikes may be missed.

2. **No historical signal performance intelligence**

   * Most platforms generate alerts but do not track how signals historically performed.
   * Users cannot measure win rates or average returns after signals.

3. **Limited portfolio-level risk visibility**

   * Traders lack consolidated metrics such as rolling volatility, maximum drawdown, Sharpe ratio, or sector concentration.

4. **Lack of operational data reliability**

   * Many systems lack defined data freshness SLAs.
   * Data pipelines are not monitored for reliability or validation errors.

FinStream addresses these challenges by building a structured, cloud-native data platform that centralizes market data ingestion, signal computation, portfolio risk analytics, and operational data engineering monitoring.

---

# 4. Quantified Business Context

Assume a small investment firm manages a $10M portfolio.

If:

* 30% of capital ($3M) is concentrated in a correlated sector
* Market volatility causes a 4% short-term drawdown

Potential loss:

$3,000,000 × 4% = $120,000

If centralized signal monitoring identifies elevated volatility or clustered bearish signals and reduces exposure by 25%, avoided loss becomes:

$750,000 × 4% = $30,000

This illustrates how better signal monitoring and risk analytics can improve portfolio risk management.

---

# 5. Data Engineering KPIs

To simulate a production financial data platform, FinStream defines operational SLAs.

### Data Freshness

Target: ≤ 10 minutes after each hourly market close

### Pipeline Reliability

Target: ≥ 99% Airflow DAG success rate

### Validation Integrity

Target: < 1% validation failure rate

### End-to-End Pipeline Latency

Target: < 15 minutes from ingestion to curated signal tables

### Query Cost Optimization

Target: ≥ 60% reduction in scanned bytes through partitioning and clustering 

### Transformation Runtime

Target: < 3 minutes for full dbt pipeline execution

### Scalability

Architecture designed to scale from 50 to 500 tickers without schema redesign.

---

# 6. Financial Data Engineering Lifecycle (FDEL)

The system follows the Financial Data Engineering Lifecycle framework :

1. Ingestion
2. Storage
3. Transformation & Delivery
4. Monitoring

---

# 7. Data Pipeline Architecture

## Hourly Data Flow

```
Yahoo Finance API
        ↓
Airflow DAG (hourly)
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

---

# 8. Data Pipeline Layers

## Raw Layer (Landing Zone)

Purpose:
Preserve immutable source data.

Characteristics:

* Exact API response
* Append-only
* Stored in Parquet format
* Schema-on-read 

Example structure:

```
gs://finstream/landing/prices/year=YYYY/month=MM/day=DD/hour=HH/
```

---

## Validated Layer

Purpose:
Filter invalid or corrupted records before warehouse ingestion.

Validation checks:

* Non-null symbol
* Valid timestamps
* Numeric OHLC values
* Non-negative volume
* No duplicate (symbol, timestamp)

Invalid records are stored in a quarantine dataset.

---

## Curated Layer (Data Warehouse)

Curated tables are analytics-ready.

Key tables:

### fact_prices

Clean hourly OHLCV market data.

Partition:
DATE(timestamp)

Cluster:
symbol

---

# 9. Transformation Layer (dbt)

dbt models compute financial indicators and signal events.

### Indicator Computation

Indicators include:

* EMA (12 and 26)
* RSI (14)
* Bollinger Bands
* Average True Range
* Volume spike detection

---

### Signal Event Table

fact_signals

Columns:

* signal_id
* symbol
* timestamp
* signal_type
* signal_strength
* volatility_regime
* volume_confirmation_flag

Example signals:

* EMA crossover
* RSI overbought / oversold
* Bollinger breakout
* volatility spike

---

# 10. Signal Performance Tracking

Table: fact_signal_performance

Tracks:

* entry_price
* price_after_1h
* price_after_1d
* price_after_3d
* return_1d
* return_3d
* win_flag

This allows computing historical signal win rates and average returns.

---

# 11. Portfolio Risk Analytics

Table: mart_portfolio_risk

Metrics include:

* Rolling 30-day volatility
* Maximum drawdown
* Rolling Sharpe ratio 
* Daily returns
* Sector exposure percentage
* Signal concentration risk

These metrics simulate portfolio risk monitoring capabilities.

---

# 12. Monitoring and Observability

## Pipeline Monitoring

Airflow tracks:

* DAG success rate
* Task retries
* pipeline duration
* failure causes

---

## Data Quality Monitoring

Table: mart_pipeline_quality

Tracks:

* total_records
* invalid_records
* duplicate_records
* validation_failure_rate

---

## Data Freshness Monitoring

Table: mart_freshness_monitor

Tracks:

* table_name
* max_timestamp
* lag_minutes
* SLA compliance

---

# 13. Dashboard

Streamlit dashboard includes:

### Categorical Visualization

Signal distribution by:

* signal_type
  or
* sector

---

### Time Series Visualization

One of the following:

* Rolling portfolio volatility
* Portfolio drawdown curve
* Signal frequency over time

These satisfy dashboard requirements .

---

# 14. Technology Stack

Cloud Platform
GCP

Data Lake
Google Cloud Storage

Data Warehouse
BigQuery

Orchestration
Apache Airflow

Transformation
dbt

Infrastructure as Code
Terraform

Dashboard
Streamlit

Optional ML
Scikit-learn / XGBoost

---

# 15. Future Extensions

The platform architecture is designed to support future AI capabilities such as:

* AI signal interpretation
* LLM-generated risk narratives
* RAG-based trading assistant
* ML-based signal confidence scoring

---

# 16. Key Engineering Principles

The platform follows best practices from financial data engineering systems:

* Immutable raw data storage
* Data validation gates
* Partition-optimized warehouse design
* Observability and SLAs
* Scalable architecture
* Cost-efficient analytics
