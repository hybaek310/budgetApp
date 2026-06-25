"""Core business logic for the CSV-based budget CLI app."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def add_transaction(
    transactions: list[dict[str, Any]],
    transaction: dict[str, Any],
) -> list[dict[str, Any]]:
    """Add a transaction to the transaction list."""
    new_transaction = {
        "date": transaction["date"],
        "type": transaction["type"],
        "category": transaction["category"],
        "description": transaction["description"],
        "amount": transaction["amount"],
        "memo": transaction["memo"],
    }
    return [*transactions, new_transaction]


def get_balance(transactions: list[dict[str, Any]]) -> float:
    """Return the net balance for the given transactions."""
    return float(sum(transaction["amount"] for transaction in transactions))


def filter_by_category(
    transactions: list[dict[str, Any]],
    category: str,
) -> list[dict[str, Any]]:
    """Return transactions that match the given category."""
    target_category = category.casefold()
    return [
        transaction.copy()
        for transaction in transactions
        if str(transaction["category"]).casefold() == target_category
    ]


def load_transactions_from_csv(
    csv_path: str | Path,
) -> list[dict[str, Any]]:  # pragma: no cover
    """Load transactions from a CSV file."""
    pass


def monthly_summary(
    transactions: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    """Return monthly income, expense, and net summary."""
    summary: dict[str, dict[str, int]] = {}
    for transaction in transactions:
        month = str(transaction["date"])[:7]
        amount = int(transaction["amount"])
        if month not in summary:
            summary[month] = {"income": 0, "expense": 0, "net": 0}
        if amount > 0:
            summary[month]["income"] += amount
        else:
            summary[month]["expense"] += amount
        summary[month]["net"] += amount
    return summary
