from datetime import datetime, timedelta

from src.controllers.payment_controller import PaymentController
from src.entity_classes import Booking, Room, Student


def make_student(balance=0.0, package_hours=0.0):
    student = Student(
        "student@example.com",
        "Password1",
        "Test",
        "Student",
        "0412345678",
        "S001"
    )
    student.set_balance(balance)
    student.set_deal_package_hours(package_hours)
    return student


def make_booking(student=None, total_price=20.0, equipment_rental=False):
    if student is None:
        student = make_student()

    room = Room(
        "RM001",
        "Study Room",
        "Clayton",
        4,
        10.0,
        "08:00-22:00"
    )
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    return Booking(
        "BK001",
        student,
        room,
        start_time,
        end_time,
        equipment_rental,
        total_price
    )


def test_validate_promo_code_returns_default_code_when_unused():
    controller = PaymentController()
    student = make_student()

    promo_code = controller.validate_promo_code("NEWBEE20", student)

    assert promo_code is not None
    assert promo_code.get_code() == "NEWBEE20"
    assert promo_code.get_discount_amount() == 20.0


def test_get_promo_codes_returns_default_codes():
    controller = PaymentController()

    promo_codes = controller.get_promo_codes()

    assert len(promo_codes) == 1
    assert promo_codes[0].get_code() == "NEWBEE20"


def test_validate_promo_code_returns_none_for_unknown_or_used_code():
    controller = PaymentController()
    student = make_student()
    promo_code = controller.validate_promo_code("NEWBEE20", student)
    promo_code.mark_used(student.get_student_id())

    assert controller.validate_promo_code("UNKNOWN", student) is None
    assert controller.validate_promo_code("NEWBEE20", student) is None


def test_apply_promo_code_updates_order_student_and_promo_usage():
    controller = PaymentController()
    student = make_student()
    order = controller.create_order(make_booking(student), "balance")
    promo_code = controller.validate_promo_code("NEWBEE20", student)

    final_price = controller.apply_promo_code(promo_code, student, order)

    assert final_price == 16.0
    assert order.get_final_price() == 16.0
    assert promo_code.is_used_by(student.get_student_id()) is True
    assert student.has_used_promo_code("NEWBEE20") is True
    assert controller.validate_promo_code("NEWBEE20", student) is None


def test_apply_promo_code_cannot_be_applied_twice_to_same_order():
    controller = PaymentController()
    student = make_student()
    order = controller.create_order(make_booking(student), "balance")
    promo_code = controller.validate_promo_code("NEWBEE20", student)

    first_price = controller.apply_promo_code(promo_code, student, order)
    second_price = controller.apply_promo_code(promo_code, student, order)

    assert first_price == 16.0
    assert second_price == 16.0
    assert order.get_promo_discount() == 4.0
    assert order.get_promo_code_used() == "NEWBEE20"


def test_apply_promo_code_only_works_for_first_booking():
    controller = PaymentController()
    student = make_student()
    previous_booking = make_booking(student, total_price=20.0)
    student.add_booking(previous_booking)
    order = controller.create_order(make_booking(student), "balance")
    promo_code = controller.validate_promo_code("NEWBEE20", student)

    final_price = controller.apply_promo_code(promo_code, student, order)

    assert final_price == 20.0
    assert order.get_promo_discount() == 0
    assert promo_code.is_used_by(student.get_student_id()) is False


def test_apply_promo_code_does_not_work_with_deal_package():
    controller = PaymentController()
    student = make_student()
    order = controller.create_order(make_booking(student), "deal_package")
    promo_code = controller.validate_promo_code("NEWBEE20", student)

    final_price = controller.apply_promo_code(promo_code, student, order)

    assert final_price == 20.0
    assert order.get_final_price() == 20.0
    assert promo_code.is_used_by(student.get_student_id()) is False
    assert student.has_used_promo_code("NEWBEE20") is False


def test_purchase_deal_package_deducts_balance_and_adds_hours():
    controller = PaymentController()
    student = make_student(balance=150.0)

    success = controller.purchase_deal_package(student)

    assert success is True
    assert student.get_balance() == 50.0
    assert student.get_deal_package_hours() == 12.0


def test_get_deal_package_returns_checkout_package():
    controller = PaymentController()

    deal_package = controller.get_deal_package()

    assert deal_package.get_price() == 100.0
    assert deal_package.get_hours() == 12.0


def test_purchase_deal_package_fails_when_balance_is_insufficient():
    controller = PaymentController()
    student = make_student(balance=80.0)

    success = controller.purchase_deal_package(student)

    assert success is False
    assert student.get_balance() == 80.0
    assert student.get_deal_package_hours() == 0.0


def test_pay_by_deal_package_deducts_hours_only_without_equipment():
    controller = PaymentController()
    student = make_student(package_hours=5.0)

    success = controller.pay_by_deal_package(
        student,
        required_hours=2.0,
        has_equipment=False
    )

    assert success is True
    assert student.get_deal_package_hours() == 3.0


def test_pay_by_deal_package_fails_with_equipment_or_insufficient_hours():
    controller = PaymentController()
    student = make_student(package_hours=1.0)

    assert controller.can_use_deal_package(False) is True
    assert controller.can_use_deal_package(True) is False
    assert controller.pay_by_deal_package(student, 1.0, True) is False
    assert student.get_deal_package_hours() == 1.0
    assert controller.pay_by_deal_package(student, 2.0, False) is False
    assert student.get_deal_package_hours() == 1.0


def test_balance_payment_checks_and_deducts_balance():
    controller = PaymentController()
    student = make_student(balance=75.0)

    assert controller.check_balance_sufficient(student, 50.0) is True
    assert controller.check_balance_sufficient(student, 80.0) is False
    assert controller.pay_by_balance(student, 50.0) is True
    assert student.get_balance() == 25.0
    assert controller.pay_by_balance(student, 50.0) is False
    assert student.get_balance() == 25.0


def test_balance_payment_includes_equipment_deposit():
    controller = PaymentController()
    student = make_student(balance=150.0)
    order = controller.create_order(
        make_booking(student, total_price=20.0, equipment_rental=True),
        "balance"
    )

    payable_amount = controller.get_order_payable_amount(order)
    success = controller.pay_by_balance(student, payable_amount)

    assert controller.get_equipment_deposit_amount() == 100.0
    assert payable_amount == 120.0
    assert success is True
    assert student.get_balance() == 30.0


def test_balance_payment_accepts_order_and_includes_equipment_deposit():
    controller = PaymentController()
    student = make_student(balance=150.0)
    order = controller.create_order(
        make_booking(student, total_price=20.0, equipment_rental=True),
        "balance"
    )

    assert controller.check_balance_sufficient(student, order) is True
    assert controller.pay_by_balance(student, order) is True
    assert student.get_balance() == 30.0


def test_balance_payment_with_latest_equipment_order_final_price_adds_deposit():
    controller = PaymentController()
    student = make_student(balance=150.0)
    order = controller.create_order(
        make_booking(student, total_price=20.0, equipment_rental=True),
        "balance"
    )

    assert controller.check_balance_sufficient(student, order.get_final_price()) is True
    assert controller.pay_by_balance(student, order.get_final_price()) is True
    assert student.get_balance() == 30.0


def test_balance_payment_does_not_add_deposit_without_equipment():
    controller = PaymentController()
    student = make_student(balance=150.0)
    order = controller.create_order(
        make_booking(student, total_price=20.0, equipment_rental=False),
        "balance"
    )

    payable_amount = controller.get_order_payable_amount(order)
    success = controller.pay_by_balance(student, payable_amount)

    assert payable_amount == 20.0
    assert success is True
    assert student.get_balance() == 130.0


def test_equipment_deposit_is_not_discounted_by_promo_code():
    controller = PaymentController()
    student = make_student(balance=150.0)
    order = controller.create_order(
        make_booking(student, total_price=20.0, equipment_rental=True),
        "balance"
    )
    promo_code = controller.validate_promo_code("NEWBEE20", student)

    final_price = controller.apply_promo_code(promo_code, student, order)
    payable_amount = controller.get_order_payable_amount(order)

    assert final_price == 16.0
    assert payable_amount == 116.0


def test_create_order_uses_booking_price_and_increments_order_id():
    controller = PaymentController()
    booking = make_booking(total_price=20.0)

    first_order = controller.create_order(booking, "balance")
    second_order = controller.create_order(booking, "deal_package")

    assert first_order.get_order_id() == "OD0001"
    assert first_order.get_booking() is booking
    assert first_order.get_price() == 20.0
    assert first_order.get_payment_method() == "balance"
    assert second_order.get_order_id() == "OD0002"
    assert second_order.get_payment_method() == "deal_package"


def test_confirm_order_marks_booking_confirmed_and_payment_method():
    controller = PaymentController()
    student = make_student()
    booking = make_booking(student)
    booking.set_status("pending")
    order = controller.create_order(booking, "balance")

    success = controller.confirm_order(order, student)

    assert success is True
    assert booking.get_status() == "confirmed"
    assert booking.get_payment_method() == "balance"
