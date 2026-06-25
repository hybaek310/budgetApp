"""Tests for budget.core."""

from budget.core import add_transaction


def test_add_transaction_increases_length() -> None:
    transactions: list[dict[str, object]] = []
    transaction = {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1

