import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from logic import (
    calculate_average_rating,
    count_items_by_status,
    count_items_by_type,
    validate_rating,
    validate_year,
)


def test_validate_rating_accepts_valid_rating():
    assert validate_rating("1") is True
    assert validate_rating("3") is True
    assert validate_rating("5") is True


def test_validate_rating_rejects_invalid_rating():
    assert validate_rating("0") is False
    assert validate_rating("6") is False
    assert validate_rating("abc") is False


def test_validate_rating_allows_empty_rating():
    assert validate_rating("") is True
    assert validate_rating(None) is True


def test_validate_year_accepts_valid_year():
    assert validate_year("2000") is True
    assert validate_year("2020") is True


def test_validate_year_rejects_invalid_year():
    assert validate_year("1800") is False
    assert validate_year("2026") is False
    assert validate_year("abc") is False


def test_validate_year_allows_empty_year():
    assert validate_year("") is True
    assert validate_year(None) is True


def test_calculate_average_rating():
    items = [
        {"rating": 5},
        {"rating": 3},
        {"rating": 4},
    ]

    assert calculate_average_rating(items) == 4


def test_calculate_average_rating_ignores_none_values():
    items = [
        {"rating": 5},
        {"rating": None},
        {"rating": 3},
    ]

    assert calculate_average_rating(items) == 4


def test_calculate_average_rating_returns_zero_when_no_rating():
    items = [
        {"rating": None},
        {"rating": None},
    ]

    assert calculate_average_rating(items) == 0


def test_count_items_by_status():
    items = [
        {"status": "Completed"},
        {"status": "In Progress"},
        {"status": "Completed"},
    ]

    assert count_items_by_status(items, "Completed") == 2
    assert count_items_by_status(items, "In Progress") == 1


def test_count_items_by_type():
    items = [
        {"item_type": "Movie"},
        {"item_type": "Book"},
        {"item_type": "Movie"},
    ]

    assert count_items_by_type(items, "Movie") == 2
    assert count_items_by_type(items, "Book") == 1