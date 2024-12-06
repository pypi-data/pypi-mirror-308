from __future__ import annotations

import os
from typing import Optional

import pandas as pd
import scipy.io as spio
from sklearn.datasets import fetch_openml
from ucimlrepo import fetch_ucirepo

from .. import dataset2openml_id, dataset2path, dataset2uci_id


def load_tabular_dataset(
    dataset_name: str,
    target_col: Optional[str] = None,
) -> dict:
    """Load a tabular dataset.

    Args:
        dataset_name (str): Name of the dataset to load.
        target_col (Optional[str], optional): Name of the target column.

    Raises:
        ValueError: If the dataset is not recognised.

    Returns:
        dict: Dictionary containing the features and target variables.
    """
    # ===== Load the dataset =====
    dataset_source = get_dataset_source(dataset_name)
    if dataset_source == 'openml':
        data_dict = load_openml_dataset(dataset_name)
    elif dataset_source == 'uci':
        data_dict = load_uci_dataset(dataset_name)
    elif dataset_source == 'local':
        data_dict = load_local_dataset(dataset_name, target_col)
    else:
        raise ValueError(f"Dataset {dataset_name} not recognised.")

    return data_dict


def get_dataset_source(dataset_name: str) -> str:
    """Get the source of dataset.

    Args:
        dataset_name (str): Name of the dataset.

    Returns:
        str: Type of dataset (openml or local).
    """
    if dataset_name in dataset2openml_id.keys():
        dataset_type = 'openml'
    elif dataset_name in dataset2uci_id.keys():
        dataset_type = 'uci'
    elif os.path.exists(dataset_name) or dataset_name in dataset2path.keys():
        dataset_type = 'local'
    else:
        raise ValueError(f"Dataset {dataset_name} not recognised.")

    return dataset_type


def load_openml_dataset(dataset_name: str) -> dict:
    """Load a dataset from OpenML.

    Args:
        dataset_name (str): Name of the dataset to load.

    Returns:
        dict: Dictionary containing the features and target variables.
    """
    # ===== Load the dataset with id=====
    data_loaded = fetch_openml(data_id=dataset2openml_id[dataset_name], as_frame=True)
    # ===== Get the features and target variables =====
    X_df = data_loaded.data
    y_s = data_loaded.target

    return {
        'X': X_df,
        'y': y_s,
    }


def load_uci_dataset(dataset_name: str) -> dict:

    # ===== Load the dataset with id=====
    data_loaded = fetch_ucirepo(id=dataset2uci_id[dataset_name])
    # ===== Get the features and target variables =====
    X_df = data_loaded.data.features
    y_s = data_loaded.data.targets.iloc[:, 0]

    return {
        'X': X_df,
        'y': y_s,
    }


def load_local_dataset(
    dataset_name: str,
    target_col: Optional[str] = None,
) -> dict:
    """Load a dataset from a local file.

    Args:
        dataset_name (str): Name of the dataset to load.
        target_col (Optional[str], optional): Name of the target column.

    Returns:
        dict: Dictionary containing the features and target variables.
    """
    # ===== Transform the dataset name to the path =====
    if dataset_name in dataset2path.keys():
        dataset_name = dataset2path[dataset_name]

    if 'csv' in dataset_name:
        data_df = pd.read_csv(dataset_name)
        # === Ignore the first column if it is an index ===
        if 'Unnamed: 0' in data_df.columns:
            data_df = data_df.drop('Unnamed: 0', axis=1)
        # === Drop the last column as the target ===
        target_col = target_col if target_col is not None else data_df.columns[-1]
        X_df = data_df.drop(target_col, axis=1)
        y_s = data_df[target_col]
    elif 'mat' in dataset_name:
        data = spio.loadmat(dataset_name)
        X_df = pd.DataFrame(data['X'])
        y_s = pd.Series(data['Y'][:, 0])
    else:
        raise NotImplementedError("File format not recognised for local dataset.")

    return {
        'X': X_df,
        'y': y_s,
    }
