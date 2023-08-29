import pandas as pd
import numpy as np


def fe_perc_items(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the percentage of male items purchased"""
    assign_dict = {
        "perc_male_items": df.loc[:, "male_items"] / df.loc[:, "items"],
        "perc_female_items": df.loc[:, "female_items"] / df.loc[:, "items"],
        "perc_unisex_items": df.loc[:, "unisex_items"] / df.loc[:, "items"],
    }
    return df.assign(**assign_dict)


def fe_items_per_order(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the average number of items per order"""
    assign_dict = {"items_per_order": df.loc[:, "items"] / df.loc[:, "orders"]}
    return df.assign(**assign_dict)


def fe_days_between_first_and_last_order(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the number of days between the last and the first order"""
    assign_dict = {"days_between_first_and_last_order": df.loc[:, "days_since_first_order"] - df.loc[:, "days_since_last_order"]}
    return df.assign(**assign_dict)


def fe_rev_per_item(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the average revenue per item"""
    assign_dict = {"rev_per_item": df.loc[:, "revenue"] / df.loc[:, "items"]}
    return df.assign(**assign_dict)


def fe_rev_per_order(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the average revenue per order"""
    assign_dict = {"rev_per_order": df.loc[:, "revenue"] / df.loc[:, "orders"]}
    return df.assign(**assign_dict)


def fe_perc_cancels(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the percentage cancels"""
    assign_dict = {"perc_cancels": df.loc[:, "cancels"] / df.loc[:, "orders"]}
    return df.assign(**assign_dict)


def fe_perc_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the percentage returns"""
    assign_dict = {"perc_returns": df.loc[:, "returns"] / df.loc[:, "orders"]}
    return df.assign(**assign_dict)