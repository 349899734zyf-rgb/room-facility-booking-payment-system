from account import Account
from payment import Payment
from promotion import Promotion
from dealpackage import DealPackage

acc = Account()
acc.top_up(200)

promo = Promotion("SAVE20")
payment = Payment(acc)

# 买套餐
package = DealPackage()
package.apply(acc)

# 支付学习室（比如 $50）
success = payment.pay(50, promo)

print("Balance:", acc.balance)
print("Hours:", acc.package_hours)