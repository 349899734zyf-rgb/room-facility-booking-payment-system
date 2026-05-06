class Payment:
    def __init__(self, account):
        self.account = account

    def pay(self, amount, promotion=None):
        if promotion:
            amount = promotion.apply(amount)

        if self.account.balance >= amount:
            self.account.balance -= amount
            return True
        return False