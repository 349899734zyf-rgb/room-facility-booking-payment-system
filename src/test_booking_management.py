"""
Boundary value tests for Booking Management user stories Book 1 to Book 15.

This test file adapts the team-provided test scenarios to the current booking
module interfaces in entities.booking and controllers.booking_controller.
"""

import unittest
from datetime import datetime, timedelta

from booking_constants import (
    BOOKING_STATUS_CONFIRMED,
    CANCELLATION_LATE,
    CANCELLATION_REGULAR,
    CANCELLATION_STOPPED,
    REASON_BANNED,
    REASON_BOOKING_CREATED,
    REASON_BOOKING_LIMIT_REACHED,
    REASON_BOOKING_NOT_FOUND,
    REASON_INVALID_DURATION,
    REASON_INVALID_INPUT,
    REASON_NO_ROOMS,
    REASON_ROOM_UNAVAILABLE,
    REASON_ROOMS_FOUND,
)
from controllers.booking_controller import BookingController
from entities.booking import Booking
from entity_classes import Equipment, Room, Student

STUDENT_EMAIL = "s@student.monash.edu"
STUDENT_PASSWORD = "Pass1234"
STUDENT_FIRST_NAME = "John"
STUDENT_LAST_NAME = "Doe"
STUDENT_PHONE = "0412345678"
STUDENT_ID = "12345678"
DEFAULT_BALANCE = 500.0

ROOM_ID = "RM0001"
ROOM_NAME = "Room A"
BUILDING = "BldgA"
ROOM_CAPACITY = 10
ROOM_PRICE = 15.0
OPENING_HOURS = "09:00-21:00"
TIME_FORMAT = "%Y-%m-%d %H:%M"


def make_student(banned: bool = False, balance: float = DEFAULT_BALANCE) -> Student:
    """Create a student for booking management tests."""
    student = Student(
        STUDENT_EMAIL,
        STUDENT_PASSWORD,
        STUDENT_FIRST_NAME,
        STUDENT_LAST_NAME,
        STUDENT_PHONE,
        STUDENT_ID,
    )
    if banned:
        student.set_booking_ban_status(True)
    if balance > 0:
        student.add_funds(balance)
    return student


def make_room(price: float = ROOM_PRICE, slots: list[str] | None = None) -> Room:
    """Create a room with optional available time slots."""
    room = Room(ROOM_ID, ROOM_NAME, BUILDING, ROOM_CAPACITY, price, OPENING_HOURS)
    if slots:
        room.set_available_time_slots(slots)
    return room


def future(hours_ahead: int = 24) -> datetime:
    """Return a future datetime rounded to the current minute."""
    now = datetime.now().replace(second=0, microsecond=0)
    return now + timedelta(hours=hours_ahead)


def slot_text(start_time: datetime, end_time: datetime) -> str:
    """Format a Room time slot string used by the current Room entity."""
    return f"{start_time.strftime(TIME_FORMAT)}-{end_time.strftime(TIME_FORMAT)}"


class TestBook01FilterRooms(unittest.TestCase):
    """Book 1: filter rooms by building and availability."""

    def setUp(self) -> None:
        """Create one searchable room."""
        self.ctrl = BookingController()
        self.start = future()
        self.end = self.start + timedelta(hours=1)
        self.room = make_room(slots=[slot_text(self.start, self.end)])
        self.ctrl.add_room(self.room)

    def test_matching_building_and_time(self) -> None:
        """Correct building and available time returns the room."""
        result = self.ctrl.search_rooms(
            BUILDING,
            self.start.strftime(TIME_FORMAT),
            self.end.strftime(TIME_FORMAT),
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["reason"], REASON_ROOMS_FOUND)
        self.assertEqual(result["rooms"], [self.room])

    def test_wrong_building(self) -> None:
        """Wrong building returns no rooms."""
        result = self.ctrl.search_rooms(
            "BldgZ",
            self.start.strftime(TIME_FORMAT),
            self.end.strftime(TIME_FORMAT),
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_NO_ROOMS)

    def test_wrong_time(self) -> None:
        """Unavailable time returns no rooms."""
        later_start = self.start + timedelta(hours=3)
        later_end = later_start + timedelta(hours=1)
        result = self.ctrl.search_rooms(
            BUILDING,
            later_start.strftime(TIME_FORMAT),
            later_end.strftime(TIME_FORMAT),
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_NO_ROOMS)

    def test_invalid_time(self) -> None:
        """Invalid time format returns invalid input."""
        result = self.ctrl.search_rooms(BUILDING, "09:00", "10:00")
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_INVALID_INPUT)


class TestBook02CancelEarly(unittest.TestCase):
    """Book 2: regular cancellation refunds balance."""

    def setUp(self) -> None:
        """Create one regular cancellable booking."""
        self.ctrl = BookingController()
        self.student = make_student()
        self.room = make_room()
        self.start = future(24)
        self.end = self.start + timedelta(hours=1)
        self.room.set_available_time_slots([slot_text(self.start, self.end)])
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            self.start,
            self.end,
            False,
        )
        self.booking = result["booking"]

    def test_regular_cancel_refund(self) -> None:
        """Cancellation more than 30 minutes before start gives refund."""
        balance_after_payment = self.student.get_balance()
        result = self.ctrl.cancel_booking(
            self.student,
            self.booking.get_booking_id(),
            True,
            current_time=self.start - timedelta(hours=2),
        )
        self.assertEqual(result["reason"], CANCELLATION_REGULAR)
        self.assertGreater(result["refund"], 0)
        self.assertGreater(self.student.get_balance(), balance_after_payment)


class TestBook03LateCancellation(unittest.TestCase):
    """Book 3: late cancellation count and ban threshold."""

    def setUp(self) -> None:
        """Create a student for late cancellation tests."""
        self.student = make_student()

    def test_zero_late_not_banned(self) -> None:
        """Zero late cancellations does not ban the student."""
        self.assertFalse(self.student.get_booking_ban_status())

    def test_one_late_not_banned(self) -> None:
        """One late cancellation does not ban the student."""
        self.student.record_late_cancellation()
        self.assertEqual(self.student.get_late_cancellation_count(), 1)
        self.assertFalse(self.student.get_booking_ban_status())

    def test_three_late_banned(self) -> None:
        """Three late cancellations bans the student."""
        for _ in range(3):
            self.student.record_late_cancellation()
        self.assertTrue(self.student.get_booking_ban_status())


class TestBook04EquipmentBundle(unittest.TestCase):
    """Book 4: equipment deposit boundary."""

    def test_with_equipment_deposit(self) -> None:
        """Equipment has a positive deposit amount."""
        equipment = Equipment("EQ001", 50.0)
        self.assertGreater(equipment.get_deposit_amount(), 0)

    def test_controller_deposit_setting(self) -> None:
        """Controller can update equipment deposit."""
        ctrl = BookingController()
        self.assertTrue(ctrl.set_equipment_deposit(100.0))
        self.assertEqual(ctrl.get_equipment_deposit(), 100.0)


class TestBook05CreateBooking(unittest.TestCase):
    """Book 5: create new booking."""

    def setUp(self) -> None:
        """Create controller, student, room, and slot."""
        self.ctrl = BookingController()
        self.student = make_student()
        self.room = make_room()
        self.start = future(24)
        self.end = self.start + timedelta(hours=1)
        self.room.set_available_time_slots([slot_text(self.start, self.end)])

    def test_valid_booking(self) -> None:
        """Eligible student with valid slot creates booking."""
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            self.start,
            self.end,
            False,
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["reason"], REASON_BOOKING_CREATED)

    def test_banned_student(self) -> None:
        """Banned student cannot create booking."""
        self.student.set_booking_ban_status(True)
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            self.start,
            self.end,
            False,
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_BANNED)

    def test_invalid_duration(self) -> None:
        """Duration shorter than one hour is rejected."""
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            self.start,
            self.start + timedelta(minutes=30),
            False,
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_INVALID_DURATION)


class TestBook06CancelExisting(unittest.TestCase):
    """Book 6: cancel existing booking."""

    def setUp(self) -> None:
        """Create one active booking."""
        self.ctrl = BookingController()
        self.student = make_student()
        self.room = make_room()
        self.start = future(24)
        self.end = self.start + timedelta(hours=1)
        self.room.set_available_time_slots([slot_text(self.start, self.end)])
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            self.start,
            self.end,
            False,
        )
        self.booking = result["booking"]

    def test_cancel_existing(self) -> None:
        """Existing booking can be cancelled."""
        result = self.ctrl.cancel_booking(
            self.student,
            self.booking.get_booking_id(),
            True,
            current_time=self.start - timedelta(hours=2),
        )
        self.assertTrue(result["success"])
        self.assertEqual(len(self.ctrl.get_student_bookings(self.student)), 0)

    def test_cancel_missing_booking(self) -> None:
        """Missing booking ID returns booking not found."""
        result = self.ctrl.cancel_booking(self.student, "BAD_ID", True)
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_BOOKING_NOT_FOUND)


class TestBook07CheckEligibility(unittest.TestCase):
    """Book 7: check eligibility."""

    def test_eligible_student(self) -> None:
        """Student with no ban and no limit can make booking."""
        result = BookingController().check_eligibility(make_student())
        self.assertTrue(result["can_make_booking"])
        self.assertFalse(result["is_banned"])
        self.assertFalse(result["has_reached_limit"])

    def test_banned_student(self) -> None:
        """Banned student cannot make booking."""
        result = BookingController().check_eligibility(make_student(banned=True))
        self.assertFalse(result["can_make_booking"])
        self.assertTrue(result["is_banned"])


class TestBook08DurationRules(unittest.TestCase):
    """Book 8: duration rules."""

    def setUp(self) -> None:
        """Create a base time."""
        self.ctrl = BookingController()
        self.base = future(24)

    def test_30_minutes_fails(self) -> None:
        """30 minutes is shorter than minimum duration."""
        self.assertFalse(
            self.ctrl.validate_duration(self.base, self.base + timedelta(minutes=30)),
        )

    def test_60_minutes_passes(self) -> None:
        """60 minutes is accepted."""
        self.assertTrue(
            self.ctrl.validate_duration(self.base, self.base + timedelta(minutes=60)),
        )

    def test_90_minutes_passes(self) -> None:
        """90 minutes is accepted as a 30-minute increment."""
        self.assertTrue(
            self.ctrl.validate_duration(self.base, self.base + timedelta(minutes=90)),
        )

    def test_75_minutes_fails(self) -> None:
        """75 minutes is not a 30-minute increment."""
        self.assertFalse(
            self.ctrl.validate_duration(self.base, self.base + timedelta(minutes=75)),
        )


class TestBook09SelectRoom(unittest.TestCase):
    """Book 9: select an available room."""

    def test_valid_selection(self) -> None:
        """Room in available list can be selected."""
        ctrl = BookingController()
        room = make_room()
        selected = ctrl.select_room([room], ROOM_ID)
        self.assertEqual(selected, room)

    def test_invalid_selection(self) -> None:
        """Room outside available list cannot be selected."""
        ctrl = BookingController()
        room = make_room()
        selected = ctrl.select_room([room], "RM9999")
        self.assertIsNone(selected)


class TestBook10BookingLimit(unittest.TestCase):
    """Book 10: booking limit."""

    def setUp(self) -> None:
        """Create student and room."""
        self.student = make_student()
        self.room = make_room()

    def add_confirmed_bookings(self, count: int) -> None:
        """Add confirmed bookings directly to student."""
        for index in range(count):
            start = future(24 + index * 2)
            end = start + timedelta(hours=1)
            booking = Booking(
                f"BK{index:04d}",
                self.student,
                self.room,
                start,
                end,
                False,
                ROOM_PRICE,
            )
            booking.set_status(BOOKING_STATUS_CONFIRMED)
            self.student.add_booking(booking)

    def test_three_bookings_at_limit(self) -> None:
        """Three active bookings reaches the limit."""
        self.add_confirmed_bookings(3)
        self.assertTrue(self.student.has_reached_booking_limit())

    def test_blocked_at_limit(self) -> None:
        """Creating a fourth booking is blocked."""
        self.add_confirmed_bookings(3)
        ctrl = BookingController()
        start = future(48)
        end = start + timedelta(hours=1)
        result = ctrl.create_booking(self.student, self.room, start, end, False)
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_BOOKING_LIMIT_REACHED)


class TestBook11ReviewBeforeCancel(unittest.TestCase):
    """Book 11: review bookings before cancellation."""

    def test_no_bookings(self) -> None:
        """Student with no bookings returns empty active list."""
        bookings = BookingController().get_student_bookings(make_student())
        self.assertEqual(len(bookings), 0)


class TestBook12ViewWhileBanned(unittest.TestCase):
    """Book 12: view existing bookings while banned."""

    def test_banned_cannot_book(self) -> None:
        """Banned student cannot make new booking."""
        self.assertFalse(make_student(banned=True).is_eligible_to_book())

    def test_banned_sees_existing_list(self) -> None:
        """Banned student can still access active booking list."""
        bookings = make_student(banned=True).get_active_bookings()
        self.assertIsNotNone(bookings)


class TestBook13ViewBeforeDecision(unittest.TestCase):
    """Book 13: view current bookings before decision."""

    def test_no_bookings(self) -> None:
        """Empty booking list is returned for no bookings."""
        self.assertEqual(len(make_student().get_active_bookings()), 0)


class TestBook14StopCancellation(unittest.TestCase):
    """Book 14: stop cancellation request."""

    def test_stop_keeps_booking(self) -> None:
        """confirm_cancel=False keeps the original booking."""
        ctrl = BookingController()
        student = make_student()
        room = make_room()
        start = future(24)
        end = start + timedelta(hours=1)
        room.set_available_time_slots([slot_text(start, end)])
        booking_result = ctrl.create_booking(student, room, start, end, False)
        booking = booking_result["booking"]

        result = ctrl.cancel_booking(student, booking.get_booking_id(), False)

        self.assertEqual(result["reason"], CANCELLATION_STOPPED)
        self.assertEqual(len(student.get_active_bookings()), 1)
        self.assertEqual(student.get_active_bookings()[0].get_status(), "confirmed")


class TestBook15MakeBooking(unittest.TestCase):
    """Book 15: make booking end-to-end."""

    def setUp(self) -> None:
        """Create a valid booking setup."""
        self.ctrl = BookingController()
        self.student = make_student()
        self.room = make_room()
        self.start = future(24)
        self.end = self.start + timedelta(hours=2)
        self.room.set_available_time_slots([slot_text(self.start, self.end)])

    def test_full_flow_success(self) -> None:
        """All conditions met creates a booking."""
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            self.start,
            self.end,
            False,
        )
        booking = result["booking"]
        self.assertTrue(result["success"])
        self.assertEqual(booking.get_status(), "confirmed")
        self.assertEqual(len(self.student.get_active_bookings()), 1)

    def test_banned_blocks_flow(self) -> None:
        """Banned student is blocked from booking."""
        self.student.set_booking_ban_status(True)
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            self.start,
            self.end,
            False,
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_BANNED)

    def test_unavailable_room_blocks_flow(self) -> None:
        """Unavailable room blocks booking."""
        other_start = self.start + timedelta(days=1)
        other_end = other_start + timedelta(hours=1)
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            other_start,
            other_end,
            False,
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], REASON_ROOM_UNAVAILABLE)

    def test_price_calculation(self) -> None:
        """Price equals duration multiplied by room price."""
        result = self.ctrl.create_booking(
            self.student,
            self.room,
            self.start,
            self.end,
            False,
        )
        self.assertEqual(result["booking"].get_total_price(), 30.0)


if __name__ == "__main__":
    unittest.main()
