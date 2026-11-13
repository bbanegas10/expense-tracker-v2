# This file picks out expenses by date range and category

def filter_by_date(expenses, start_date, end_date):
    """Keep expenses between start_date and end_date (both included).

    Leave start_date or end_date empty ("") to skip that side.
    """
    results = []
    for expense in expenses:
        if start_date != "" and expense["date"] < start_date:
            continue  # too early
        if end_date != "" and expense["date"] > end_date:
            continue  # too late
        results.append(expense)
    return results


def filter_by_category(expenses, category):
    """Keep expenses that match the category (upper/lower case does not matter).

    Leave category empty ("") to keep everything.
    """
    if category == "":
        return list(expenses)

    results = []
    for expense in expenses:
        if expense["category"].lower() == category.lower():
            results.append(expense)
    return results

def filter_expenses(expenses, start_date="", end_date="", category=""):
    """Filter by date range AND category at the same time."""
    results = filter_by_date(expenses, start_date, end_date)
    results = filter_by_category(results, category)
    return results


def get_categories(expenses):
    """Return a sorted list of the different categories in use."""
    categories = []
    lowercase_seen = []
    for expense in expenses:
        name = expense["category"]
        if name.lower() not in lowercase_seen:
            lowercase_seen.append(name.lower())
            categories.append(name)
    categories.sort()
    return categories

