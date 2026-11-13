# This file prints expenses as a table.


def get_total(expenses):
    """Add up the amount of every expense."""
    total = 0
    for expense in expenses:
        total = total + expense["amount"]
    


def print_expenses(expenses):
    """Print the expenses in a table, sorted by date, with a total at the end."""
    if len(expenses) == 0:
        print("\nNo expenses to show.")
        return

    # sort by date (oldest first)
    sorted_expenses = sorted(expenses, key=lambda expense: expense["date"])