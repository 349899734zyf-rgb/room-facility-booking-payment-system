from datetime import datetime, timedelta

from src.controller_classes import BookingController, PaymentController
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


def make_booking(student, equipment_rental=False):
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
        20.0
    )


def test_aggregate_payment_controller_includes_equipment_deposit():
    controller = PaymentController()
    student = make_student(balance=150.0)
    booking = make_booking(student, equipment_rental=True)
    order = controller.create_order(booking, "balance")

    assert controller.get_order_payable_amount(order) == 120.0
    assert controller.pay_by_balance(student, order) is True
    assert student.get_balance() == 30.0


def test_aggregate_payment_controller_final_price_payment_adds_deposit():
    controller = PaymentController()
    student = make_student(balance=150.0)
    booking = make_booking(student, equipment_rental=True)
    order = controller.create_order(booking, "balance")

    assert controller.pay_by_balance(student, order.get_final_price()) is True
    assert student.get_balance() == 30.0


def test_aggregate_payment_controller_blocks_deal_package_with_equipment():
    controller = PaymentController()
    student = make_student(package_hours=5.0)

    assert controller.pay_by_deal_package(student, 2.0, True) is False
    assert student.get_deal_package_hours() == 5.0


def test_room_availability_updates_after_order_confirmation():
    booking_controller = BookingController()
    payment_controller = PaymentController()
    student = make_student(balance=150.0)
    room = Room(
        "RM001",
        "Study Room",
        "Clayton",
        4,
        10.0,
        "08:00-22:00"
    )
    start_time = datetime.now().replace(microsecond=0)
    end_time = start_time + timedelta(hours=2)
    time_slot = f"{start_time}-{end_time}"
    room.set_available_time_slots([time_slot])

    booking = booking_controller.create_booking(
        student,
        room,
        start_time,
        end_time,
        equipment_rental=False
    )
    order = payment_controller.create_order(booking, "balance")

    assert booking.get_status() == "pending"
    assert time_slot in room.get_available_time_slots()

    payment_controller.confirm_order(order, student)

    assert booking.get_status() == "confirmed"
    assert time_slot not in room.get_available_time_slots()
