# menu.py
# This file runs the console menu and talks to the user.

import os

from expense_tracker.expense import make_expense, is_valid_date
from expense_tracker.storage import save_expenses, load_expenses
from expense_tracker.filters import filter_expenses, get_categories
from expense_tracker.exporter import export_to_csv
from expense_tracker.display import print_expenses

DEFAULT_FILE = "expenses.json"


def add_extension(filename, extension):
    """Add .json or .csv to the end of a filename if it is missing."""
    if not filename.lower().endswith(extension):
        filename = filename + extension
    return filename


def ask_for_date(question):
    """Keep asking until the user types a valid date or presses Enter (blank)."""
    while True:
        text = input(question).strip()
        if text == "" or is_valid_date(text):
            return text
        print("  That is not a valid date. Use YYYY-MM-DD, like 2026-11-08.")


def ask_for_filters():
    """Ask the user for a date range and/or category. Blank means 'no filter'."""
    print("\nPress Enter to skip any of these.")

    while True:
        start_date = ask_for_date("Start date (YYYY-MM-DD): ")
        end_date = ask_for_date("End date   (YYYY-MM-DD): ")
        if start_date != "" and end_date != "" and end_date < start_date:
            print("  The end date is before the start date. Please try again.")
        else:
            break

    category = input("Category: ").strip()
    return start_date, end_date, category


def add_expense(expenses, filename):
    """Ask for the details of a new expense and add it to the list."""
    print("\n--- Add an expense ---")
    date_text = input("Date (YYYY-MM-DD): ").strip()
    category = input("Category (for example Food, Rent, Travel): ")
    description = input("Description: ")
    amount_text = input("Amount: ")

    try:
        expense = make_expense(date_text, category, description, amount_text)
    except ValueError as error:
        print("\nCould not add the expense: " + str(error))
        return

    expenses.append(expense)
    print("\nExpense added.")

    # save right away so nothing is lost
    try:
        save_expenses(expenses, filename)
        print("Saved to " + filename)
    except OSError as error:
        print("Warning: could not save the file: " + str(error))


def view_all(expenses):
    """Print every expense."""
    print("\n--- All expenses ---")
    print_expenses(expenses)


def view_filtered(expenses):
    """Ask for filters, then print only the matching expenses."""
    print("\n--- Filter expenses ---")
    if len(expenses) == 0:
        print("There are no expenses yet.")
        return

    categories = get_categories(expenses)
    print("Categories in use: " + ", ".join(categories))

    start_date, end_date, category = ask_for_filters()
    matches = filter_expenses(expenses, start_date, end_date, category)
    print_expenses(matches)


def open_file(expenses, filename):
    """Open an expense file. Returns the new filename (or the old one if it failed)."""
    print("\n--- Open an expense file ---")
    new_name = input("File to open (Enter for " + filename + "): ").strip()
    if new_name == "":
        new_name = filename
    new_name = add_extension(new_name, ".json")

    # load_expenses() gives an empty list for a missing file, which would
    # wipe the current expenses, so check that the file exists first
    if not os.path.exists(new_name):
        print("\nCould not find a file named " + new_name)
        return filename

    try:
        loaded = load_expenses(new_name)
    except (ValueError, OSError) as error:
        print("\nCould not open " + new_name + ": " + str(error))
        return filename

    # replace the current list with the loaded one (keep the same list object)
    expenses.clear()
    expenses.extend(loaded)
    print("\nOpened " + new_name + " (" + str(len(expenses)) + " expense(s)).")
    return new_name


def save_file(expenses, filename):
    """Save to a file chosen by the user. Returns the filename that was used."""
    print("\n--- Save expenses ---")
    new_name = input("File to save to (Enter for " + filename + "): ").strip()
    if new_name == "":
        new_name = filename
    new_name = add_extension(new_name, ".json")

    try:
        save_expenses(expenses, new_name)
    except OSError as error:
        print("\nCould not save: " + str(error))
        return filename

    print("\nSaved " + str(len(expenses)) + " expense(s) to " + new_name)
    return new_name


def export_csv(expenses):
    """Export all (or filtered) expenses to a CSV file for Excel."""
    print("\n--- Export to CSV (for Excel) ---")
    if len(expenses) == 0:
        print("There are no expenses to export.")
        return

    print("Choose filters for the expenses to export, or skip them to export everything.")
    start_date, end_date, category = ask_for_filters()
    matches = filter_expenses(expenses, start_date, end_date, category)

    if len(matches) == 0:
        print("\nNo expenses match those filters, so nothing was exported.")
        return

    csv_name = input("CSV file name (Enter for expenses.csv): ").strip()
    if csv_name == "":
        csv_name = "expenses.csv"
    csv_name = add_extension(csv_name, ".csv")

    try:
        export_to_csv(matches, csv_name)
    except OSError as error:
        print("\nCould not export: " + str(error))
        return

    print("\nExported " + str(len(matches)) + " expense(s) to " + csv_name)
    print("You can open this file in Microsoft Excel.")


def show_menu(filename):
    """Print the main menu."""
    print("\n==============================")
    print("        EXPENSE TRACKER")
    print("==============================")
    print("Current file: " + filename)
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. Filter expenses")
    print("4. Open an expense file")
    print("5. Save expenses to a file")
    print("6. Export to CSV (Excel)")
    print("7. Quit")


def run():
    """Start the program."""
    filename = DEFAULT_FILE
    expenses = []

    # load the default file if it already exists
    try:
        expenses = load_expenses(filename)
        if len(expenses) > 0:
            print("Loaded " + str(len(expenses)) + " expense(s) from " + filename)
    except (ValueError, OSError) as error:
        print("Could not load " + filename + ": " + str(error))
        print("Starting with an empty list.")

    while True:
        show_menu(filename)
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_expense(expenses, filename)
        elif choice == "2":
            view_all(expenses)
        elif choice == "3":
            view_filtered(expenses)
        elif choice == "4":
            filename = open_file(expenses, filename)
        elif choice == "5":
            filename = save_file(expenses, filename)
        elif choice == "6":
            export_csv(expenses)
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("\nPlease enter a number from 1 to 7.")