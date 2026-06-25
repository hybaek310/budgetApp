"""Tests for budget.core."""

import csv
from pathlib import Path

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    monthly_summary,
)


def load_step2_transactions() -> list[dict[str, object]]:
    csv_path = Path("data/step2_transactions.csv")
    with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        return [
            {**row, "amount": int(row["amount"])}
            for row in csv.DictReader(csv_file)
        ]


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


def test_get_balance_returns_zero_for_empty_transactions() -> None:
    assert get_balance([]) == 0.0


def test_get_balance_returns_positive_sum_for_income_only() -> None:
    transactions = [
        {
            "date": "2026-02-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4358625,
            "memo": "",
        },
        {
            "date": "2026-02-24",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 199790,
            "memo": "",
        },
    ]

    assert get_balance(transactions) == 4558415.0


def test_get_balance_returns_negative_sum_for_expenses_only() -> None:
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -65990,
            "memo": "카드결제",
        },
    ]

    assert get_balance(transactions) == -1045786.0


def test_get_balance_returns_net_sum_for_mixed_transactions() -> None:
    transactions = [
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
        {
            "date": "2026-01-16",
            "type": "지출",
            "category": "교통",
            "description": "지하철",
            "amount": -90127,
            "memo": "카드결제",
        },
    ]

    assert get_balance(transactions) == 45414.0


def test_get_balance_matches_step2_transactions_csv_total() -> None:
    transactions = load_step2_transactions()

    assert get_balance(transactions) == 24285027.0


def test_filter_by_category_matches_real_category_from_step2_csv() -> None:
    transactions = load_step2_transactions()

    result = filter_by_category(transactions, "여행")

    assert len(result) == 6
    assert all(transaction["category"] == "여행" for transaction in result)


def test_filter_by_category_is_case_insensitive() -> None:
    transactions = [
        {
            "date": "2026-02-01",
            "type": "지출",
            "category": "Food",
            "description": "Lunch",
            "amount": -12000,
            "memo": "",
        }
    ]

    result = filter_by_category(transactions, "food")

    assert len(result) == 1
    assert result[0]["category"] == "Food"


def test_filter_by_category_returns_empty_list_for_unknown_category() -> None:
    transactions = load_step2_transactions()

    result = filter_by_category(transactions, "반려동물")

    assert result == []


def test_filter_by_category_result_is_independent_from_original_list() -> None:
    transactions = load_step2_transactions()

    result = filter_by_category(transactions, "급여")
    result[0]["category"] = "변경됨"

    assert transactions[0]["category"] != "변경됨"


def test_monthly_summary_groups_income_expense_and_net_by_month() -> None:
    transactions = [
        {
            "date": "2026-01-07",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 3500000,
            "memo": "1월급여",
        },
        {
            "date": "2026-01-10",
            "type": "지출",
            "category": "교통",
            "description": "지하철",
            "amount": -1500,
            "memo": "",
        },
        {
            "date": "2026-02-24",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 199790,
            "memo": "",
        },
    ]

    result = monthly_summary(transactions)

    assert result == {
        "2026-01": {"income": 3500000, "expense": -1500, "net": 3498500},
        "2026-02": {"income": 199790, "expense": 0, "net": 199790},
    }


def test_monthly_summary_returns_empty_dict_for_empty_transactions() -> None:
    assert monthly_summary([]) == {}


def test_monthly_summary_matches_step2_transactions_csv() -> None:
    transactions = load_step2_transactions()

    result = monthly_summary(transactions)

    assert result == {
        "2026-01": {"income": 135541, "expense": -3608605, "net": -3473064},
        "2026-02": {"income": 15871780, "expense": -3333340, "net": 12538440},
        "2026-03": {"income": 17239079, "expense": -2019428, "net": 15219651},
    }
