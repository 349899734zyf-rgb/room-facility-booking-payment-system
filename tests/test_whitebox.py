"""
MSSRB — White-box Testing (Statement & Branch Coverage)
Goal: Cover all uncovered lines in entity_classes.py and controller_classes.py
Strategy: Trace each branch (True/False) through Control Flow Graphs
"""
import unittest
import sys
import os
sys.path.insert(0, r"d:\5136\project 2\src")

from entities.user import User
from entities.student import Student
from entities.admin import Admin
from entities.activity_record import ActivityRecord
from controllers.auth_controller import AuthController
from controllers.account_controller import AccountController

from entities.room import Room
from entities.equipment import Equipment
from controllers.room_controller import RoomController
from controllers.admin_controller import AdminController

from entities.booking import Booking
from controllers.booking_controller import BookingController

from entities.promo_code import PromoCode
from entities.deal_package import DealPackage
from entities.order import Order
from controllers.payment_controller import PaymentController
from datetime import datetime, timedelta


def make_student(**kw):
    s = Student("s@student.monash.edu", "Pass1234", "John", "Doe",
                "0412345678", "12345678")
    if kw.get("balance"):
        s.add_funds(kw["balance"])
    if kw.get("banned"):
        s.set_booking_ban_status(True)
    return s

def make_room():
    return Room("RM0001", "Room A", "BldgA", 10, 15.0, "09:00-21:00")

def future(h=24):
    return datetime.now() + timedelta(hours=h)


# ================================================================
# WB-1: User.__str__ and verify_password branches
# CFG: verify_password → [match?] → True / False
# ================================================================
class TestWB_User(unittest.TestCase):
    def test_str(self):
        """WB — User.__str__ (line 80)"""
        s = make_student()
        self.assertIn("John Doe", str(s))

    def test_verify_password_true(self):
        """WB — Branch: password matches → True"""
        s = make_student()
        self.assertTrue(s.verify_password("Pass1234"))

    def test_verify_password_false(self):
        """WB — Branch: password mismatch → False"""
        s = make_student()
        self.assertFalse(s.verify_password("Wrong"))


# ================================================================
# WB-2: Student accessors/mutators not hit by BVT
# Covers lines: 120, 126, 129, 132, 136, 139, 145, 148, 151
# ================================================================
class TestWB_StudentAccessors(unittest.TestCase):
    def test_get_no_show_count(self):
        s = make_student()
        self.assertEqual(s.get_no_show_count(), 0)

    def test_get_bookings(self):
        s = make_student()
        self.assertEqual(s.get_bookings(), [])

    def test_get_activity_history(self):
        s = make_student()
        self.assertEqual(s.get_activity_history(), [])

    def test_get_used_promo_codes(self):
        s = make_student()
        self.assertEqual(s.get_used_promo_codes(), [])

    def test_set_student_id(self):
        s = make_student()
        s.set_student_id("99999999")
        self.assertEqual(s.get_student_id(), "99999999")

    def test_set_balance(self):
        s = make_student()
        s.set_balance(50.0)
        self.assertEqual(s.get_balance(), 50.0)

    def test_set_late_cancellation_count(self):
        s = make_student()
        s.set_late_cancellation_count(2)
        self.assertEqual(s.get_late_cancellation_count(), 2)

    def test_set_no_show_count(self):
        s = make_student()
        s.set_no_show_count(1)
        self.assertEqual(s.get_no_show_count(), 1)

    def test_set_deal_package_hours(self):
        s = make_student()
        s.set_deal_package_hours(5.0)
        self.assertEqual(s.get_deal_package_hours(), 5.0)


# ================================================================
# WB-3: Student.record_no_show — all branches
# CFG: [increment count] → [append history] → [check threshold]
#      threshold: [total >= 3?] → True: ban / False: skip
# ================================================================
class TestWB_RecordNoShow(unittest.TestCase):
    def test_no_show_increments(self):
        """WB — no_show count incremented (lines 222-226)"""
        s = make_student()
        s.record_no_show()
        self.assertEqual(s.get_no_show_count(), 1)

    def test_no_show_adds_history(self):
        """WB — activity history records no_show"""
        s = make_student()
        s.record_no_show()
        self.assertEqual(s.get_activity_history()[-1].get_record_type(), "no_show")

    def test_no_show_triggers_ban(self):
        """WB — 3 no-shows → banned (threshold branch True)"""
        s = make_student()
        for _ in range(3):
            s.record_no_show()
        self.assertTrue(s.get_booking_ban_status())

    def test_no_show_under_threshold(self):
        """WB — 2 no-shows → not banned (threshold branch False)"""
        s = make_student()
        s.record_no_show()
        s.record_no_show()
        self.assertFalse(s.get_booking_ban_status())

    def test_mixed_late_and_noshow_ban(self):
        """WB — 2 late + 1 no-show = 3 → banned"""
        s = make_student()
        s.record_late_cancellation()
        s.record_late_cancellation()
        s.record_no_show()
        self.assertTrue(s.get_booking_ban_status())


# ================================================================
# WB-4: Room.__str__, update_availability branches
# CFG: update_availability:
#   [available?] → True: [not in list?] → add
#                → False: [in list?] → remove
# ================================================================
class TestWB_Room(unittest.TestCase):
    def test_str(self):
        """WB — Room.__str__ (line 432-435)"""
        r = make_room()
        self.assertIn("RM0001", str(r))
        self.assertIn("Room A", str(r))

    def test_update_availability_add(self):
        """WB — Branch: available=True, slot not in list → add"""
        r = make_room()
        r.update_availability("09:00-10:00", True)
        self.assertIn("09:00-10:00", r.get_available_time_slots())

    def test_update_availability_add_duplicate(self):
        """WB — Branch: available=True, slot already in list → skip"""
        r = make_room()
        r.set_available_time_slots(["09:00-10:00"])
        r.update_availability("09:00-10:00", True)
        self.assertEqual(r.get_available_time_slots().count("09:00-10:00"), 1)

    def test_update_availability_remove(self):
        """WB — Branch: available=False, slot in list → remove"""
        r = make_room()
        r.set_available_time_slots(["09:00-10:00"])
        r.update_availability("09:00-10:00", False)
        self.assertNotIn("09:00-10:00", r.get_available_time_slots())

    def test_update_availability_remove_missing(self):
        """WB — Branch: available=False, slot not in list → skip"""
        r = make_room()
        r.update_availability("15:00-16:00", False)
        self.assertEqual(r.get_available_time_slots(), [])

    def test_room_accessors_uncovered(self):
        """WB — opening_hours, is_student_in_room (lines 365, 374)"""
        r = make_room()
        self.assertEqual(r.get_opening_hours(), "09:00-21:00")
        self.assertFalse(r.get_is_student_in_room())

    def test_room_mutators_uncovered(self):
        """WB — set_room_id, set_price_per_hour (lines 378, 390)"""
        r = make_room()
        r.set_room_id("RM9999")
        self.assertEqual(r.get_room_id(), "RM9999")
        r.set_price_per_hour(25.0)
        self.assertEqual(r.get_price_per_hour(), 25.0)


# ================================================================
# WB-5: Booking — calculate_duration, is_late_cancellation, cancel
# CFG cancel: [set cancelled] → [is_late?]
#              → True: return "late_cancellation"
#              → False: return "regular_cancellation"
# ================================================================
class TestWB_Booking(unittest.TestCase):
    def _make_booking(self, start_delta_h=24):
        s = make_student()
        r = make_room()
        start = future(start_delta_h)
        end = start + timedelta(hours=2)
        return Booking("BK0001", s, r, start, end, False, 30.0)

    def test_calculate_duration(self):
        """WB — calculate_duration_hours (line 512-513)"""
        b = self._make_booking()
        self.assertAlmostEqual(b.calculate_duration_hours(), 2.0)

    def test_is_late_cancellation_false(self):
        """WB — Branch: start > 30 min away → False"""
        b = self._make_booking(24)
        self.assertFalse(b.is_late_cancellation())

    def test_cancel_regular(self):
        """WB — Branch: not late → 'regular_cancellation'"""
        b = self._make_booking(24)
        self.assertEqual(b.cancel(), "regular_cancellation")

    def test_booking_str(self):
        """WB — Booking.__str__ (lines 533-538)"""
        b = self._make_booking()
        text = str(b)
        self.assertIn("BK0001", text)
        self.assertIn("Room A", text)

    def test_booking_accessors_uncovered(self):
        """WB — get_booking_id, get_student, get_equipment_rental, etc."""
        b = self._make_booking()
        self.assertEqual(b.get_booking_id(), "BK0001")
        self.assertIsNotNone(b.get_student())
        self.assertFalse(b.get_equipment_rental())
        self.assertEqual(b.get_payment_method(), "")
        self.assertIsNone(b.get_promo_code_used())

    def test_booking_mutators_uncovered(self):
        """WB — set_promo_code_used, set_total_price (lines 502, 505)"""
        b = self._make_booking()
        b.set_promo_code_used("SAVE10")
        self.assertEqual(b.get_promo_code_used(), "SAVE10")
        b.set_total_price(20.0)
        self.assertEqual(b.get_total_price(), 20.0)


# ================================================================
# WB-6: PromoCode — is_valid branches
# CFG: [code.strip() != ""] → True / False
# ================================================================
class TestWB_PromoCode(unittest.TestCase):
    def test_is_valid_true(self):
        """WB — Branch: non-empty code → True (line 576)"""
        pc = PromoCode("SAVE10", 10.0)
        self.assertTrue(pc.is_valid())

    def test_is_valid_false(self):
        """WB — Branch: empty code → False"""
        pc = PromoCode("", 10.0)
        self.assertFalse(pc.is_valid())

    def test_mutators_uncovered(self):
        """WB — set_code, set_discount_amount (lines 568, 571)"""
        pc = PromoCode("OLD", 5.0)
        pc.set_code("NEW")
        self.assertEqual(pc.get_code(), "NEW")
        pc.set_discount_amount(15.0)
        self.assertEqual(pc.get_discount_amount(), 15.0)

    def test_get_used_by_students(self):
        """WB — line 564"""
        pc = PromoCode("X", 1.0)
        self.assertEqual(pc.get_used_by_students(), [])


# ================================================================
# WB-7: DealPackage — uncovered accessors/mutators
# ================================================================
class TestWB_DealPackage(unittest.TestCase):
    def test_accessors(self):
        """WB — get_package_id, set_price, set_hours (lines 609, 619, 622)"""
        dp = DealPackage("DP001", 100.0, 12.0)
        self.assertEqual(dp.get_package_id(), "DP001")
        dp.set_price(80.0)
        self.assertEqual(dp.get_price(), 80.0)
        dp.set_hours(10.0)
        self.assertEqual(dp.get_hours(), 10.0)


# ================================================================
# WB-8: Equipment — uncovered lines
# ================================================================
class TestWB_Equipment(unittest.TestCase):
    def test_accessors(self):
        """WB — lines 645, 648, 654, 657"""
        eq = Equipment("EQ001", "Projector", 50.0)
        self.assertEqual(eq.get_equipment_id(), "EQ001")
        self.assertEqual(eq.get_name(), "Projector")
        self.assertEqual(eq.get_rental_fee(), 10.0)
        self.assertTrue(eq.get_is_available())

    def test_set_is_available(self):
        """WB — line 664"""
        eq = Equipment("EQ001", "Projector", 50.0)
        eq.set_is_available(False)
        self.assertFalse(eq.get_is_available())

    def test_str(self):
        """WB — lines 672-673"""
        eq = Equipment("EQ001", "Projector", 50.0)
        self.assertIn("Available", str(eq))
        eq.set_is_available(False)
        self.assertIn("In Use", str(eq))


# ================================================================
# WB-9: ActivityRecord — uncovered accessors + __str__
# ================================================================
class TestWB_ActivityRecord(unittest.TestCase):
    def test_accessors(self):
        """WB — lines 697, 703, 706"""
        now = datetime.now()
        ar = ActivityRecord(now, "booking", "Test details", 15.0)
        self.assertEqual(ar.get_date(), now)
        self.assertEqual(ar.get_details(), "Test details")
        self.assertEqual(ar.get_amount(), 15.0)

    def test_str(self):
        """WB — line 709"""
        ar = ActivityRecord(datetime.now(), "booking", "Test", 10.0)
        text = str(ar)
        self.assertIn("BOOKING", text)
        self.assertIn("$10.00", text)


# ================================================================
# WB-10: Order — calculate_final_price + uncovered accessors
# ================================================================
class TestWB_Order(unittest.TestCase):
    def _make_order(self):
        s = make_student()
        r = make_room()
        b = Booking("BK0001", s, r, future(24), future(24) + timedelta(hours=1),
                    False, 15.0)
        return Order("OD0001", b, 15.0, "balance")

    def test_calculate_final_price(self):
        """WB — line 765"""
        o = self._make_order()
        self.assertEqual(o.calculate_final_price(), 15.0)

    def test_accessors(self):
        """WB — lines 736, 745"""
        o = self._make_order()
        self.assertEqual(o.get_order_id(), "OD0001")
        self.assertEqual(o.get_promo_discount(), 0.0)


# ================================================================
# WB-11: Admin — uncovered accessors
# ================================================================
class TestWB_Admin(unittest.TestCase):
    def test_set_admin_id(self):
        """WB — line 308"""
        a = Admin("a@monash.edu", "Admin123", "J", "S", "0400000000", "ADM001")
        a.set_admin_id("ADM999")
        self.assertEqual(a.get_admin_id(), "ADM999")

    def test_get_promotion_ideas(self):
        """WB — line 304"""
        a = Admin("a@monash.edu", "Admin123", "J", "S", "0400000000", "ADM001")
        self.assertEqual(a.get_promotion_ideas(), [])


# ================================================================
# WB-12: AuthController — register_student branch: duplicate email
# CFG: [empty?] → [valid email?] → [valid pwd?] → [valid mobile?]
#      → [duplicate?] → True: None / False: create
# ================================================================
class TestWB_AuthController(unittest.TestCase):
    def test_register_duplicate_email(self):
        """WB — Branch: duplicate email → None (lines 82-83)"""
        ctrl = AuthController()
        ctrl.register_student("a@student.monash.edu", "Pass1234",
                              "A", "B", "0412345678", "111")
        dup = ctrl.register_student("a@student.monash.edu", "Pass5678",
                                    "C", "D", "0498765432", "222")
        self.assertIsNone(dup)

    def test_register_invalid_mobile(self):
        """WB — Branch: invalid mobile → None (line 79)"""
        ctrl = AuthController()
        result = ctrl.register_student("a@student.monash.edu", "Pass1234",
                                       "A", "B", "1234567890", "111")
        self.assertIsNone(result)

    def test_find_student_not_found(self):
        """WB — Branch: no match → None (line 146)"""
        ctrl = AuthController()
        self.assertIsNone(ctrl.find_student_by_id("NONEXIST"))

    def test_find_student_found(self):
        """WB — Branch: match found → return (lines 143-145)"""
        ctrl = AuthController()
        ctrl.register_student("a@student.monash.edu", "Pass1234",
                              "A", "B", "0412345678", "111")
        self.assertIsNotNone(ctrl.find_student_by_id("111"))

    def test_update_mobile_mismatch(self):
        """WB — Branch: mobiles don't match → False (line 137)"""
        ctrl = AuthController()
        s = make_student()
        self.assertFalse(ctrl.update_mobile(s, "0412345678", "0498765432"))


# ================================================================
# WB-13: BookingController — find_room_by_id, find_booking_by_id
# CFG: [loop rooms] → [id match?] → True: return / False: continue
#      → end: return None
# ================================================================
class TestWB_BookingController(unittest.TestCase):
    def test_set_rooms(self):
        """WB — line 235"""
        ctrl = BookingController()
        r = make_room()
        ctrl.set_rooms([r])
        self.assertEqual(len(ctrl.get_rooms()), 1)

    def test_get_all_bookings(self):
        """WB — line 238"""
        ctrl = BookingController()
        self.assertEqual(ctrl.get_all_bookings(), [])

    def test_find_room_found(self):
        """WB — Branch: match → return room (lines 333-336)"""
        ctrl = BookingController()
        r = make_room()
        ctrl.set_rooms([r])
        self.assertEqual(ctrl.find_room_by_id("RM0001"), r)

    def test_find_room_not_found(self):
        """WB — Branch: no match → None"""
        ctrl = BookingController()
        self.assertIsNone(ctrl.find_room_by_id("RM9999"))

    def test_find_booking_found(self):
        """WB — Branch: match → return booking (lines 340-343)"""
        ctrl = BookingController()
        s = make_student()
        r = make_room()
        start = future(24)
        end = start + timedelta(hours=1)
        b = Booking("BK9001", s, r, start, end, False, 15.0)
        ctrl.get_all_bookings().append(b)
        self.assertEqual(ctrl.find_booking_by_id("BK9001"), b)

    def test_find_booking_not_found(self):
        """WB — Branch: no match → None"""
        ctrl = BookingController()
        self.assertIsNone(ctrl.find_booking_by_id("BK9999"))

    def test_late_cancel_branch(self):
        """WB — cancel_booking late branch (line 317)"""
        ctrl = BookingController()
        s = make_student(balance=100.0)
        r = make_room()
        # Booking starts in 10 minutes → late cancellation
        start = datetime.now() + timedelta(minutes=10)
        end = start + timedelta(hours=1)
        b = Booking("BK0001", s, r, start, end, False, 15.0)
        s.add_booking(b)
        ctrl.get_all_bookings().append(b)
        result = ctrl.cancel_booking(s, b)
        self.assertEqual(result["type"], "late_cancellation")
        self.assertEqual(result["refund"], 0.0)


# ================================================================
# WB-14: PaymentController — check_balance_sufficient
# CFG: [balance >= amount?] → True / False
# ================================================================
class TestWB_PaymentController(unittest.TestCase):
    def test_check_balance_sufficient_true(self):
        """WB — Branch: enough → True (line 379 not hit previously)"""
        ctrl = PaymentController()
        s = make_student(balance=100.0)
        self.assertTrue(ctrl.check_balance_sufficient(s, 50.0))

    def test_check_balance_sufficient_false(self):
        """WB — Branch: not enough → False"""
        ctrl = PaymentController()
        s = make_student()
        self.assertFalse(ctrl.check_balance_sufficient(s, 50.0))

    def test_confirm_order(self):
        """WB — line 581: confirm_order sets booking fields"""
        ctrl = PaymentController()
        s = make_student()
        r = make_room()
        b = Booking("BK0001", s, r, future(24),
                    future(24) + timedelta(hours=1), False, 15.0)
        order = ctrl.create_order(b, "balance")
        self.assertTrue(ctrl.confirm_order(order, s))
        self.assertEqual(b.get_payment_method(), "balance")


# ================================================================
# WB-15: User mutators (lines 51, 57, 60)
# ================================================================
class TestWB_UserMutators(unittest.TestCase):
    def test_set_email(self):
        s = make_student()
        s.set_email("new@student.monash.edu")
        self.assertEqual(s.get_email(), "new@student.monash.edu")

    def test_set_first_name(self):
        s = make_student()
        s.set_first_name("Jane")
        self.assertEqual(s.get_first_name(), "Jane")

    def test_set_last_name(self):
        s = make_student()
        s.set_last_name("Smith")
        self.assertEqual(s.get_last_name(), "Smith")

    def test_get_password(self):
        """WB — line 38"""
        s = make_student()
        self.assertEqual(s.get_password(), "Pass1234")


# ================================================================
# WB-16: Room mutators not covered
# ================================================================
class TestWB_RoomMutators(unittest.TestCase):
    def test_set_building(self):
        r = make_room()
        r.set_building("BldgB")
        self.assertEqual(r.get_building(), "BldgB")

    def test_set_capacity(self):
        r = make_room()
        r.set_capacity(20)
        self.assertEqual(r.get_capacity(), 20)

    def test_set_opening_hours(self):
        r = make_room()
        r.set_opening_hours("08:00-20:00")
        self.assertEqual(r.get_opening_hours(), "08:00-20:00")

    def test_set_room_name(self):
        r = make_room()
        r.set_room_name("Room B")
        self.assertEqual(r.get_room_name(), "Room B")


if __name__ == "__main__":
    unittest.main()
