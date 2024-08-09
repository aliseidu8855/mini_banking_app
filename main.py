from bank import Bank

def main():
    bank = Bank()

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
            bank.register_user()
        elif choose == 2:
            account_number = bank.login_user()
            if account_number:
                while True:
                    print("\n1. Deposit to your account")
                    print("2. Withdraw from your account")
                    print("3. Check your transaction history")
                    print("4. Check your account balance")
                    print("5. Logout\n")

                    try:
                        action = int(input("Choose: "))
                    except ValueError:
                        print("Warning!!! Enter a valid choice")
                        continue

                    if action == 1:
                        bank.deposit(account_number)
                    elif action == 2:
                        bank.withdraw(account_number)
                    elif action == 3:
                        bank.print_transaction_history(account_number)
                    elif action == 4:
                        bank.check_balance(account_number)
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
    main()

