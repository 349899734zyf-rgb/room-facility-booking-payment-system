class Promotion:
    def __init__(self, code):
        self.code = code
        self.used = False
        self.discount = 0.2  # 20%

    def apply(self, amount):
        if self.used:
            return amount
        self.used = True
        return amount * (1 - self.discount)