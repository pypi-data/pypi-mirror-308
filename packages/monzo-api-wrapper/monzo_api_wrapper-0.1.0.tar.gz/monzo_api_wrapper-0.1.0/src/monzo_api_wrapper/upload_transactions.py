from typing import Optional

import pandas as pd

from monzo_api_wrapper.utils import sql_templates
from monzo_api_wrapper.utils.custom_logger import CustomLogger, loggable
from monzo_api_wrapper.utils.db import Db

logger = CustomLogger.get_logger()


@loggable
def _get_db_transactions(db: Db, table: str) -> pd.DataFrame | None:
    """Fetch transactions from the database.

    Args:
        db (Db): Database connection object.
        table (str): Name of the table to fetch transactions from.

    Returns:
        pd.DataFrame | None: DataFrame containing the transactions fetched from the database.

    """
    return db.query(
        sql=sql_templates.exists.format(table=table),
        return_data=True,
    )


@loggable
def get_new_transactions(db: Db, table: str, fetched_transactions: pd.DataFrame) -> pd.DataFrame:
    """Identify new transactions that are not present in the database.

    Args:
        db (Db): Database connection object.
        table (str): Name of the table to check transactions against.
        fetched_transactions (pd.DataFrame): DataFrame containing fetched transactions.

    Returns:
        pd.DataFrame: DataFrame containing new transactions to be uploaded.

    """
    db_transactions = _get_db_transactions(db, table)
    db_ids_lst = db_transactions["id"].tolist() if db_transactions is not None else []

    new_transaction_ids = [
        item for item in fetched_transactions["id"].tolist() if item not in db_ids_lst
    ]

    return fetched_transactions[fetched_transactions["id"].isin(new_transaction_ids)].reset_index(
        drop=True
    )


@loggable
def get_changed_transaction_ids(
    db: Db, table: str, fetched_transactions: pd.DataFrame
) -> Optional[list[str]]:
    """Identify transactions that have changed based on a set of columns.

    Args:
        db (Db): Database connection object.
        table (str): Name of the table to check transactions against.
        fetched_transactions (pd.DataFrame): DataFrame containing fetched transactions.

    Returns:
       Optional[List[str]]: List of transactions IDs that have changed, or None if no changes are found.

    """
    compare_transaction_cols = ["id", "description", "amount", "category", "notes", "timestamp"]

    logger.debug("Getting existing transactions from database")
    db_transactions = _get_db_transactions(db, table)

    if db_transactions is None:
        return None

    logger.debug("Standardizing date and amount columns for comparison")
    db_transactions["date"] = pd.to_datetime(db_transactions["date"])
    db_transactions["amount"] = db_transactions["amount"].round(2)
    fetched_transactions["date"] = pd.to_datetime(fetched_transactions["date"])

    logger.debug("Creating comparable subsets of database and fetched transactions")
    db_transactions_subset = db_transactions[compare_transaction_cols]
    fetched_transactions_subset = (
        fetched_transactions[compare_transaction_cols]
        .sort_values("timestamp")
        .reset_index(drop=True)
    )

    filtered_db_transactions_subset = (
        db_transactions_subset[db_transactions_subset["id"].isin(fetched_transactions["id"])]
        .sort_values("timestamp")
        .reset_index(drop=True)
    )

    logger.debug("Comparing transactions to identify differences")
    # Compare each row across all columns (excluding 'id')
    differences = (
        fetched_transactions_subset[compare_transaction_cols[1:]]
        .ne(filtered_db_transactions_subset[compare_transaction_cols[1:]])
        .any(axis=1)
    )

    changed_ids = fetched_transactions_subset.loc[differences, "id"].to_list()
    return changed_ids if changed_ids else None
