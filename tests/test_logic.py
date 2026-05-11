from datetime import date

from logic import calculate_average_rating, count_items_by_status, count_items_by_type
from logic import validate_rating, validate_year


def test_rating_between_1_and_5_is_valid():
    assert validate_rating("1") == True
    assert validate_rating("5") == True



def test_rating_0_is_invalid():
    assert validate_rating("0") == False


def test_rating_6_is_invalid():
    assert validate_rating("6") == False


def test_empty_rating_is_valid():
    assert validate_rating("") == True



def test_year_is_valid():
    assert validate_year("2000") == True



def test_future_year_is_invalid():
    future_year = date.today().year + 1
    assert validate_year(str(future_year)) == False


def test_average_rating_is_calculated():
    items = [
        {"rating": 5},
        {"rating": 3},
        {"rating": None}
    ]

    assert calculate_average_rating(items) == 4


def test_count_items_by_status():
    items = [
        {"status": "Completed"},
        {"status": "In Progress"},
        {"status": "Completed"}
    ]

    assert count_items_by_status(items, "Completed") == 2


def test_count_items_by_type():
    items = [
        {"item_type": "Movie"},
        {"item_type": "Book"},
        {"item_type": "Book"}
    ]

    assert count_items_by_type(items, "Book") == 2
