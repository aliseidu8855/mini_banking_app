import sqlite3
from transaction import Transaction
from user import User

class Account:
    def __init__(self, account_number):
        self.account_number = account_number
        self.balance = self.get_balance()

    def get_balance(self):
        conn = sqlite3.connect('banking_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM balances WHERE account_number = ?', (self.account_number,))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.balance = result[0]
        return self.balance

    def deposit(self, amount):
        if amount > 0:
            conn = sqlite3.connect('banking_app.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE balances SET balance = balance + ? WHERE account_number = ?', (amount, self.account_number))
            conn.commit()
            conn.close()
            self.add_transaction(Transaction(self.account_number, 'deposit', amount))
        else:
            print("Invalid amount for deposit")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.get_balance():
            conn = sqlite3.connect('banking_app.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE balances SET balance = balance - ? WHERE account_number = ?', (amount, self.account_number))
            conn.commit()
            conn.close()
            self.add_transaction(Transaction(self.account_number, 'withdrawal', amount))
        else:
            print("Invalid amount for withdrawal or insufficient balance")

    def add_transaction(self, transaction):
        conn = sqlite3.connect('banking_app.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO transactions (account_number, amount, transaction_type) VALUES (?, ?, ?)',
                    (self.account_number, transaction.get_amount(), transaction.get_transaction_type()))
        conn.commit()
        conn.close()

    def print_transaction_history(self):
        conn = sqlite3.connect('banking_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT transaction_type, amount, timestamp FROM transactions WHERE account_number = ? ORDER BY timestamp',
                    (self.account_number,))
        history = cursor.fetchall()
        conn.close()
        if not history:
            print("No transaction history available.")
        else:
            print("Transaction history:")
            for transaction in history:
                print(f"{transaction[0]}: GHS {transaction[1]} on {transaction[2]}")

