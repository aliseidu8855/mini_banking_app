import sqlite3
import db

# record transaction function
def record_transaction(conn, cursor, account_number, transaction_type, amount):
    cursor.execute('INSERT INTO transactions (account_number, amount, transaction_type) VALUES (?, ?, ?)',
                (account_number, amount, transaction_type))
    conn.commit()

# deposit function
def deposit(account_number):
    conn = sqlite3.connect('banking_app.db')
    cursor = conn.cursor()

    amount = input("How much do you want to deposit? ")
    try:
        amount = float(amount)
    except ValueError:
        print("Enter a valid amount")
        conn.close()
        return

    if amount >= 0:
        cursor.execute('UPDATE balances SET balance = balance + ? WHERE account_number = ?', (amount, account_number))
        record_transaction(conn, cursor, account_number, 'deposit', amount)
        conn.commit()
        cursor.execute('SELECT balance FROM balances WHERE account_number = ?', (account_number,))
        new_balance = cursor.fetchone()[0]
        print(f"\nYou have successfully deposited GHS {amount} to account {account_number}.\nYour new balance is {new_balance}\nThank you for trusting us!\n")
    else:
        print("Enter a valid amount")

    conn.close()

# check balance function
def check_balance(account_number):
    conn = sqlite3.connect('banking_app.db')
    cursor = conn.cursor()

    cursor.execute('SELECT balance FROM balances WHERE account_number = ?', (account_number,))
    balance = cursor.fetchone()[0]
    print(f"Your current balance is GHS {balance}")

    conn.close()

# withdrawal function
def withdrawal(account_number):
    conn = sqlite3.connect('banking_app.db')
    cursor = conn.cursor()

    amount = input("How much do you want to withdraw? ")
    try:
        amount = float(amount)
    except ValueError:
        print("Enter a valid amount")
        return

    cursor.execute('SELECT balance FROM balances WHERE account_number = ?', (account_number,))
    current_balance = cursor.fetchone()[0]
    if amount > current_balance:
        print("Insufficient balance")
    elif amount >= 0:
        cursor.execute('UPDATE balances SET balance = balance - ? WHERE account_number = ?', (amount, account_number))
        record_transaction(conn, cursor, account_number, 'withdrawal', amount)
        conn.commit()
        print(f"\nYou have successfully withdrawn GHS {amount} from account {account_number}\nThank you for trusting us!\n")
    else:
        print("Enter a valid amount")

    conn.close()

# transaction history function
def transaction_history(account_number):
    conn = sqlite3.connect('banking_app.db')
    cursor = conn.cursor()

    cursor.execute('SELECT transaction_type, amount, timestamp FROM transactions WHERE account_number = ? ORDER BY timestamp', (account_number,))
    history = cursor.fetchall()
    if not history:
        print("No transaction history available.")
    else:
        print("Transaction history:")
        for transaction in history:
            print(f"{transaction[0]}: GHS {transaction[1]} on {transaction[2]}")

    conn.close()

# main function
def main():
    while True:
        print("\nWelcome to my mini bank")
        print("*********************************")
        print("1. Register")
        print("2. Login")
        print("3. Exit\n")

        try:
            choose = int(input("Choose: "))
        except ValueError:
            print("Warning!!! Enter a valid choice")
            continue

        if choose == 1:
            db.register_user()
        elif choose == 2:
            account_number = db.login_user()
            if account_number:
                while True:
                    print("\n1. Deposit to your account")
                    print("2. Withdrawal from your account")
                    print("3. Check your transaction history")
                    print("4. Check your account balance")
                    print("5. Logout\n")

                    try:
                        action = int(input("Choose: "))
                    except ValueError:
                        print("Warning!!! Enter a valid choice")
                        continue

                    if action == 1:
                        deposit(account_number)
                    elif action == 2:
                        withdrawal(account_number)
                    elif action == 3:
                        transaction_history(account_number)
                    elif action == 4:
                        check_balance(account_number)
                    elif action == 5:
                        print("Logged out.")
                        break
                    else:
                        print("Warning!!! Enter a valid choice")
                        continue
        elif choose == 3:
            print("Thank you for banking with us!\nHave a nice day")
            break
        else:
            print("Warning!!! Enter a valid choice")
            continue

if __name__ == "__main__":
    db.create_database()
    main()
