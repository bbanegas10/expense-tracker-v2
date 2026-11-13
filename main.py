
# Run this file to start the Expense Tracker:



from expense_tracker.menu import run


def main():
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        
        print("\n\nGoodbye!")


if __name__ == '__main__':
    main()