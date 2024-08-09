import sqlite3
import random
from user import User
from account import Account

class Bank:
    def __init__(self):
        self.create_database()

    def create_database(self):
        conn = sqlite3.connect('banking_app.db')
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            account_number TEXT UNIQUE NOT NULL,
                            full_name TEXT NOT NULL,
                            phone_number TEXT NOT NULL,
                            email TEXT NOT NULL
                        )''')

        # Create balances table
        cursor.execute('''CREATE TABLE IF NOT EXISTS balances (
                            account_number TEXT PRIMARY KEY,
                            balance REAL DEFAULT 0.0,
                            FOREIGN KEY (account_number) REFERENCES users (account_number)
                        )''')

        # Create transactions table
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            account_number TEXT NOT NULL,
                            amount REAL NOT NULL,
                            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('deposit', 'withdrawal')),
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (account_number) REFERENCES users (account_number)
                        )''')

        conn.commit()
        conn.close()

    def generate_account_number(self):
        return str(random.randint(10000000, 99999999))

    def register_user(self):
        full_name = input("Enter your full name: ")
        phone_number = input("Enter your phone number: ")
        email = input("Enter your email: ")

        while True:
            account_number = self.generate_account_number()
            if not self.account_exists(account_number):
                break

        try:
            conn = sqlite3.connect('banking_app.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (account_number, full_name, phone_number, email) VALUES (?, ?, ?, ?)',
                        (account_number, full_name, phone_number, email))
            cursor.execute('INSERT INTO balances (account_number, balance) VALUES (?, 0)', (account_number,))
            conn.commit()
            conn.close()
            print(f"User registered successfully. Your account number is: {account_number}")
        except sqlite3.IntegrityError:
            print("Error occurred during registration.")

    def account_exists(self, account_number):
        conn = sqlite3.connect('banking_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT account_number FROM users WHERE account_number = ?', (account_number,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def login_user(self):
        account_number = input("Enter your account number: ")
        if self.account_exists(account_number):
            return account_number
        else:
            print("Account not found. Please register.")
            return None

    def deposit(self, account_number):
        amount = input("How much do you want to deposit? ")
        try:
            amount = float(amount)
        except ValueError:
            print("Enter a valid amount")
            return

        if amount >= 0:
            account = Account(account_number)
            account.deposit(amount)
            print(f"\nYou have successfully deposited GHS {amount} to account {account_number}.\nYour new balance is GHS {account.get_balance()}\nThank you for trusting us!\n")
        else:
            print("Enter a valid amount")

    def withdraw(self, account_number):
        amount = input("How much do you want to withdraw? ")
        try:
            amount = float(amount)
        except ValueError:
            print("Enter a valid amount")
            return

        account = Account(account_number)
        current_balance = account.get_balance()
        if amount > current_balance:
            print("Insufficient balance")
        elif amount >= 0:
            account.withdraw(amount)
            print(f"\nYou have successfully withdrawn GHS {amount} from account {account_number}.\nThank you for trusting us!\n")
        else:
            print("Enter a valid amount")

    def check_balance(self, account_number):
        account = Account(account_number)
        print(f"Your current balance is GHS {account.get_balance()}")

    def print_transaction_history(self, account_number):
        account = Account(account_number)
        account.print_transaction_history()
