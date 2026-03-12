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

    return Path, pd, storage, yf


@app.cell
def _(Path):
    # Configuration
    TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    START_DATE = "2023-01-01"
    INTERVAL = "1h"

    OUTPUT_DIR = Path("../data/raw/market_data")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    BUCKET_NAME = "finstream-data-lake-845671354"
    local_file = OUTPUT_DIR / "market_data.parquet"
    return BUCKET_NAME, OUTPUT_DIR, START_DATE, TICKERS, local_file


@app.cell
def _(yf):
    # Fetch market data
    def fetch_market_data(tickers, start_date):
        """
        Pull stock data from Yahoo Finance
        """
        df = yf.download(
            tickers,
            start=start_date,
            group_by="ticker",
            auto_adjust=True,
            threads=True
        )
    
        return df

    return (fetch_market_data,)


@app.function
# Convert to normalize dataframe
def transform_data(df):
    """
    Convert multi-index dataframe to flat structure
    """
    df = df.stack(level=0).reset_index()

    df = df.rename(
        columns={
            "level_1": "ticker",
            "Date": "date"
        }
    )
    
    return df


@app.cell
def _(OUTPUT_DIR):
    # Save Parquet
    def save_parquet(df):
        """
        Save data locally as parquet
        """
        file_path = OUTPUT_DIR / "market_data.parquet"
    
        df.to_parquet(
            path = file_path,
            engine = "pyarrow",
            index = False
        )

        return(f"Saved parquet to {file_path}")

    return (save_parquet,)


@app.cell
def _(START_DATE, TICKERS, fetch_market_data, save_parquet):
    print("Fetching market data...")

    raw_df = fetch_market_data(TICKERS, START_DATE)

    print("Transforming data...")

    df = transform_data(raw_df)

    print("Saving parquet...")

    save_parquet(df)

    print("Pipeline complete!")
    return


@app.cell
def _(OUTPUT_DIR, pd):
    market_df = pd.read_parquet(OUTPUT_DIR / "market_data.parquet")
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
def _(Path, upload_to_gcs):
    def upload_market_data(
        local_path: Path,
        bucket_name: str
    ):
        """
        Upload market data parquet to raw layer
        """
        filename = local_path.name

        object_name = f"raw/market/data/{filename}"

        upload_to_gcs(
            bucket_name=bucket_name,
            local_file=str(local_path),
            object_name=object_name
        )

    return (upload_market_data,)


@app.cell
def _(BUCKET_NAME, local_file, upload_market_data):
    upload_market_data(local_file, BUCKET_NAME)
    return


if __name__ == "__main__":
    app.run()
