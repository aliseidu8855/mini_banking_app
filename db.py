import sqlite3
import random

def create_database():
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

# Function to generate a random 8-digit account number
def generate_account_number():
    return str(random.randint(10000000, 99999999))

# User registration
def register_user():
    conn = sqlite3.connect('banking_app.db')
    cursor = conn.cursor()

    full_name = input("Enter your full name: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")

    while True:
        account_number = generate_account_number()
        cursor.execute('SELECT account_number FROM users WHERE account_number = ?', (account_number,))
        if not cursor.fetchone():
            break

    try:
        cursor.execute('INSERT INTO users (account_number, full_name, phone_number, email) VALUES (?, ?, ?, ?)',
                    (account_number, full_name, phone_number, email))
        cursor.execute('INSERT INTO balances (account_number, balance) VALUES (?, 0)', (account_number,))
        conn.commit()
        print(f"User registered successfully. Your account number is: {account_number}")
    except sqlite3.IntegrityError:
        print("Error occurred during registration.")

    conn.close()

# User login
def login_user():
    account_number = input("Enter your account number: ")
    conn = sqlite3.connect('banking_app.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE account_number = ?', (account_number,))
    user = cursor.fetchone()

    conn.close()
    if user:
        return account_number
    else:
        print("Account not found. Please register.")
        return None
