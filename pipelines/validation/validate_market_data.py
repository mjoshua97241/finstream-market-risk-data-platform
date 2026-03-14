import pandas as pd
from pathlib import Path

# Schema Validation

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

## Missing Value Detection

def detect_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag any rows with null values.
    """

    missing_mask = df[
        ["timestamp_utc", "ticker", "open", "high", "low", "close", "volume"]
        ].isnull().any(axis=1)

    df.loc[missing_mask, "validation_errors"] += "missing_value;"

    return df

## Duplicate Timestamp Detection

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

## OHLC Logic Validation

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

## Price Sanity Validation

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

## Main Validation Pipeline

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