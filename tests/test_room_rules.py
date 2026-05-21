import unittest
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, r"d:\5136\project 2\src")

from entities.student import Student
from entities.room import Room
from entities.booking import Booking
from controllers.booking_controller import BookingController
from controllers.payment_controller import PaymentController
from controllers.admin_controller import AdminController

class TestRoomRules(unittest.TestCase):
    def setUp(self):
        self.student = Student("s@student.monash.edu", "Pass1234", "John", "Doe", "0412345678", "12345678")
        self.student.add_funds(500.0)
        self.book_ctrl = BookingController()
        self.payment_ctrl = PaymentController()
        self.admin_ctrl = AdminController()

    def test_small_room_rules(self):
        room = Room("RM0001", "Small Room 1", "BldgA", 2, 10.0, "00:00-24:00") # price <= 10.0 -> Small
        self.assertEqual(room.get_room_type(), "Small")
        
        # Advance booking: any time (0 hours)
        now = datetime.now()
        start = now + timedelta(minutes=15)
        end = start + timedelta(hours=1)
        self.book_ctrl.set_rooms([room])
        room.update_availability(f"{self.book_ctrl.format_time(start)}-{self.book_ctrl.format_time(end)}", True)
        
        res = self.book_ctrl.create_booking(self.student, room, start, end, False, current_time=now)
        self.assertTrue(res["success"])
        booking = res["booking"]
        
        # Duration: >= 1 hour is valid (increment 30 min)
        # Cancel within 30 min is late cancellation
        cancel_time = now + timedelta(minutes=10) # start is now+15, so 5 mins before start. Late cancel.
        c_res = self.book_ctrl.cancel_booking(self.student, booking, True, current_time=cancel_time)
        self.assertEqual(c_res["type"], "late_cancellation")
        # 50% refund of room price (price was 10.0 for 1h)
        self.assertEqual(c_res["refund"], 5.0)

    def test_medium_room_rules(self):
        room = Room("RM0002", "Medium Room 1", "BldgA", 6, 40.0, "00:00-24:00") # price = 40.0 -> Medium
        self.assertEqual(room.get_room_type(), "Medium")
        
        # Advance booking: >= 3 hours required
        now = datetime.now()
        start_too_soon = now + timedelta(hours=2)
        end_too_soon = start_too_soon + timedelta(hours=2)
        self.book_ctrl.set_rooms([room])
        
        res1 = self.book_ctrl.create_booking(self.student, room, start_too_soon, end_too_soon, False, current_time=now)
        self.assertFalse(res1["success"])
        self.assertEqual(res1["reason"], "advance_booking_requirement_not_met")
        
        # Valid advance booking (>= 3 hours)
        start_valid = now + timedelta(hours=4)
        end_valid = start_valid + timedelta(hours=2)
        room.update_availability(f"{self.book_ctrl.format_time(start_valid)}-{self.book_ctrl.format_time(end_valid)}", True)
        
        res2 = self.book_ctrl.create_booking(self.student, room, start_valid, end_valid, False, current_time=now)
        self.assertTrue(res2["success"])
        booking = res2["booking"]
        
        # Duration: >= 2 hours required
        start_short = now + timedelta(hours=4)
        end_short = start_short + timedelta(hours=1.5)
        self.assertFalse(self.book_ctrl.validate_duration(start_short, end_short, "Medium"))

        # Late cancellation window: < 3 hours
        cancel_time = start_valid - timedelta(hours=2) # 2 hours before start -> late cancel
        c_res = self.book_ctrl.cancel_booking(self.student, booking, True, current_time=cancel_time)
        self.assertEqual(c_res["type"], "late_cancellation")
        # 50% refund of room price (price was 80.0 for 2h) -> 40.0
        self.assertEqual(c_res["refund"], 40.0)

    def test_large_room_rules(self):
        room = Room("RM0003", "Large Room 1", "BldgA", 10, 80.0, "00:00-24:00") # price = 80.0 -> Large
        self.assertEqual(room.get_room_type(), "Large")
        
        # Advance booking: >= 24 hours required
        now = datetime.now()
        start_too_soon = now + timedelta(hours=23)
        end_too_soon = start_too_soon + timedelta(hours=2)
        self.book_ctrl.set_rooms([room])
        
        res1 = self.book_ctrl.create_booking(self.student, room, start_too_soon, end_too_soon, False, current_time=now)
        self.assertFalse(res1["success"])
        self.assertEqual(res1["reason"], "advance_booking_requirement_not_met")
        
        # Valid advance booking (>= 24 hours)
        start_valid = now + timedelta(hours=25)
        end_valid = start_valid + timedelta(hours=2)
        room.update_availability(f"{self.book_ctrl.format_time(start_valid)}-{self.book_ctrl.format_time(end_valid)}", True)
        
        res2 = self.book_ctrl.create_booking(self.student, room, start_valid, end_valid, False, current_time=now)
        self.assertTrue(res2["success"])
        booking = res2["booking"]
        
        # Late cancellation window: < 4 hours
        cancel_time = start_valid - timedelta(hours=3) # 3 hours before start -> late cancel
        c_res = self.book_ctrl.cancel_booking(self.student, booking, True, current_time=cancel_time)
        self.assertEqual(c_res["type"], "late_cancellation")
        # 30% refund of room price (price was 160.0 for 2h) -> 48.0
        self.assertEqual(c_res["refund"], 48.0)

    def test_promo_and_deal_package_restrictions(self):
        # NEWBIE20 / NEWBEE20 validation restricted to Small room
        small_room = Room("RM0001", "Small Room", "BldgA", 2, 10.0, "00:00-24:00")
        medium_room = Room("RM0002", "Medium Room", "BldgA", 6, 40.0, "00:00-24:00")
        
        s_bk = Booking("BK001", self.student, small_room, datetime.now(), datetime.now() + timedelta(hours=1), False, 10.0)
        m_bk = Booking("BK002", self.student, medium_room, datetime.now(), datetime.now() + timedelta(hours=2), False, 80.0)
        
        # small room booking can use NEWBIE20
        p1 = self.payment_ctrl.validate_promo_code("NEWBIE20", self.student, s_bk)
        self.assertIsNotNone(p1)
        
        # medium room booking cannot use NEWBIE20
        p2 = self.payment_ctrl.validate_promo_code("NEWBIE20", self.student, m_bk)
        self.assertIsNone(p2)
        
        # deal package check
        self.assertTrue(self.payment_ctrl.can_use_deal_package(False, "Small"))
        self.assertFalse(self.payment_ctrl.can_use_deal_package(False, "Medium"))
