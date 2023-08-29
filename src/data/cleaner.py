from __future__ import annotations
from zipfile import ZipFile
from pathlib import (
    Path,
    WindowsPath,
    PosixPath,
)
from hashlib import sha256
import pandas as pd
import numpy as np
import seaborn as sns


def convert_hours_to_days(df: pd.DataFrame) -> pd.DataFrame:
    """Converts hours since last purchase to days since last purchase.
    This affects the field `days_since_last_order`/
    """
    return df.assign(days_since_last_order = lambda df: df.loc[:, "days_since_last_order"]/24)


def fix_average_discount_used(df: pd.DataFrame) -> pd.DataFrame:
    """Divides `average_discount_used` by 10000
    """
    return df.assign(average_discount_used = lambda df: df.loc[:, "average_discount_used"]/10000)


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate the rows.
    """
    return df.drop_duplicates()


def drop_features(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Drops the `cols`"""
    return df.drop(columns=cols)


def drop_rows(df: pd.DataFrame, items_to_drop: iterable[str], key_col: str = "customer_id") -> pd.DataFrame:
    """Drops the `cols`"""
    return df.query(f"{key_col}  not in @items_to_drop")