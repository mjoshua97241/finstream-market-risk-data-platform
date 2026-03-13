import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import os
    import yfinance as yf
    import pandas as pd
    from pathlib import Path
    from google.cloud import storage
    from datetime import datetime

    return Path, pd, storage, yf


@app.cell
def _(Path):
    # Configuration
    TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    START_DATE = "2026-03-10"
    INTERVAL = "1h"

    OUTPUT_DIR = Path("./data/raw/market_prices")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    BUCKET_NAME = "finstream-data-lake-845671354"
    return BUCKET_NAME, INTERVAL, OUTPUT_DIR, START_DATE, TICKERS


@app.cell
def _(yf):
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

    return (fetch_market_data,)


@app.cell
def _(pd):
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

    return (transform_data,)


@app.cell
def _(Path):
    def write_partitioned_parquet(df, base_dir: Path):
        """
        Write parquet files partitioned by date
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

    return (write_partitioned_parquet,)


@app.cell
def _(
    INTERVAL,
    OUTPUT_DIR,
    START_DATE,
    TICKERS,
    fetch_market_data,
    transform_data,
    write_partitioned_parquet,
):
    print("Fetching market data...")

    raw_df = fetch_market_data(TICKERS, START_DATE, INTERVAL)

    print("Transforming data...")

    df = transform_data(raw_df)

    print("Saving parquet...")

    write_partitioned_parquet(df, OUTPUT_DIR)

    print("Pipeline complete!")
    return


@app.cell
def _(OUTPUT_DIR, pd):
    market_df = pd.read_parquet(OUTPUT_DIR / "year=2026/month=03/day=10/hour=13/part-0000.parquet")
    market_df.head()
    return


@app.cell
def _(storage):
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

    return (upload_to_gcs,)


@app.cell
def _(BUCKET_NAME, OUTPUT_DIR, upload_to_gcs):
    for file in OUTPUT_DIR.rglob("*.parquet"):
        relative_path = file.relative_to(OUTPUT_DIR)

        object_name = f"raw/market_prices/{relative_path}"

        upload_to_gcs(
            bucket_name=BUCKET_NAME,
            local_file=str(file),
            object_name=object_name
        )
    return


if __name__ == "__main__":
    app.run()
