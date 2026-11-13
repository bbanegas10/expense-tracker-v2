# This file picks out expenses by date range 


def filter_by_date(expenses, start_date, end_date):
    """Keep expenses between start_date and end_date."""
    results = []
    for expense in expenses:
        if start_date != "" and expense["date"] < start_date:
            continue  # too early
        if end_date != "" and expense["date"] > end_date:
            continue  # too late
        results.append(expense)
    return results