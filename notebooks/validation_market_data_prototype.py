import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import os
    import pandas as pd
    from pathlib import Path

    return Path, pd


@app.cell
def _(Path):
    OUTPUT_DIR = Path("./data/raw/market_prices")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return (OUTPUT_DIR,)


@app.cell
def _(OUTPUT_DIR, pd):
    market_df = pd.read_parquet(OUTPUT_DIR / "year=2026/month=03/day=10/hour=13/part-0000.parquet")
    market_df.head()
    return (market_df,)


@app.cell
def _(market_df):
    market_df.columns
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Schema Validation
    """)
    return


@app.cell
def _(pd):
    def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure dataframe contains expected schema.
        """

        # expected columns
        expected_columns = [
            "timestamp_utc", 
            "ticker", 
            "open", 
            "high", 
            "low", 
            "close", 
            "volume"
        ]

        # missing cols
        missing_cols = set(expected_columns) - set(df.columns)

        # raise ValueError
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")

        return df

    return (validate_schema,)


@app.cell
def _(market_df, validate_schema):
    test_df = market_df.copy()
    validate_schema(test_df)
    return (test_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Missing Value Detection
    """)
    return


@app.cell
def _(pd):
    def detect_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """
        Flag any rows with null values.
        """

        missing_mask = df[
            ["timestamp_utc", "ticker", "open", "high", "low", "close", "volume"]
            ].isnull().any(axis=1)

        df.loc[missing_mask, "validation_errors"] += "missing_value;"

        return df

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Duplicate Timestamp Detection
    """)
    return


@app.cell
def _(pd):
    def detect_duplicate_timestamps(df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect duplicate (timestamp, ticker) paris.
        """

        dup_mask = df.duplicated(
            subset=["timestamp_utc", "ticker"],
            keep=False
        )

        df.loc[dup_mask, "validation_errors"] += "duplicate_timestamp;"

        return df

    return (detect_duplicate_timestamps,)


@app.cell
def _(detect_duplicate_timestamps, test_df):
    detect_duplicate_timestamps(test_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## OHLC Logic Validation
    """)
    return


@app.cell
def _(pd):
    def validate_ohlc_logic(df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate OHLC price relationships.
        """

        ohlc_mask = (
            (df["high"] < df["low"]) |
            (df["high"] < df["open"]) |
            (df["high"] < df["close"]) |
            (df["low"] > df["open"]) |
            (df["low"] > df["close"]) |
            (df["volume"] < 0)
        )

        df.loc[ohlc_mask, "validation_errors"] += "ohlc_violation;"

        return df

    return (validate_ohlc_logic,)


@app.cell
def _(test_df, validate_ohlc_logic):
    validate_ohlc_logic(test_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Price Sanity Validation
    """)
    return


@app.function
def validate_price_sanity(df):

    sanity_mask = (
        (df["open"] <= 0) |
        (df["high"] <= 0) |
        (df["low"] <= 0) |
        (df["close"] <= 0) |
        (df["volume"] <= 0)
    )

    df.loc[sanity_mask, "validation_errors"] += "ohlc_violation;"

    return df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Main Validation Pipeline
    """)
    return


@app.cell
def _(validate_schema):
    def validate_market_data(df):
        df = validate_schema(df)

        df["validation_errors"] = ""

        # Missing Values
        missing_mask = df[
            ["timestamp_utc", "ticker", "open", "high", "low", "close", "volume"]].isnull().any(axis=1)

        df.loc[missing_mask, "validation_errors"] += "missing_value;"

        # Duplicate Timestamps
        dup_mask = df.duplicated(
            subset=["timestamp_utc", "ticker"],
            keep=False
        )

        df.loc[dup_mask, "validation_errors"] += "duplicate_timestamp;"

        # OHLC Logic
        ohlc_mask = (
            (df["high"] < df["low"]) |
            (df["high"] < df["open"]) |
            (df["high"] < df["close"]) |
            (df["low"] > df["open"]) |
            (df["low"] > df["close"]) |
            (df["volume"] < 0)
        )

        df.loc[ohlc_mask, "validation_errors"] += "ohlc_violation;"

        # Price Sanity Logic
        sanity_mask = (
            (df["open"] <= 0) |
            (df["high"] <= 0) |
            (df["low"] <= 0) |
            (df["close"] <= 0) |
            (df["volume"] <= 0)
        )

        df.loc[sanity_mask, "validation_errors"] += "ohlc_violation;"

        # Split dataset (valid | invalid)
        valid_df = df[df["validation_errors"] == ""].copy()
        invalid_df = df[df["validation_errors"] != ""].copy()

        return valid_df, invalid_df

    return (validate_market_data,)


@app.cell
def _(test_df, validate_market_data):
    valid_df, invalid_df = validate_market_data(test_df)

    print("Validation results")

    print(f"Valid records:", len(valid_df))
    print(f"Invalid records:", len(invalid_df))
    return invalid_df, valid_df


@app.cell
def _(invalid_df):
    invalid_df[["timestamp_utc", "ticker", "validation_errors"]].head()
    return


@app.cell
def _(valid_df):
    valid_df[["timestamp_utc", "ticker", "validation_errors"]].head()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
