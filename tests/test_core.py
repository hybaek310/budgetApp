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


def test_add_transaction_saves_negative_amount_for_expense() -> None:
    transactions: list[dict[str, object]] = []
    transaction = {
        "date": "2026-01-10",
        "type": "지출",
        "category": "교통",
        "description": "지하철",
        "amount": -1500,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == -1500
    assert result[0]["type"] == "지출"
    assert result[0]["category"] == "교통"


def test_add_transaction_saves_positive_amount_for_income() -> None:
    transactions: list[dict[str, object]] = []
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == 3500000
    assert result[0]["type"] == "수입"
    assert result[0]["category"] == "급여"


def test_add_transaction_allows_empty_description() -> None:
    transactions: list[dict[str, object]] = []
    transaction = {
        "date": "2026-01-12",
        "type": "지출",
        "category": "식비",
        "description": "",
        "amount": -5800,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["description"] == ""
