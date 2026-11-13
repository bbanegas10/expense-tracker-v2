# This file creates one expense.
# last commit would break when I would type anything other than a number
# An expense is stored as a dictionary like this:
# {"date": "2026-11-08", "category": "Food", "description": "Lunch", "amount": 12.5}
#safety nets needed to be addead (code kept breaking)

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"


def is_valid_date(date_text):
    """Return True if date_text looks like YYYY-MM-DD, otherwise False."""
    try:
        datetime.strptime(date_text, DATE_FORMAT)
        return True
    except ValueError:
        return False


def make_expense(date_text, category, description, amount_text):
    """Check the values and return a new expense dictionary.

    Raises a ValueError with a helpful message if something is wrong.
    """
    date_text = date_text.strip()
    category = category.strip()
    description = description.strip()

    if not is_valid_date(date_text):
        raise ValueError("Date must be in the format YYYY-MM-DD, like 2026-11-08.")

    if category == "":
        raise ValueError("Category cannot be empty.")

    try:   
        amount = float(amount_text.replace("$", "").replace(",", ""))
    except ValueError:
        raise ValueError("Amount must be a number, like 12.50.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    
    
    # round to 2 decimal places (cents)
    amount = round(amount, 2)

    expense = {
        "date": date_text,
        "category": category,
        "description": description,
        "amount": amount,
    }
    return expense