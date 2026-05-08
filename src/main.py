from datetime import timedelta, datetime

from controllers.payment_controller import PaymentController
from entity_classes import Student, Room, Booking


student = Student(
    "test@student.monash.edu",
    "Password1",
    "Tom",
    "Lee",
    "0412345678",
    "12345678"
)

student.add_funds(200)

room = Room(
    "RM001",
    "Study Room",
    "Clayton",
    4,
    25,
    "08:00-22:00"
)

start = datetime.now()
end = start + timedelta(hours=2)

booking = Booking(
    "BK001",
    student,
    room,
    start,
    end,
    False,
    50
)

payment_controller = PaymentController()

# create order
order = payment_controller.create_order(
    booking,
    "balance"
)

# apply promo
promo = payment_controller.validate_promo_code(
    "SAVE20",
    student
)

if promo:

    final_price = payment_controller.apply_promo_code(
        promo,
        student,
        order
    )

    print("Discount applied")
    print(final_price)

# pay
success = payment_controller.pay_by_balance(
    student,
    order.get_final_price()
)

if success:

    payment_controller.confirm_order(
        order,
        student
    )

    print("Payment successful")
    print(student.get_balance())

else:
    print("Payment failed")