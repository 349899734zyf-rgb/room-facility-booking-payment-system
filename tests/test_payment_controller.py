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


def make_booking(student=None, total_price=50.0, equipment_rental=False):
    if student is None:
        student = make_student()

    room = Room(
        "RM001",
        "Study Room",
        "Clayton",
        4,
        25.0,
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

    promo_code = controller.validate_promo_code("SAVE20", student)

    assert promo_code is not None
    assert promo_code.get_code() == "SAVE20"
    assert promo_code.get_discount_amount() == 20.0


def test_validate_promo_code_returns_none_for_unknown_or_used_code():
    controller = PaymentController()
    student = make_student()
    promo_code = controller.validate_promo_code("SAVE20", student)
    promo_code.mark_used(student.get_student_id())

    assert controller.validate_promo_code("UNKNOWN", student) is None
    assert controller.validate_promo_code("SAVE20", student) is None


def test_apply_promo_code_updates_order_student_and_promo_usage():
    controller = PaymentController()
    student = make_student()
    order = controller.create_order(make_booking(student), "balance")
    promo_code = controller.validate_promo_code("SAVE20", student)

    final_price = controller.apply_promo_code(promo_code, student, order)

    assert final_price == 30.0
    assert order.get_final_price() == 30.0
    assert promo_code.is_used_by(student.get_student_id()) is True
    assert student.has_used_promo_code("SAVE20") is True


def test_purchase_deal_package_deducts_balance_and_adds_hours():
    controller = PaymentController()
    student = make_student(balance=150.0)

    success = controller.purchase_deal_package(student)

    assert success is True
    assert student.get_balance() == 50.0
    assert student.get_deal_package_hours() == 12.0


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


def test_create_order_uses_booking_price_and_increments_order_id():
    controller = PaymentController()
    booking = make_booking(total_price=50.0)

    first_order = controller.create_order(booking, "balance")
    second_order = controller.create_order(booking, "deal_package")

    assert first_order.get_order_id() == "OD0001"
    assert first_order.get_booking() is booking
    assert first_order.get_price() == 50.0
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
