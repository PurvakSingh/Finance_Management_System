import mysql.connector
from mysql.connector import Error
from datetime import datetime

def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Your MySQL host
            user='root',  # Your MySQL username
            password='password123',  # Your MySQL password
            database='finance_tracker'  # Updated database name
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            cursor = conn.cursor()
            # Create tables if they don't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                account_id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(100) NOT NULL,
                                balance FLOAT DEFAULT 0.0
                            )''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                                account_id INT,
                                amount FLOAT NOT NULL,
                                category VARCHAR(100),
                                transaction_date DATE NOT NULL,
                                description VARCHAR(255),
                                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS budget_plans (
                                budget_id INT AUTO_INCREMENT PRIMARY KEY,
                                account_id INT,
                                category VARCHAR(100),
                                budget_amount FLOAT NOT NULL,
                                start_date DATE,
                                end_date DATE,
                                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
                            )''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS expense_categories (
                                category_id INT AUTO_INCREMENT PRIMARY KEY,
                                category_name VARCHAR(100) NOT NULL
                            )''')
            conn.commit()
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Creating expense categories
def create_category(conn, category_name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expense_categories (category_name) VALUES (%s)", (category_name,))
    conn.commit()
    print(f"Category '{category_name}' created successfully!")

# Add a transaction
def add_transaction(conn, account_id, amount, category, description):
    transaction_date = datetime.now().date()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (account_id, amount, category, transaction_date, description) VALUES (%s, %s, %s, %s, %s)",
                   (account_id, amount, category, transaction_date, description))
    conn.commit()
    print(f"Transaction of {amount} in category '{category}' added successfully.")

# Create a budget plan
def create_budget_plan(conn, account_id, category, budget_amount, start_date, end_date):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO budget_plans (account_id, category, budget_amount, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
                   (account_id, category, budget_amount, start_date, end_date))
    conn.commit()
    print(f"Budget plan for category '{category}' created successfully.")

# Generate monthly financial report
def generate_monthly_report(conn, account_id, month, year):
    cursor = conn.cursor()
    cursor.execute('''SELECT category, SUM(amount) FROM transactions 
                      WHERE account_id = %s AND MONTH(transaction_date) = %s AND YEAR(transaction_date) = %s
                      GROUP BY category''', (account_id, month, year))
    transactions = cursor.fetchall()

    print(f"\n--- Monthly Financial Report for {month}/{year} ---")
    total_expenses = 0
    for category, total_amount in transactions:
        print(f"Category: {category}, Total Expenses: {total_amount}")
        total_expenses += total_amount
    
    print(f"\nTotal Expenses for the month: {total_expenses}")

# View expenses by category
def view_expenses_by_category(conn, account_id):
    cursor = conn.cursor()
    cursor.execute('''SELECT category, SUM(amount) FROM transactions WHERE account_id = %s GROUP BY category''', (account_id,))
    expenses = cursor.fetchall()
    
    print("\n--- Expenses by Category ---")
    for category, total_amount in expenses:
        print(f"Category: {category}, Total Expenses: {total_amount}")

def main():
    conn = connect_db()
    if conn is None:
        print("Failed to connect to the database!")
        return

    while True:
        print("\n--- Financial Management System ---")
        print("1. Create Account")
        print("2. Create Expense Category")
        print("3. Add Transaction")
        print("4. Create Budget Plan")
        print("5. View Monthly Financial Report")
        print("6. View Expenses by Category")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter account holder's name: ")
            initial_deposit = float(input("Enter initial deposit amount: "))
            create_account(conn, name, initial_deposit)
        elif choice == "2":
            category_name = input("Enter expense category name: ")
            create_category(conn, category_name)
        elif choice == "3":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter transaction amount: "))
            category = input("Enter transaction category: ")
            description = input("Enter transaction description: ")
            add_transaction(conn, account_id, amount, category, description)
        elif choice == "4":
            account_id = int(input("Enter account ID: "))
            category = input("Enter budget category: ")
            budget_amount = float(input("Enter budget amount: "))
            start_date = input("Enter budget start date (YYYY-MM-DD): ")
            end_date = input("Enter budget end date (YYYY-MM-DD): ")
            create_budget_plan(conn, account_id, category, budget_amount, start_date, end_date)
        elif choice == "5":
            account_id = int(input("Enter account ID: "))
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year (YYYY): "))
            generate_monthly_report(conn, account_id, month, year)
        elif choice == "6":
            account_id = int(input("Enter account ID: "))
            view_expenses_by_category(conn, account_id)
        elif choice == "7":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
