from datetime import datetime

class Transaction:
    def __init__(self, account_number, transaction_type, amount):
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_transaction_type(self):
        return self.transaction_type

    def get_amount(self):
        return self.amount

    def get_timestamp(self):
        return self.timestamp

    def get_account_number(self):
        return self.account_number
