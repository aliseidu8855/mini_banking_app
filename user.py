class User:
    def __init__(self, account_number, full_name, phone_number, email):
        self.account_number = account_number
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email

    def get_account_number(self):
        return self.account_number

    def get_full_name(self):
        return self.full_name

    def get_phone_number(self):
        return self.phone_number

    def get_email(self):
        return self.email
