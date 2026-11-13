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



