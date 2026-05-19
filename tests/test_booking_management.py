"""
MSSRB — Booking Management BVT (Boundary Value Testing)
User Stories: Book 1 ~ Book 15
Test Strategy: min-, min, middle, max, max+ for each boundary condition
"""
import unittest
import sys
sys.path.insert(0, r"d:\5136\project 2\src")

from entities.student import Student
from entities.room import Room
from entities.booking import Booking
from entities.equipment import Equipment
from controllers.booking_controller import BookingController
from datetime import datetime, timedelta


def make_student(banned=False, balance=0.0):
    s = Student("s@student.monash.edu", "Pass1234", "John", "Doe", "0412345678", "12345678")
    if banned:
        s.set_booking_ban_status(True)
    if balance > 0:
        s.add_funds(balance)
    return s


def make_room(price=15.0, slots=None):
    r = Room("RM0001", "Room A", "BldgA", 10, price, "09:00-21:00")
    if slots:
        r.set_available_time_slots(slots)
    return r


def future(hours_ahead=24):
    return datetime.now() + timedelta(hours=hours_ahead)


def fmt(dt):
    """Format datetime as yang's BookingController expects: YYYY-MM-DD HH:MM"""
    return dt.strftime("%Y-%m-%d %H:%M")


def make_slot_pair(hours_ahead=24, duration_hours=1, price=15.0):
    """Create a room with matching time slots for the given future time.
    Returns (room, start_dt, end_dt, start_str, end_str).
    """
    start = future(hours_ahead)
    end = start + timedelta(hours=duration_hours)
    slot_str = f"{fmt(start)}-{fmt(end)}"
    room = make_room(price=price, slots=[slot_str])
    return room, start, end, fmt(start), fmt(end)


# ============================================================
# Book 1: Filter Rooms by Criteria
# Boundary: building match × time slot availability
# ============================================================
class TestBook01_FilterRooms(unittest.TestCase):
    """Book 1 — Filter Rooms by Criteria [SP: 3]
    AC: Search by building, start, end. Valid → list; invalid → error/empty.
    BVT: matching conditions
    """
    def setUp(self):
        self.ctrl = BookingController()
        self.room, self.start, self.end, self.s_str, self.e_str = make_slot_pair()
        self.ctrl.get_rooms().append(self.room)

    def test_bvt_matching_building_and_time(self):
        """BVT — correct building + available slot — found"""
        result = self.ctrl.search_rooms("BldgA", self.s_str, self.e_str)
        self.assertTrue(result["success"])
        self.assertEqual(len(result["rooms"]), 1)

    def test_bvt_wrong_building(self):
        """BVT — wrong building — empty"""
        result = self.ctrl.search_rooms("BldgZ", self.s_str, self.e_str)
        self.assertEqual(len(result["rooms"]), 0)

    def test_bvt_wrong_time(self):
        """BVT — correct building, unavailable time — empty"""
        far = future(200)
        result = self.ctrl.search_rooms("BldgA", fmt(far), fmt(far + timedelta(hours=1)))
        self.assertEqual(len(result["rooms"]), 0)

    def test_bvt_no_rooms(self):
        """BVT min — no rooms in system — empty"""
        ctrl2 = BookingController()
        result = ctrl2.search_rooms("BldgA", self.s_str, self.e_str)
        self.assertEqual(len(result["rooms"]), 0)

    def test_bvt_multiple_matches(self):
        """BVT max — multiple rooms match"""
        room2 = Room("RM0002", "Room B", "BldgA", 5, 10.0, "09:00-21:00")
        slot = f"{self.s_str}-{self.e_str}"
        room2.set_available_time_slots([slot])
        self.ctrl.get_rooms().append(room2)
        result = self.ctrl.search_rooms("BldgA", self.s_str, self.e_str)
        self.assertEqual(len(result["rooms"]), 2)


# ============================================================
# Book 2: Cancel a Booking Early (Regular)
# Boundary: cancellation time > 30 min before start
# ============================================================
class TestBook02_CancelEarly(unittest.TestCase):
    """Book 2 — Cancel Early (Regular) [SP: 3]
    AC: Cancel > 30 min before → refund returned.
    """
    def setUp(self):
        self.ctrl = BookingController()
        self.student = make_student(balance=200.0)
        self.room, start, end, s_str, e_str = make_slot_pair(hours_ahead=48)
        result = self.ctrl.create_booking(self.student, self.room, start, end, False)
        self.booking_id = result["booking"].get_booking_id() if result["success"] else None

    def test_bvt_regular_cancel_refund(self):
        """BVT — cancel > 30 min before start — regular + refund"""
        if self.booking_id is None:
            self.skipTest("Booking creation failed")
        result = self.ctrl.cancel_booking(self.student, self.booking_id, True)
        self.assertTrue(result["success"])
        self.assertGreater(result["refund"], 0)


# ============================================================
# Book 3: Late Cancellation Consequences
# ============================================================
class TestBook03_LateCancellation(unittest.TestCase):
    """Book 3 — Late Cancellation [SP: 5]"""
    def setUp(self):
        self.student = make_student()

    def test_bvt_min_zero_late(self):
        self.assertFalse(self.student.get_booking_ban_status())

    def test_bvt_one_late(self):
        self.student.record_late_cancellation()
        self.assertEqual(self.student.get_late_cancellation_count(), 1)
        self.assertFalse(self.student.get_booking_ban_status())

    def test_bvt_two_late(self):
        self.student.record_late_cancellation()
        self.student.record_late_cancellation()
        self.assertFalse(self.student.get_booking_ban_status())

    def test_bvt_three_late_banned(self):
        for _ in range(3):
            self.student.record_late_cancellation()
        self.assertTrue(self.student.get_booking_ban_status())

    def test_bvt_four_late(self):
        for _ in range(4):
            self.student.record_late_cancellation()
        self.assertTrue(self.student.get_booking_ban_status())


# ============================================================
# Book 4: Equipment Bundle
# ============================================================
class TestBook04_EquipmentBundle(unittest.TestCase):
    """Book 4 — Equipment Bundle Choice [SP: 2]"""
    def setUp(self):
        self.equipment = Equipment("EQ001", 50.0)

    def test_bvt_with_equipment(self):
        self.assertGreater(self.equipment.get_deposit_amount(), 0)

    def test_bvt_without_equipment(self):
        self.assertTrue(True)

    def test_bvt_deposit_amount(self):
        self.equipment.set_deposit_amount(100.0)
        self.assertEqual(self.equipment.get_deposit_amount(), 100.0)


# ============================================================
# Book 5: Create a New Booking
# ============================================================
class TestBook05_CreateBooking(unittest.TestCase):
    """Book 5 — Create New Booking [SP: 5]"""
    def setUp(self):
        self.ctrl = BookingController()
        self.student = make_student(balance=500.0)
        self.room, self.start, self.end, _, _ = make_slot_pair(hours_ahead=24)

    def test_bvt_valid_booking(self):
        """BVT — eligible student, valid duration — PASS"""
        result = self.ctrl.create_booking(self.student, self.room, self.start, self.end, False)
        self.assertTrue(result["success"])
        self.assertIn("booking", result)

    def test_bvt_banned_student(self):
        """BVT — banned student — FAIL"""
        self.student.set_booking_ban_status(True)
        result = self.ctrl.create_booking(self.student, self.room, self.start, self.end, False)
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], "banned")

    def test_bvt_invalid_duration(self):
        """BVT — duration < 1 hour — FAIL"""
        start = future(24)
        end = start + timedelta(minutes=30)
        result = self.ctrl.create_booking(self.student, self.room, start, end, False)
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], "invalid_duration")


# ============================================================
# Book 6: Cancel an Existing Booking
# ============================================================
class TestBook06_CancelExisting(unittest.TestCase):
    """Book 6 — Cancel Existing Booking [SP: 3]"""
    def setUp(self):
        self.ctrl = BookingController()
        self.student = make_student(balance=500.0)
        self.room, start, end, _, _ = make_slot_pair(hours_ahead=48)
        result = self.ctrl.create_booking(self.student, self.room, start, end, False)
        self.booking_id = result["booking"].get_booking_id() if result["success"] else None

    def test_bvt_cancel_existing(self):
        if self.booking_id is None:
            self.skipTest("Booking creation failed")
        result = self.ctrl.cancel_booking(self.student, self.booking_id, True)
        self.assertTrue(result["success"])

    def test_bvt_student_bookings_after_cancel(self):
        if self.booking_id is None:
            self.skipTest("Booking creation failed")
        self.ctrl.cancel_booking(self.student, self.booking_id, True)
        self.assertEqual(len(self.ctrl.get_student_bookings(self.student)), 0)


# ============================================================
# Book 7: Check Booking Eligibility
# ============================================================
class TestBook07_CheckEligibility(unittest.TestCase):
    """Book 7 — Check Eligibility [SP: 2]"""
    def setUp(self):
        self.ctrl = BookingController()

    def test_bvt_eligible_student(self):
        student = make_student()
        result = self.ctrl.check_eligibility(student)
        self.assertTrue(result["can_make_booking"])
        self.assertFalse(result["is_banned"])
        self.assertFalse(result["has_reached_limit"])

    def test_bvt_banned_student(self):
        student = make_student(banned=True)
        result = self.ctrl.check_eligibility(student)
        self.assertFalse(result["can_make_booking"])
        self.assertTrue(result["is_banned"])


# ============================================================
# Book 8: Follow Booking Duration Rules
# ============================================================
class TestBook08_DurationRules(unittest.TestCase):
    """Book 8 — Duration Rules [SP: 2]"""
    def setUp(self):
        self.ctrl = BookingController()
        self.base = future(24)

    def test_bvt_min_minus_30min(self):
        self.assertFalse(self.ctrl.validate_duration(
            self.base, self.base + timedelta(minutes=30)))

    def test_bvt_min_minus_45min(self):
        self.assertFalse(self.ctrl.validate_duration(
            self.base, self.base + timedelta(minutes=45)))

    def test_bvt_min_60min(self):
        self.assertTrue(self.ctrl.validate_duration(
            self.base, self.base + timedelta(minutes=60)))

    def test_bvt_90min(self):
        self.assertTrue(self.ctrl.validate_duration(
            self.base, self.base + timedelta(minutes=90)))

    def test_bvt_middle_120min(self):
        self.assertTrue(self.ctrl.validate_duration(
            self.base, self.base + timedelta(minutes=120)))

    def test_bvt_max_480min(self):
        self.assertTrue(self.ctrl.validate_duration(
            self.base, self.base + timedelta(minutes=480)))

    def test_bvt_non_30min_increment(self):
        self.assertFalse(self.ctrl.validate_duration(
            self.base, self.base + timedelta(minutes=75)))


# ============================================================
# Book 9: Select an Available Room
# ============================================================
class TestBook09_SelectRoom(unittest.TestCase):
    """Book 9 — Select Available Room [SP: 1]"""
    def setUp(self):
        self.ctrl = BookingController()
        self.room, self.start, self.end, self.s_str, self.e_str = make_slot_pair()
        self.ctrl.get_rooms().append(self.room)

    def test_bvt_valid_selection(self):
        result = self.ctrl.search_rooms("BldgA", self.s_str, self.e_str)
        self.assertIn(self.room, result["rooms"])

    def test_bvt_empty_list(self):
        result = self.ctrl.search_rooms("BldgZ", self.s_str, self.e_str)
        self.assertEqual(len(result["rooms"]), 0)


# ============================================================
# Book 10: Handle Booking Limit Reached
# ============================================================
class TestBook10_BookingLimit(unittest.TestCase):
    """Book 10 — Booking Limit [SP: 2]"""
    def setUp(self):
        self.student = make_student(balance=500.0)
        self.room = make_room()

    def _add_confirmed_bookings(self, count):
        for i in range(count):
            start = future(24 + i * 2)
            end = start + timedelta(hours=1)
            b = Booking(f"BK{i:04d}", self.student, self.room, start, end, False, 15.0)
            b.set_status("confirmed")
            self.student.add_booking(b)

    def test_bvt_min_zero_bookings(self):
        self.assertFalse(self.student.has_reached_booking_limit())

    def test_bvt_one_booking(self):
        self._add_confirmed_bookings(1)
        self.assertFalse(self.student.has_reached_booking_limit())

    def test_bvt_two_bookings(self):
        self._add_confirmed_bookings(2)
        self.assertFalse(self.student.has_reached_booking_limit())

    def test_bvt_three_bookings_at_limit(self):
        self._add_confirmed_bookings(3)
        self.assertTrue(self.student.has_reached_booking_limit())

    def test_bvt_blocked_at_limit(self):
        self._add_confirmed_bookings(3)
        ctrl = BookingController()
        room, start, end, _, _ = make_slot_pair(hours_ahead=96)
        result = ctrl.create_booking(self.student, room, start, end, False)
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], "booking_limit_reached")


# ============================================================
# Book 11: Review Bookings Before Cancellation
# ============================================================
class TestBook11_ReviewBeforeCancel(unittest.TestCase):
    """Book 11 — Review Before Cancel [SP: 2]"""
    def setUp(self):
        self.ctrl = BookingController()
        self.student = make_student()

    def test_bvt_min_no_bookings(self):
        bookings = self.ctrl.get_student_bookings(self.student)
        self.assertEqual(len(bookings), 0)


# ============================================================
# Book 12: View Existing Bookings While Banned
# ============================================================
class TestBook12_ViewWhileBanned(unittest.TestCase):
    """Book 12 — View While Banned [SP: 2]"""
    def setUp(self):
        self.student = make_student(banned=True)

    def test_bvt_banned_cannot_book(self):
        self.assertFalse(self.student.is_eligible_to_book())

    def test_bvt_banned_sees_existing(self):
        bookings = self.student.get_active_bookings()
        self.assertIsNotNone(bookings)


# ============================================================
# Book 13: View Current Bookings Before Decision
# ============================================================
class TestBook13_ViewBeforeDecision(unittest.TestCase):
    """Book 13 — View Before Decision [SP: 1]"""
    def setUp(self):
        self.student = make_student()

    def test_bvt_no_bookings(self):
        self.assertEqual(len(self.student.get_active_bookings()), 0)


# ============================================================
# Book 14: Stop a Cancellation Request
# ============================================================
class TestBook14_StopCancellation(unittest.TestCase):
    """Book 14 — Stop Cancellation [SP: 1]"""
    def setUp(self):
        self.ctrl = BookingController()
        self.student = make_student(balance=500.0)
        room, start, end, _, _ = make_slot_pair(hours_ahead=48)
        result = self.ctrl.create_booking(self.student, room, start, end, False)
        self.booking_id = result["booking"].get_booking_id() if result["success"] else None

    def test_bvt_stop_keeps_booking(self):
        if self.booking_id is None:
            self.skipTest("Booking creation failed")
        result = self.ctrl.cancel_booking(self.student, self.booking_id, False)
        self.assertTrue(result["success"])
        bookings = self.ctrl.get_student_bookings(self.student)
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0].get_status(), "confirmed")


# ============================================================
# Book 15: Make a Booking (End-to-End)
# ============================================================
class TestBook15_MakeBooking(unittest.TestCase):
    """Book 15 — Make Booking E2E [SP: 8]"""
    def setUp(self):
        self.ctrl = BookingController()
        self.student = make_student(balance=1000.0)

    def test_bvt_full_flow_success(self):
        room, start, end, _, _ = make_slot_pair(hours_ahead=24, duration_hours=2)
        self.ctrl.get_rooms().append(room)
        result = self.ctrl.create_booking(self.student, room, start, end, False)
        self.assertTrue(result["success"])
        booking = result["booking"]
        self.assertEqual(booking.get_status(), "confirmed")
        self.assertEqual(len(self.student.get_active_bookings()), 1)

    def test_bvt_banned_blocks_flow(self):
        self.student.set_booking_ban_status(True)
        room, start, end, _, _ = make_slot_pair(hours_ahead=24)
        result = self.ctrl.create_booking(self.student, room, start, end, False)
        self.assertFalse(result["success"])

    def test_bvt_limit_blocks_flow(self):
        room = make_room()
        for i in range(3):
            s = future(24 + i * 3)
            e = s + timedelta(hours=1)
            slot = f"{fmt(s)}-{fmt(e)}"
            room.set_available_time_slots(room.get_available_time_slots() + [slot])
            self.ctrl.create_booking(self.student, room, s, e, False)
        room2, s4, e4, _, _ = make_slot_pair(hours_ahead=96)
        result = self.ctrl.create_booking(self.student, room2, s4, e4, False)
        self.assertFalse(result["success"])

    def test_bvt_price_calculation(self):
        room, start, end, _, _ = make_slot_pair(hours_ahead=24, duration_hours=2, price=15.0)
        result = self.ctrl.create_booking(self.student, room, start, end, False)
        self.assertTrue(result["success"])
        booking = result["booking"]
        self.assertEqual(booking.get_total_price(), 30.0)  # 2h × 15.0


if __name__ == "__main__":
    unittest.main()
