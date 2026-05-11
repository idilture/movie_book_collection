from datetime import date


def validate_rating(rating):
    if rating is None or rating == "":
        return True

    try:
        rating = int(rating)
        return 1 <= rating <= 5
    except ValueError:
        return False


def validate_year(year):
    if year is None or year == "":
        return True

    try:
        year = int(year)
        return 1450 <= year <= date.today().year
    except ValueError:
        return False


def calculate_average_rating(items):
    ratings = []

    for item in items:
        if item["rating"] is not None:
            ratings.append(item["rating"])

    if len(ratings) == 0:
        return 0

    return sum(ratings) / len(ratings)


def count_items_by_status(items, status):
    count = 0

    for item in items:
        if item["status"] == status:
            count += 1

    return count


def count_items_by_type(items, item_type):
    count = 0

    for item in items:
        if item["item_type"] == item_type:
            count += 1

    return count
