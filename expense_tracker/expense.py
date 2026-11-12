# This file creates one expense.


def make_expense(date_text, category, description, amount_text):
    expense = {
        "date": date_text,
        "category": category,
        "description": description,
        "amount": float(amount_text),
    }
  