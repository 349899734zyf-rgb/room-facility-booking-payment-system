"""
This file contains simple test cases for the booking module, including room search,
booking creation, duration validation, booking limits, and cancellation rules.
"""

from datetime import datetime, timedelta

from booking_constants import (
    BOOKING_STATUS_CONFIRMED,
    CANCELLATION_LATE,
    CANCELLATION_REGULAR,
    REASON_BOOKING_LIMIT_REACHED,
    REASON_INVALID_DURATION,
)
from controllers.booking_controller import BookingController
from entity_classes import Room, Student

TEST_BALANCE = 500.0
TEST_EMAIL = "test@student.monash.edu"
TEST_PASSWORD = "Password1"
TEST_FIRST_NAME = "Test"
TEST_LAST_NAME = "Student"
TEST_PHONE = "0412345678"
TEST_STUDENT_ID = "S001"

TEST_ROOM_ID = "R001"
TEST_ROOM_NAME = "Study Room"
TEST_BUILDING = "BLD1"
TEST_CAPACITY = 4
TEST_PRICE_PER_HOUR = 20.0
TEST_OPENING_HOURS = "09:00-18:00"

SEARCH_START_TEXT = "2026-05-12 10:00"
SEARCH_END_TEXT = "2026-05-12 12:00"
BASE_START_TIME = datetime(2026, 5, 12, 10, 0)
BASE_END_TIME = datetime(2026, 5, 12, 12, 0)
SHORT_END_TIME = datetime(2026, 5, 12, 10, 30)
EARLY_CANCELLATION_TIME = datetime(2026, 5, 11, 10, 0)
FOURTH_BOOKING_START = datetime(2026, 5, 20, 10, 0)
FOURTH_BOOKING_END = datetime(2026, 5, 20, 12, 0)
LATE_CANCELLATION_START_OFFSET = 20
LATE_CANCELLATION_CHECK_OFFSET = 10
BOOKING_LIMIT_COUNT = 3


def make_student(balance: float = TEST_BALANCE) -> Student:
    """Create a sample student for booking tests."""
    student = Student(
        TEST_EMAIL,
        TEST_PASSWORD,
        TEST_FIRST_NAME,
        TEST_LAST_NAME,
        TEST_PHONE,
        TEST_STUDENT_ID,
    )
    student.set_balance(balance)
    return student


def make_room(room_id: str = TEST_ROOM_ID) -> Room:
    """Create a sample room for booking tests."""
    return Room(room_id, TEST_ROOM_NAME, TEST_BUILDING, TEST_CAPACITY, TEST_PRICE_PER_HOUR, TEST_OPENING_HOURS)


def slot_text(start_time: datetime, end_time: datetime) -> str:
    """Format a time slot in the same format used by Room."""
    return f"{start_time:%Y-%m-%d %H:%M}-{end_time:%Y-%m-%d %H:%M}"


def test_search_available_room() -> None:
    """Test that the controller can find an available room."""
    controller = BookingController()
    room = make_room()
    room.set_available_time_slots([slot_text(BASE_START_TIME, BASE_END_TIME)])
    controller.add_room(room)

    result = controller.search_rooms(TEST_BUILDING, SEARCH_START_TEXT, SEARCH_END_TEXT)

    assert result["success"] is True
    assert result["rooms"] == [room]


def test_create_booking_success() -> None:
    """Test that a valid booking can be created."""
    controller = BookingController()
    student = make_student()
    room = make_room()
    room.set_available_time_slots([slot_text(BASE_START_TIME, BASE_END_TIME)])

    result = controller.create_booking(student, room, BASE_START_TIME, BASE_END_TIME, False)

    assert result["success"] is True
    assert result["booking"].get_status() == BOOKING_STATUS_CONFIRMED
    assert len(student.get_active_bookings()) == 1


def test_invalid_duration_fails() -> None:
    """Test that bookings shorter than 1 hour are rejected."""
    controller = BookingController()
    student = make_student()
    room = make_room()
    room.set_available_time_slots([slot_text(BASE_START_TIME, SHORT_END_TIME)])

    result = controller.create_booking(student, room, BASE_START_TIME, SHORT_END_TIME, False)

    assert result["success"] is False
    assert result["reason"] == REASON_INVALID_DURATION


def test_booking_limit_fails() -> None:
    """Test that a student cannot create more than 3 active bookings."""
    controller = BookingController()
    student = make_student()
    room = make_room()

    for index in range(BOOKING_LIMIT_COUNT):
        start_time = datetime(2026, 5, 12 + index, 10, 0)
        end_time = datetime(2026, 5, 12 + index, 12, 0)
        room.set_available_time_slots(room.get_available_time_slots() + [slot_text(start_time, end_time)])
        result = controller.create_booking(student, room, start_time, end_time, False)
        assert result["success"] is True

    room.set_available_time_slots(room.get_available_time_slots() + [slot_text(FOURTH_BOOKING_START, FOURTH_BOOKING_END)])
    result = controller.create_booking(student, room, FOURTH_BOOKING_START, FOURTH_BOOKING_END, False)

    assert result["success"] is False
    assert result["reason"] == REASON_BOOKING_LIMIT_REACHED


def test_regular_cancellation_refunds_balance() -> None:
    """Test that an early cancellation returns the booking price."""
    controller = BookingController()
    student = make_student()
    room = make_room()
    room.set_available_time_slots([slot_text(BASE_START_TIME, BASE_END_TIME)])

    booking_result = controller.create_booking(student, room, BASE_START_TIME, BASE_END_TIME, False)
    booking = booking_result["booking"]
    balance_after_payment = student.get_balance()

    cancel_result = controller.cancel_booking(
        student,
        booking.get_booking_id(),
        True,
        current_time=EARLY_CANCELLATION_TIME,
    )

    assert cancel_result["success"] is True
    assert cancel_result["reason"] == CANCELLATION_REGULAR
    assert cancel_result["refund"] == booking.get_total_price()
    assert student.get_balance() == balance_after_payment + booking.get_total_price()


def test_late_cancellation_has_no_refund() -> None:
    """Test that a late cancellation does not refund the student."""
    controller = BookingController()
    student = make_student()
    room = make_room()
    start_time = datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=LATE_CANCELLATION_START_OFFSET)
    end_time = start_time + timedelta(hours=1)
    room.set_available_time_slots([slot_text(start_time, end_time)])

    booking_result = controller.create_booking(student, room, start_time, end_time, False)
    booking = booking_result["booking"]
    balance_after_payment = student.get_balance()

    cancel_result = controller.cancel_booking(
        student,
        booking.get_booking_id(),
        True,
        current_time=start_time - timedelta(minutes=LATE_CANCELLATION_CHECK_OFFSET),
    )

    assert cancel_result["success"] is True
    assert cancel_result["reason"] == CANCELLATION_LATE
    assert cancel_result["refund"] == 0.0
    assert student.get_balance() == balance_after_payment
    assert student.get_late_cancellation_count() == 1


def run_all_tests() -> None:
    """Run all booking tests without needing an external test framework."""
    test_search_available_room()
    test_create_booking_success()
    test_invalid_duration_fails()
    test_booking_limit_fails()
    test_regular_cancellation_refunds_balance()
    test_late_cancellation_has_no_refund()
    print("All booking tests passed.")


if __name__ == "__main__":
    run_all_tests()


