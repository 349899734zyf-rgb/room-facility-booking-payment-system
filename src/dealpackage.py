class DealPackage:
    def __init__(self):
        self.price = 100
        self.hours = 12

    def apply(self, account):
        if account.balance >= self.price:
            account.balance -= self.price
            account.add_package_hours(self.hours)
            return True
        return False