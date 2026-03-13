
__generated_with = "0.20.4"

# %%
import marimo as mo

# %%
import os
import yfinance as yf
import pandas as pd
from pathlib import Path
from google.cloud import storage
from datetime import datetime

# %%
# Configuration
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
START_DATE = "2026-03-10"
INTERVAL = "1h"

OUTPUT_DIR = Path("./data/raw/market_prices")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BUCKET_NAME = "finstream-data-lake-845671354"

# %%
# Fetch market data
def fetch_market_data(tickers, start_date, interval):
    """
    Pull stock data from Yahoo Finance
    """
    df = yf.download(
        tickers,
        start=start_date,
        interval=interval,
        group_by="ticker",
        auto_adjust=True,
        threads=True
    )

    return df

# %%
# Convert to normalize dataframe
def transform_data(df):
    """
    Convert multi-index dataframe to flat structure
    """
    df = df.stack(level=0).reset_index()

    df = df.rename(
        columns={
            "Date": "timestamp_utc",
            "Datetime": "timestamp_utc",
            "level_1": "ticker",
            "Ticker": "ticker",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }
    )

    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)

    df = df[
        [
            "timestamp_utc",
            "ticker",
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]
    ]

    df = df.sort_values(["timestamp_utc", "ticker"])

    return df

# %%
def write_partitioned_parquet(df, base_dir: Path):
    """
    Write parquet files partitioned by year/month/day/hour.
    """
    df["year"] = df["timestamp_utc"].dt.year
    df["month"] = df["timestamp_utc"].dt.month
    df["day"] = df["timestamp_utc"].dt.day
    df["hour"] = df["timestamp_utc"].dt.hour

    for keys, partitioned_df in df.groupby(["year", "month", "day", "hour"]):

        year, month, day, hour = keys

        partition_path = (
            base_dir /
            f"year={year}" /
            f"month={month:02}" /
            f"day={day:02}" /
            f"hour={hour:02}"
        )

        partition_path.mkdir(parents=True, exist_ok=True)

        file_path = partition_path / "part-0000.parquet"

        # drop date column and save to parquet
        partitioned_df.drop(columns=["year", "month", "day", "hour"]).to_parquet(
            file_path,
            engine="pyarrow",
            compression="snappy",
            index=False
        )

        # print
        print(f"Saved partition: {file_path}")

# %%
market_df = pd.read_parquet(OUTPUT_DIR / "year=2026/month=03/day=10/hour=13/part-0000.parquet")
market_df.head()

# %%
def upload_to_gcs(
    bucket_name: str,
    local_file: str,
    object_name: str
):
    """
    Upload file to Google Cloud Storage.

    Args:
        bucket_name: GCS bucket name
        local_file: local file path
        object_name: path inside GCS bucket
    """

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

    print(f"Uploaded {local_file} → gs://{bucket_name}/{object_name}")

# %%
def upload_directory_to_gcs(bucket_name: str, local_dir: Path):

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for file in local_dir.rglob("*.parquet"):
        relative_path = file.relative_to(local_dir)

        object_name = f"raw/market_prices/{relative_path}"

        blob = bucket.blob(str(object_name))

        blob.upload_from_filename(file)

        print(f"Uploaded {file} → gs://{bucket_name}/{object_name}")

# %%
print("Fetching market data...")

raw_df = fetch_market_data(TICKERS, START_DATE, INTERVAL)

print("Transforming data...")

df = transform_data(raw_df)

print("Saving parquet...")

write_partitioned_parquet(df, OUTPUT_DIR)

print("Uploading partitions to GCS...")

upload_directory_to_gcs(BUCKET_NAME, OUTPUT_DIR)

print("Ingestion complete!")
