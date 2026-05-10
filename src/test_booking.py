from datetime import datetime, timedelta

from controllers.booking_controller import BookingController
from entity_classes import Room, Student


def make_student(balance: float = 500.0) -> Student:
    """Create a sample student for booking tests."""
    student = Student(
        "test@student.monash.edu",
        "Password1",
        "Test",
        "Student",
        "0412345678",
        "S001",
    )
    student.set_balance(balance)
    return student


def make_room(room_id: str = "R001") -> Room:
    """Create a sample room for booking tests."""
    return Room(room_id, "Study Room", "BLD1", 4, 20.0, "09:00-18:00")


def slot_text(start_time: datetime, end_time: datetime) -> str:
    """Format a time slot in the same format used by Room."""
    return f"{start_time:%Y-%m-%d %H:%M}-{end_time:%Y-%m-%d %H:%M}"


def test_search_available_room() -> None:
    """Test that the controller can find an available room."""
    controller = BookingController()
    room = make_room()
    start_time = datetime(2026, 5, 12, 10, 0)
    end_time = datetime(2026, 5, 12, 12, 0)
    room.set_available_time_slots([slot_text(start_time, end_time)])
    controller.add_room(room)

    result = controller.search_rooms("BLD1", "2026-05-12 10:00", "2026-05-12 12:00")

    assert result["success"] is True
    assert result["rooms"] == [room]


def test_create_booking_success() -> None:
    """Test that a valid booking can be created."""
    controller = BookingController()
    student = make_student()
    room = make_room()
    start_time = datetime(2026, 5, 12, 10, 0)
    end_time = datetime(2026, 5, 12, 12, 0)
    room.set_available_time_slots([slot_text(start_time, end_time)])

    result = controller.create_booking(student, room, start_time, end_time, False)

    assert result["success"] is True
    assert result["booking"].get_status() == "confirmed"
    assert len(student.get_active_bookings()) == 1


def test_invalid_duration_fails() -> None:
    """Test that bookings shorter than 1 hour are rejected."""
    controller = BookingController()
    student = make_student()
    room = make_room()
    start_time = datetime(2026, 5, 12, 10, 0)
    end_time = datetime(2026, 5, 12, 10, 30)
    room.set_available_time_slots([slot_text(start_time, end_time)])

    result = controller.create_booking(student, room, start_time, end_time, False)

    assert result["success"] is False
    assert result["reason"] == "invalid_duration"


def test_booking_limit_fails() -> None:
    """Test that a student cannot create more than 3 active bookings."""
    controller = BookingController()
    student = make_student()
    room = make_room()

    for index in range(3):
        start_time = datetime(2026, 5, 12 + index, 10, 0)
        end_time = datetime(2026, 5, 12 + index, 12, 0)
        room.set_available_time_slots(room.get_available_time_slots() + [slot_text(start_time, end_time)])
        result = controller.create_booking(student, room, start_time, end_time, False)
        assert result["success"] is True

    fourth_start = datetime(2026, 5, 20, 10, 0)
    fourth_end = datetime(2026, 5, 20, 12, 0)
    room.set_available_time_slots(room.get_available_time_slots() + [slot_text(fourth_start, fourth_end)])
    result = controller.create_booking(student, room, fourth_start, fourth_end, False)

    assert result["success"] is False
    assert result["reason"] == "booking_limit_reached"


def test_regular_cancellation_refunds_balance() -> None:
    """Test that an early cancellation returns the booking price."""
    controller = BookingController()
    student = make_student()
    room = make_room()
    start_time = datetime(2026, 5, 12, 10, 0)
    end_time = datetime(2026, 5, 12, 12, 0)
    room.set_available_time_slots([slot_text(start_time, end_time)])

    booking_result = controller.create_booking(student, room, start_time, end_time, False)
    booking = booking_result["booking"]
    balance_after_payment = student.get_balance()

    cancel_result = controller.cancel_booking(
        student,
        booking.get_booking_id(),
        True,
        current_time=datetime(2026, 5, 11, 10, 0),
    )

    assert cancel_result["success"] is True
    assert cancel_result["reason"] == "regular_cancellation"
    assert cancel_result["refund"] == booking.get_total_price()
    assert student.get_balance() == balance_after_payment + booking.get_total_price()


def test_late_cancellation_has_no_refund() -> None:
    """Test that a late cancellation does not refund the student."""
    controller = BookingController()
    student = make_student()
    room = make_room()
    start_time = datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=20)
    end_time = start_time + timedelta(hours=1)
    room.set_available_time_slots([slot_text(start_time, end_time)])

    booking_result = controller.create_booking(student, room, start_time, end_time, False)
    booking = booking_result["booking"]
    balance_after_payment = student.get_balance()

    cancel_result = controller.cancel_booking(
        student,
        booking.get_booking_id(),
        True,
        current_time=start_time - timedelta(minutes=10),
    )

    assert cancel_result["success"] is True
    assert cancel_result["reason"] == "late_cancellation"
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
