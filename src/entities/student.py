"""
Student entity.
Covers: Acct 1-12
"""
from datetime import datetime
from typing import List, Optional


from entities.user import User
from entities.activity_record import ActivityRecord


class Student(User):
    """Student entity (Account Management 1-13, Booking, Checkout)"""

    def __init__(self, email: str, password: str, first_name: str, last_name: str,
                 phone: str, student_id: str) -> None:
        super().__init__(email, password, first_name, last_name, phone)
        self.__student_id: str = student_id
        self.__balance: float = 0.0
        self.__booking_ban_status: bool = False
        self.__late_cancellation_count: int = 0
        self.__no_show_count: int = 0
        self.__deal_package_hours: float = 0.0
        self.__bookings: List['Booking'] = []
        self.__activity_history: List['ActivityRecord'] = []
        self.__used_promo_codes: List[str] = []

    # --- Accessors ---
    def get_student_id(self) -> str:
        return self.__student_id

    def get_balance(self) -> float:
        return self.__balance

    def get_booking_ban_status(self) -> bool:
        return self.__booking_ban_status

    def get_late_cancellation_count(self) -> int:
        return self.__late_cancellation_count

    def get_no_show_count(self) -> int:
        return self.__no_show_count

    def get_deal_package_hours(self) -> float:
        return self.__deal_package_hours

    def get_bookings(self) -> List['Booking']:
        return self.__bookings

    def get_activity_history(self) -> List['ActivityRecord']:
        return self.__activity_history

    def get_used_promo_codes(self) -> List[str]:
        return self.__used_promo_codes

    # --- Mutators ---
    def set_student_id(self, student_id: str) -> None:
        self.__student_id = student_id

    def set_balance(self, balance: float) -> None:
        self.__balance = balance

    def set_booking_ban_status(self, status: bool) -> None:
        self.__booking_ban_status = status

    def set_late_cancellation_count(self, count: int) -> None:
        self.__late_cancellation_count = count

    def set_no_show_count(self, count: int) -> None:
        self.__no_show_count = count

    def set_deal_package_hours(self, hours: float) -> None:
        self.__deal_package_hours = hours

    # --- Business Methods ---
    def get_role(self) -> str:
        return "student"

    def add_funds(self, amount: float) -> bool:
        """Add funds (Acct 12)"""
        if amount <= 0:
            return False
        self.__balance += amount
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "recharge", f"Added ${amount}", amount))
        return True

    def deposit_funds(self, amount: float) -> None:
        """Deposit funds"""
        self.add_funds(amount)

    def deduct_balance(self, amount: float) -> bool:
        """Deduct balance"""
        if self.__balance >= amount:
            self.__balance -= amount
            return True
        return False

    def is_eligible_to_book(self) -> bool:
        """Check booking eligibility (Book 7)"""
        return not self.__booking_ban_status

    def has_reached_booking_limit(self) -> bool:
        """Check if booking limit reached (Book 10): max 3"""
        active = [b for b in self.__bookings if b.get_status() == "confirmed"]
        return len(active) >= 3

    def add_booking(self, booking: 'Booking') -> None:
        """Add booking to list"""
        self.__bookings.append(booking)
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "booking", str(booking), booking.get_total_price()))

    def remove_booking(self, booking: 'Booking') -> None:
        """Remove booking"""
        if booking in self.__bookings:
            self.__bookings.remove(booking)

    def record_late_cancellation(self) -> None:
        """Record late cancellation (Book 3)"""
        self.__late_cancellation_count += 1
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "late_cancellation", "Late cancellation recorded", 0.0))
        self._check_ban_threshold()

    def record_no_show(self) -> None:
        """Record no show"""
        self.__no_show_count += 1
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "no_show", "No show recorded", 0.0))
        self._check_ban_threshold()

    def _check_ban_threshold(self) -> None:
        """Check if ban threshold reached"""
        if (self.__late_cancellation_count + self.__no_show_count) >= 3:
            self.__booking_ban_status = True

    def add_deal_package_hours(self, hours: float) -> None:
        """Add deal package hours (Checkout 7)"""
        self.__deal_package_hours += hours

    def deduct_deal_package_hours(self, hours: float) -> bool:
        """Deduct deal package hours (Checkout 5)"""
        if self.__deal_package_hours >= hours:
            self.__deal_package_hours -= hours
            return True
        return False

    def has_used_promo_code(self, code: str) -> bool:
        """Check if promo code has been used (Checkout 4)"""
        return code in self.__used_promo_codes

    def mark_promo_code_used(self, code: str) -> None:
        """Mark promo code used"""
        self.__used_promo_codes.append(code)

    def get_active_bookings(self) -> List['Booking']:
        """Get active bookings list"""
        return [b for b in self.__bookings if b.get_status() == "confirmed"]

    def get_activity_history_page(self, page: int, page_size: int = 10) -> List['ActivityRecord']:
        """Get activity history page (Acct 10)"""
        start = (page - 1) * page_size
        end = start + page_size
        return self.__activity_history[start:end]

