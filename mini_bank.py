# Initialize a dictionary to store balances
balances = {}


# Initialize a dictionary to store transaction history
transaction_histories = {}


# deposit function
def deposit():
    global balances
    account_number = input("Enter your account number: ")
    if len(account_number) != 8:
        print("Enter a valid account number (8 digits long).")
        return

    amount = input("How much do you want to deposit? ")
    try:
        amount = float(amount)
    except ValueError:
        print("Enter a valid amount")
        return

    if amount >= 0:
        balances[account_number] = balances.get(account_number, 0) + amount
        print(f"\nYou have successfully deposited GHS {amount} to account {account_number}\nThank you for trusting us!\n")
        record_transaction(account_number, 'deposit', amount)
    else:
        print("Enter a valid amount")


# check balance function
def check_balance():
    global balances
    account_number = input("Enter your account number: ")
    if len(account_number) != 8:
        print("Enter a valid account number (8 digits long).")
        return
    balance = balances.get(account_number, 0)
    print(f"Your current balance is GHS {balance}")


# withdrawal function
def withdrawal():
    global balances
    account_number = input("Enter your account number: ")
    if account_number not in balances :
        print("Account not found")
        return

    amount = input("How much do you want to withdraw? ")
    try:
        amount = float(amount)
    except ValueError:
        print("Enter a valid amount")
        return

    current_balance = balances.get(account_number, 0)
    if amount > current_balance:
        print("Insufficient balance")
    elif amount >= 0:
        balances[account_number] = current_balance - amount
        print(f"\nYou have successfully withdrawn GHS {amount} from account {account_number}\nThank you for trusting us!\n")
        record_transaction(account_number, 'withdrawal', amount)
    else:
        print("Enter a valid amount")


# transaction history function
def transaction_history():
    global transaction_histories
    account_number = input("Enter your account number: ")
    if len(account_number) != 8:
        print("Enter a valid account number (8 digits long).")
        return
    
    history = transaction_histories.get(account_number, [])
    if not history:
        print("No transaction history available.")
    else:
        print("Transaction history:")
        for transaction in history:
            print(transaction)


# record transaction function
def record_transaction(account_number, transaction_type, amount):
    global transaction_histories
    if account_number not in transaction_histories:
        transaction_histories[account_number] = []
    transaction_histories[account_number].append(f"{transaction_type}: GHS {amount}")


# main function
def main():
    while True:
        print("\nWelcome to my mini bank")
        print("*********************************")
        print("1. Deposit to your account")
        print("2. Withdrawal from your account")
        print("3. Check your transaction history")
        print("4. Check your account balance")
        print("5. Exit\n")

        try:
            choose = int(input("Choose: "))
        except ValueError:
            print("Warning!!! Enter a valid choice")
            continue


        if choose == 1:
            deposit()
        elif choose == 2:
            withdrawal()
        elif choose == 3:
            transaction_history()
        elif choose == 4:
            check_balance()
        elif choose == 5:
            print("Thank you for banking with us!\nHave a nice day")
            break
        else:
            print("Warning!!! Enter a valid choice")
            continue


if __name__ == "__main__":
    main()

