from src.account import Account
from src.payment import Payment

def test_payment_success():
    acc = Account()
    acc.top_up(100)

    pay = Payment(acc)
    assert pay.pay(50) == True
    assert acc.balance == 50