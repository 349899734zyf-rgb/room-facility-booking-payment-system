class Account:
    def __init__(self):
        self.balance = 0
        self.package_hours = 0

    def top_up(self, amount):
        self.balance += amount

    def add_package_hours(self, hours):
        self.package_hours += hours