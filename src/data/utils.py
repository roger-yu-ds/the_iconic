from __future__ import annotations
import os
from dotenv import load_dotenv, find_dotenv
from zipfile import ZipFile
from pathlib import (
    Path,
    WindowsPath,
    PosixPath,
)
from hashlib import sha256
import pandas as pd
import seaborn as sns


def sha256_text(input: str) -> str:
    """Applies SHA-256 hash algorithm on `input`, returns the hashed value."""
    return sha256(input.encode("utf-8")).hexdigest()


def extract_file(filepath: Path, target_dir: Path, pwd: str) -> None:
    """Extracts `path` and dumps the contents into `target_dir`.
    """    
    with ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(target_dir, pwd=pwd.encode())


def plot_two_histograms(
    df: pd.DataFrame, 
    cols: list[str],
    id_vars: list[str] = ["customer_id"],
) -> sns.axisgrid.FacetGrid:
    """Plot two histograms on the same axes."""
    plot_df = pd.melt(frame=df.loc[:, id_vars + cols],
                  var_name="first_last",
                  value_name="n_days",
                  id_vars=id_vars,)
    fg = sns.displot(
        data=plot_df,
        x="n_days",
        hue="first_last",
        kind="hist",
        aspect=2,
    )
    
    return fg


def diff_agg_const(df: pd.DataFrame,
                   aggregate_col: str, 
                   constituent_cols: list[str]) -> pd.Series:
    """Compares an aggregate column with the sum of its constituents."""
    diff = df.loc[:, aggregate_col] - df.loc[:, constituent_cols].sum(axis="columns")
    return diff


def write_customer_ids_to_drop(df: pd.DataFrame, filepath: Path, reason: str = None) -> None:
    """Writes to disk the `customer_id`s to drop.
    If a file already exists, then just write the new `customer_id`s.
    """
    index_col = "idx"
    key_col = "customer_id"
    try:
        customer_ids = df.loc[:, key_col]
    except KeyError:
        print(f"`df` is missing `{key_col}`.")

    if filepath.exists():
        existing_df = pd.read_csv(filepath, index_col=index_col)
        new_customer_ids = set(customer_ids) - set(existing_df.loc[:, key_col])
        new_df = (
            pd.DataFrame(new_customer_ids, columns=[key_col])
            .assign(reason = reason)
        )
        result_df = pd.concat([existing_df, new_df])
    else:
        result_df = (
            df.loc[:, [key_col]]
            .drop_duplicates(subset=[key_col])
            .assign(reason = reason)
        )
    result_df.to_csv(filepath, index_label=index_col)
    

def write_cols_to_drop(cols: list[str], filepath: Path, reason: str = None) -> None:
    """Writes to disk the columns to drop.
    If a file already exists, then just write the new columns.
    """
    df = pd.DataFrame({"feature": cols, "reason": reason})
    if filepath.exists():
        existing_df = pd.read_csv(filepath)
        df = df.query("feature not in @existing_df.feature")
    header = not filepath.exists()
    df.to_csv(filepath, mode="a", index=False, header=header)


def save_preds(
    preds: np.ndarray, 
    keys: pd.Series, 
    model_name: str,
    filename: str = "clusters.csv",
    save_dir: Path = None,
) -> None:
    """Matches the preSaves the predictions to disk."""
    if save_dir is None:
        save_dir = Path(find_dotenv()).parent / "reports/artifacts"
    filepath = save_dir / filename
    if filepath.exists():
        pred_df = pd.read_csv(filepath)
    else:
        pred_df = keys.to_frame()
    pred_df.loc[:, model_name] = preds
    pred_df.to_csv(filepath, index=False)


def highlight_max(data, color='yellow'):
    '''
    highlight the maximum in a Series or DataFrame
    From https://stackoverflow.com/a/45606572
    '''
    attr = 'background-color: {}'.format(color)
    #remove % and cast to float
    data = data.replace('%','', regex=True).astype(float)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_max = data == data.max()
        return [attr if v else '' for v in is_max]
    else:  # from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index=data.index, columns=data.columns)
