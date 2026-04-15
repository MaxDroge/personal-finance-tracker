import sqlite3
from datetime import datetime

DATABASE_NAME = "finance.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_transaction():
    category = input("Enter category (food, rent, gas, etc.): ").strip().lower()
    amount_input = input("Enter amount: ").strip()
    date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()

    if not category:
        print("Category cannot be empty.\n")
        return

    try:
        amount = float(amount_input)
        if amount <= 0:
            print("Amount must be greater than 0.\n")
            return
    except ValueError:
        print("Invalid amount.\n")
        return

    if not date_input:
        date_input = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.\n")
            return

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (category, amount, date)
        VALUES (?, ?, ?)
    """, (category, amount, date_input))

    conn.commit()
    conn.close()

    print("Transaction added successfully.\n")


def view_transactions():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, category, amount, date
        FROM transactions
        ORDER BY date DESC, id DESC
    """)
    transactions = cursor.fetchall()

    conn.close()

    if not transactions:
        print("No transactions found.\n")
        return

    print("\nAll Transactions:")
    print("-" * 50)
    for transaction in transactions:
        print(
            f"ID: {transaction[0]} | "
            f"Category: {transaction[1].title()} | "
            f"Amount: ${transaction[2]:.2f} | "
            f"Date: {transaction[3]}"
        )
    print()


def show_total_spending():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions")
    total = cursor.fetchone()[0]

    conn.close()

    total = total or 0
    print(f"\nTotal Spending: ${total:.2f}\n")


def show_spending_by_category():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)
    results = cursor.fetchall()

    conn.close()

    if not results:
        print("No transactions found.\n")
        return

    print("\nSpending by Category:")
    print("-" * 50)
    for category, total in results:
        print(f"{category.title()}: ${total:.2f}")
    print()


def show_highest_expense():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, amount, date
        FROM transactions
        ORDER BY amount DESC
        LIMIT 1
    """)
    result = cursor.fetchone()

    conn.close()

    if not result:
        print("No transactions found.\n")
        return

    print("\nHighest Expense:")
    print("-" * 50)
    print(f"Category: {result[0].title()}")
    print(f"Amount: ${result[1]:.2f}")
    print(f"Date: {result[2]}\n")


def show_menu():
    print("Personal Finance Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Show Total Spending")
    print("4. Show Spending by Category")
    print("5. Show Highest Expense")
    print("6. Exit")


def main():
    create_database()

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()
        print()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            show_total_spending()
        elif choice == "4":
            show_spending_by_category()
        elif choice == "5":
            show_highest_expense()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.\n")


if __name__ == "__main__":
    main()