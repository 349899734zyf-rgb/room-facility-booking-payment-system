"""
MSSRB — Room Management BVT (Boundary Value Testing)
User Stories: Room 1 ~ Room 11
Test Strategy: min-, min, middle, max, max+ for each boundary condition
"""
import unittest
import sys
sys.path.insert(0, r"d:\5136\project 2\src")

from entities.student import Student
from entities.admin import Admin
from entities.room import Room
from entities.booking import Booking
from entities.equipment import Equipment
from controllers.room_controller import RoomController
from controllers.admin_controller import AdminController
from datetime import datetime, timedelta


# ============================================================
# Room 1: Add a Room
# Boundary: name/building/hours non-empty, capacity > 0, price > 0
# ============================================================
class TestRoom01_AddRoom(unittest.TestCase):
    """Room 1 — Add a Room [SP: 5]
    AC: Valid input adds room; invalid/blank input shows error.
    BVT: capacity and price boundaries
    """
    def setUp(self):
        self.ctrl = RoomController()

    def test_bvt_valid_room(self):
        """BVT — all valid inputs — PASS"""
        room = self.ctrl.add_room("Study Room A", "Building A", 10, 15.0, "09:00-21:00")
        self.assertIsNotNone(room)
        self.assertEqual(len(self.ctrl.get_rooms()), 1)

    def test_bvt_capacity_zero(self):
        """BVT min- — capacity = 0 — FAIL"""
        room = self.ctrl.add_room("Room B", "Building B", 0, 15.0, "09:00-21:00")
        self.assertIsNone(room)

    def test_bvt_capacity_negative(self):
        """BVT min-- — capacity = -1 — FAIL"""
        room = self.ctrl.add_room("Room C", "Building C", -1, 15.0, "09:00-21:00")
        self.assertIsNone(room)

    def test_bvt_capacity_one(self):
        """BVT min — capacity = 1 — PASS"""
        room = self.ctrl.add_room("Room D", "Building D", 1, 15.0, "09:00-21:00")
        self.assertIsNotNone(room)

    def test_bvt_capacity_large(self):
        """BVT max — capacity = 100 — PASS"""
        room = self.ctrl.add_room("Room E", "Building E", 100, 15.0, "09:00-21:00")
        self.assertIsNotNone(room)

    def test_bvt_price_zero(self):
        """BVT min- — price = 0 — FAIL"""
        room = self.ctrl.add_room("Room F", "Building F", 10, 0.0, "09:00-21:00")
        self.assertIsNone(room)

    def test_bvt_price_negative(self):
        """BVT min-- — price = -5.0 — FAIL"""
        room = self.ctrl.add_room("Room G", "Building G", 10, -5.0, "09:00-21:00")
        self.assertIsNone(room)

    def test_bvt_price_min(self):
        """BVT min — price = 0.01 — PASS"""
        room = self.ctrl.add_room("Room H", "Building H", 10, 0.01, "09:00-21:00")
        self.assertIsNotNone(room)

    def test_bvt_blank_name(self):
        """BVT — blank room name — FAIL"""
        room = self.ctrl.add_room("", "Building I", 10, 15.0, "09:00-21:00")
        self.assertIsNone(room)

    def test_bvt_blank_building(self):
        """BVT — blank building — FAIL"""
        room = self.ctrl.add_room("Room J", "", 10, 15.0, "09:00-21:00")
        self.assertIsNone(room)

    def test_bvt_room_in_list(self):
        """AC: New room appears in room list"""
        self.ctrl.add_room("Room K", "Building K", 5, 10.0, "09:00-17:00")
        self.assertEqual(len(self.ctrl.get_rooms()), 1)


# ============================================================
# Room 2: Record a Promotion Idea
# Boundary: idea text non-empty
# ============================================================
class TestRoom02_RecordPromotionIdea(unittest.TestCase):
    """Room 2 — Record Promotion Idea [SP: 1]
    AC: Submitted idea recorded; abandoned input not recorded.
    BVT: idea text length
    """
    def setUp(self):
        self.ctrl = AdminController()
        self.admin = Admin("admin@monash.edu", "Admin123",
                           "Jane", "Smith", "0498765432", "ADM001")

    def test_bvt_min_minus_empty(self):
        """BVT min- — empty string — FAIL"""
        self.assertFalse(self.ctrl.record_promotion_idea(self.admin, ""))

    def test_bvt_min_minus_whitespace(self):
        """BVT min- — whitespace only — FAIL"""
        self.assertFalse(self.ctrl.record_promotion_idea(self.admin, "   "))

    def test_bvt_min_one_char(self):
        """BVT min — single character — PASS"""
        self.assertTrue(self.ctrl.record_promotion_idea(self.admin, "A"))

    def test_bvt_middle(self):
        """BVT middle — normal text — PASS"""
        self.assertTrue(self.ctrl.record_promotion_idea(self.admin, "50% off for new students"))

    def test_bvt_max_long(self):
        """BVT max — very long text — PASS"""
        self.assertTrue(self.ctrl.record_promotion_idea(self.admin, "A" * 500))


# ============================================================
# Room 3: View Room Management Menu
# Boundary: number of rooms in list (0, 1, many)
# ============================================================
class TestRoom03_ViewRoomMgmtMenu(unittest.TestCase):
    """Room 3 — View Room Mgmt Menu [SP: 2]
    AC: Room list displayed, functions available.
    BVT: room count
    """
    def setUp(self):
        self.ctrl = RoomController()

    def test_bvt_min_zero_rooms(self):
        """BVT min — 0 rooms — empty list"""
        self.assertEqual(len(self.ctrl.get_rooms()), 0)

    def test_bvt_one_room(self):
        """BVT min+ — 1 room"""
        self.ctrl.add_room("Room A", "BldgA", 10, 15.0, "09:00-21:00")
        self.assertEqual(len(self.ctrl.get_rooms()), 1)

    def test_bvt_multiple_rooms(self):
        """BVT middle — 3 rooms"""
        for i in range(3):
            self.ctrl.add_room(f"Room {i}", f"Bldg{i}", 10, 15.0, "09:00-21:00")
        self.assertEqual(len(self.ctrl.get_rooms()), 3)


# ============================================================
# Room 4: Remove an Existing Room
# Boundary: room exists vs doesn't exist
# ============================================================
class TestRoom04_RemoveRoom(unittest.TestCase):
    """Room 4 — Remove Room [SP: 2]
    AC: Successful removal, non-existent shows not found.
    BVT: room ID existence
    """
    def setUp(self):
        self.ctrl = RoomController()
        self.room = self.ctrl.add_room("Room A", "BldgA", 10, 15.0, "09:00-21:00")

    def test_bvt_remove_existing(self):
        """BVT — remove existing room — PASS"""
        self.assertTrue(self.ctrl.remove_room(self.room.get_room_id()))
        self.assertEqual(len(self.ctrl.get_rooms()), 0)

    def test_bvt_remove_nonexistent(self):
        """BVT — remove nonexistent ID — FAIL"""
        self.assertFalse(self.ctrl.remove_room("RM9999"))

    def test_bvt_remove_empty_id(self):
        """BVT min- — empty string ID — FAIL"""
        self.assertFalse(self.ctrl.remove_room(""))


# ============================================================
# Room 5: Record Student Presence and Equipment Status
# Boundary: boolean states (True/False)
# ============================================================
class TestRoom05_StudentPresenceEquipment(unittest.TestCase):
    """Room 5 — Student Presence & Equipment [SP: 3]
    AC: Update student presence and equipment usage.
    BVT: room existence and boolean states
    """
    def setUp(self):
        self.ctrl = RoomController()
        self.room = self.ctrl.add_room("Room A", "BldgA", 10, 15.0, "09:00-21:00")

    def test_bvt_set_both_true(self):
        """BVT max — both present — PASS"""
        rid = self.room.get_room_id()
        self.assertTrue(self.ctrl.update_room_usage_status(rid, True, True))
        self.assertTrue(self.room.get_is_student_in_room())
        self.assertTrue(self.room.get_is_equipment_rented())

    def test_bvt_set_both_false(self):
        """BVT min — both absent — PASS"""
        rid = self.room.get_room_id()
        self.assertTrue(self.ctrl.update_room_usage_status(rid, False, False))

    def test_bvt_nonexistent_room(self):
        """BVT — nonexistent room — FAIL"""
        self.assertFalse(self.ctrl.update_room_usage_status("RM9999", True, True))


# ============================================================
# Room 6: Update Room Available Time Slots
# Boundary: number of slots (0, 1, many)
# ============================================================
class TestRoom06_UpdateTimeSlots(unittest.TestCase):
    """Room 6 — Update Time Slots [SP: 3]
    AC: Update available time period, display latest availability.
    BVT: slot count
    """
    def setUp(self):
        self.ctrl = RoomController()
        self.room = self.ctrl.add_room("Room A", "BldgA", 10, 15.0, "09:00-21:00")

    def test_bvt_min_empty_slots(self):
        """BVT min — 0 slots"""
        rid = self.room.get_room_id()
        self.assertTrue(self.ctrl.update_room_time_slots(rid, []))
        self.assertEqual(len(self.room.get_available_time_slots()), 0)

    def test_bvt_one_slot(self):
        """BVT min+ — 1 slot"""
        rid = self.room.get_room_id()
        self.assertTrue(self.ctrl.update_room_time_slots(rid, ["09:00-10:00"]))
        self.assertEqual(len(self.room.get_available_time_slots()), 1)

    def test_bvt_multiple_slots(self):
        """BVT middle — 5 slots"""
        slots = [f"{9+i}:00-{10+i}:00" for i in range(5)]
        rid = self.room.get_room_id()
        self.assertTrue(self.ctrl.update_room_time_slots(rid, slots))
        self.assertEqual(len(self.room.get_available_time_slots()), 5)

    def test_bvt_nonexistent_room(self):
        """BVT — nonexistent room — FAIL"""
        self.assertFalse(self.ctrl.update_room_time_slots("RM9999", ["09:00-10:00"]))


# ============================================================
# Room 7: View Predicted Room Income
# Boundary: slots (0, 1, many) × equipment (yes/no)
# ============================================================
class TestRoom07_PredictedIncome(unittest.TestCase):
    """Room 7 — Predicted Income [SP: 3]
    AC: Income displayed, includes room price and equipment rental.
    BVT: income calculation boundaries
    """
    def setUp(self):
        self.ctrl = RoomController()
        self.room = self.ctrl.add_room("Room A", "BldgA", 10, 15.0, "09:00-21:00")

    def test_bvt_min_no_slots_no_equipment(self):
        """BVT min — 0 booked slots, no equipment — income=0"""
        income = self.ctrl.get_predicted_income(self.room.get_room_id())
        self.assertEqual(income, 0.0)

    def test_bvt_one_slot_no_equipment(self):
        """BVT min+ — 1 slot, no equipment — income=15"""
        self.room.set_available_time_slots(["09:00-10:00"])
        income = self.ctrl.get_predicted_income(self.room.get_room_id())
        self.assertEqual(income, 15.0)

    def test_bvt_one_slot_with_equipment(self):
        """BVT — 1 slot + equipment — income=15+10=25"""
        self.room.set_available_time_slots(["09:00-10:00"])
        self.room.set_is_equipment_rented(True)
        income = self.ctrl.get_predicted_income(self.room.get_room_id())
        self.assertEqual(income, 25.0)

    def test_bvt_multiple_slots(self):
        """BVT max — 5 slots, no equipment — income=75"""
        self.room.set_available_time_slots(["s1", "s2", "s3", "s4", "s5"])
        income = self.ctrl.get_predicted_income(self.room.get_room_id())
        self.assertEqual(income, 75.0)

    def test_bvt_nonexistent_room(self):
        """BVT — nonexistent room — returns 0"""
        self.assertEqual(self.ctrl.get_predicted_income("RM9999"), 0.0)


# ============================================================
# Room 8: Change Room Information
# Boundary: valid vs nonexistent room, field updates
# ============================================================
class TestRoom08_ChangeRoomInfo(unittest.TestCase):
    """Room 8 — Change Room Info [SP: 3]
    AC: Update name, building, capacity, price, hours.
    BVT: update existing vs nonexistent room
    """
    def setUp(self):
        self.ctrl = RoomController()
        self.room = self.ctrl.add_room("Room A", "BldgA", 10, 15.0, "09:00-21:00")

    def test_bvt_update_all_fields(self):
        """BVT — update all fields — PASS"""
        rid = self.room.get_room_id()
        updates = {"name": "New Name", "building": "BldgB", "capacity": 20,
                   "price": 25.0, "opening_hours": "08:00-22:00"}
        self.assertTrue(self.ctrl.update_room_info(rid, updates))
        self.assertEqual(self.room.get_room_name(), "New Name")
        self.assertEqual(self.room.get_capacity(), 20)

    def test_bvt_update_single_field(self):
        """BVT min — update 1 field only — PASS"""
        rid = self.room.get_room_id()
        self.assertTrue(self.ctrl.update_room_info(rid, {"name": "Updated"}))
        self.assertEqual(self.room.get_room_name(), "Updated")
        self.assertEqual(self.room.get_building(), "BldgA")  # unchanged

    def test_bvt_update_nonexistent(self):
        """BVT — nonexistent room — FAIL"""
        self.assertFalse(self.ctrl.update_room_info("RM9999", {"name": "X"}))


# ============================================================
# Room 9: Update Booking Status
# Boundary: booking exists vs doesn't
# ============================================================
class TestRoom09_UpdateBookingStatus(unittest.TestCase):
    """Room 9 — Update Booking Status [SP: 2]
    AC: Status update saved, reflected in student records.
    BVT: booking existence
    """
    def setUp(self):
        self.ctrl = AdminController()
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")
        room = Room("RM0001", "Room A", "BldgA", 10, 15.0, "09:00-21:00")
        now = datetime.now() + timedelta(days=1)
        self.booking = Booking("BK0001", self.student, room, now,
                               now + timedelta(hours=2), False, 30.0)
        self.ctrl.set_all_bookings([self.booking])

    def test_bvt_update_existing(self):
        """BVT — update existing booking status — PASS"""
        self.assertTrue(self.ctrl.update_booking_status("BK0001", "completed"))
        self.assertEqual(self.booking.get_status(), "completed")

    def test_bvt_update_nonexistent(self):
        """BVT — nonexistent booking — FAIL"""
        self.assertFalse(self.ctrl.update_booking_status("BK9999", "completed"))


# ============================================================
# Room 10: Ban a Student from Booking
# Boundary: already banned vs not banned
# ============================================================
class TestRoom10_BanStudent(unittest.TestCase):
    """Room 10 — Ban Student [SP: 3]
    AC: Admin bans student, system updates status, student cannot book.
    BVT: ban status transitions
    """
    def setUp(self):
        self.ctrl = AdminController()
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")

    def test_bvt_ban_unbanned_student(self):
        """BVT — ban an unbanned student — PASS"""
        self.assertTrue(self.ctrl.ban_student(self.student))
        self.assertTrue(self.student.get_booking_ban_status())

    def test_bvt_ban_already_banned(self):
        """BVT — ban already banned student — FAIL (already banned)"""
        self.student.set_booking_ban_status(True)
        self.assertFalse(self.ctrl.ban_student(self.student))

    def test_bvt_unban_banned_student(self):
        """BVT — unban a banned student — PASS"""
        self.student.set_booking_ban_status(True)
        self.assertTrue(self.ctrl.unban_student(self.student))
        self.assertFalse(self.student.get_booking_ban_status())

    def test_bvt_unban_not_banned(self):
        """BVT — unban already unbanned — FAIL"""
        self.assertFalse(self.ctrl.unban_student(self.student))

    def test_bvt_banned_cannot_book(self):
        """AC: Banned student cannot make new bookings"""
        self.ctrl.ban_student(self.student)
        self.assertFalse(self.student.is_eligible_to_book())


# ============================================================
# Room 11: Set Equipment Deposit Amount
# Boundary: deposit amount > 0
# ============================================================
class TestRoom11_SetEquipmentDeposit(unittest.TestCase):
    """Room 11 — Set Equipment Deposit [SP: 2]
    AC: Admin sets deposit amount, refunded when returned.
    BVT: deposit amount boundaries
    """
    def setUp(self):
        self.ctrl = AdminController()
        self.equipment = Equipment("EQ001", 50.0)
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")

    def test_bvt_min_minus_negative(self):
        """BVT min- — amount = -10 — FAIL"""
        self.assertFalse(self.ctrl.set_equipment_deposit(self.equipment, -10.0))

    def test_bvt_min_zero(self):
        """BVT min — amount = 0 — FAIL"""
        self.assertFalse(self.ctrl.set_equipment_deposit(self.equipment, 0.0))

    def test_bvt_min_plus(self):
        """BVT min+ — amount = 0.01 — PASS"""
        self.assertTrue(self.ctrl.set_equipment_deposit(self.equipment, 0.01))
        self.assertEqual(self.equipment.get_deposit_amount(), 0.01)

    def test_bvt_middle(self):
        """BVT middle — amount = 50.0 — PASS"""
        self.assertTrue(self.ctrl.set_equipment_deposit(self.equipment, 50.0))

    def test_bvt_max_large(self):
        """BVT max — amount = 500.0 — PASS"""
        self.assertTrue(self.ctrl.set_equipment_deposit(self.equipment, 500.0))

    def test_bvt_refund(self):
        """AC: Deposit refunded when equipment returned"""
        self.ctrl.set_equipment_deposit(self.equipment, 100.0)
        self.ctrl.refund_equipment_deposit(self.equipment, self.student)
        self.assertEqual(self.student.get_balance(), 100.0)


if __name__ == "__main__":
    unittest.main()
