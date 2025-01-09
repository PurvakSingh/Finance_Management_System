import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import messagebox
import threading
import os
import sys

# MySQL connection function
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password123',
            database='finance_tracker'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Error", f"Database connection failed: {e}")
        return None

# Tkinter function to show expense report
def show_expense_report(account_id):
    conn = connect_db()
    if conn is None:
        return
    
    cursor = conn.cursor()
    cursor.execute('''SELECT category, SUM(amount) FROM transactions WHERE account_id = %s GROUP BY category''', (account_id,))
    expenses = cursor.fetchall()
    
    categories = [category for category, _ in expenses]
    amounts = [amount for _, amount in expenses]
    
    # Plotting the bar chart with Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(x=categories, y=amounts)
    plt.title('Expense Distribution by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount Spent')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    conn.close()

# Tkinter window to interact with the user
def create_window():
    window = tk.Tk()
    window.title("Financial Management System")

    def on_show_report_click():
        account_id = int(account_id_entry.get())
        show_expense_report(account_id)

    account_id_label = tk.Label(window, text="Account ID")
    account_id_label.grid(row=0, column=0)
    
    account_id_entry = tk.Entry(window)
    account_id_entry.grid(row=0, column=1)

    show_report_button = tk.Button(window, text="Show Expense Report", command=on_show_report_click)
    show_report_button.grid(row=1, columnspan=2)

    window.mainloop()

# Streamlit function for expense report
def streamlit_show_expense_report(account_id):
    conn = connect_db()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute('''SELECT category, SUM(amount) FROM transactions WHERE account_id = %s GROUP BY category''', (account_id,))
    expenses = cursor.fetchall()
    
    categories = [category for category, _ in expenses]
    amounts = [amount for _, amount in expenses]
    
    # Plotting the bar chart with Seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=categories, y=amounts, ax=ax)
    ax.set_title('Expense Distribution by Category')
    ax.set_xlabel('Category')
    ax.set_ylabel('Amount Spent')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
    conn.close()

# Streamlit app layout
def streamlit_app():
    import streamlit as st
    
    st.title('Financial Dashboard')

    account_id = st.number_input("Enter Account ID", min_value=1, step=1)

    if account_id:
        if st.button('Show Expense Report'):
            streamlit_show_expense_report(account_id)

# Function to start Streamlit app in a separate thread
def start_streamlit_app():
    os.system('streamlit run app.py')

def main():
    print("Choose the interface you want to run:")
    print("1. Desktop (Tkinter) Interface")
    print("2. Web (Streamlit) Dashboard")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # Tkinter GUI
        create_window()
    elif choice == '2':
        # Streamlit Dashboard
        # Run Streamlit in a separate thread
        streamlit_thread = threading.Thread(target=start_streamlit_app)
        streamlit_thread.start()
    else:
        print("Invalid choice! Please select either 1 or 2.")

if __name__ == "__main__":
    main()
