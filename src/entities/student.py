"""
Module: student.py
Layer: Entity
User Stories: Acct 1-12, Book 3.7/3.10, Checkout 4-7

Represents a student user who can register, manage their account,
search and book rooms, make payments, and view activity history.
"""
from datetime import datetime
from typing import List, Optional


from entities.user import User
from entities.activity_record import ActivityRecord
from booking_constants import (
    BAN_THRESHOLD,
    BOOKING_STATUS_CONFIRMED,
    MAX_ACTIVE_BOOKINGS,
)


class Student(User):
    """Student entity extending User.

    Responsibilities:
        - Manage account balance and fund top-ups (Acct 11-12)
        - Track booking list and enforce booking limit (Book 3.10)
        - Track ban status via late cancellation / no-show counts (Book 3.7)
        - Manage deal package hours for alternative payment (Checkout 6-7)
        - Record activity history for audit trail (Acct 9-10)
        - Track used promo codes to prevent re-use (Checkout 5)

    Collaborators:
        - Booking: linked bookings managed by BookingController
        - ActivityRecord: history entries for account activity display
    """

    def __init__(self, email: str, password: str, first_name: str, last_name: str,
                 phone: str, student_id: str) -> None:
        """Initialise a student with profile data and a unique student ID."""
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
        """Return the unique student identifier."""
        return self.__student_id

    def get_balance(self) -> float:
        """Return the current account balance."""
        return self.__balance

    def get_booking_ban_status(self) -> bool:
        """Return True if the student is currently banned from booking (Book 3.7)."""
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
        """Return 'student' as the user role (Acct 13)."""
        return "student"

    def add_funds(self, amount: float) -> bool:
        """Top up the student's balance and record the activity (Acct 12).

        Args:
            amount: Amount to add (must be positive).

        Returns:
            True if funds were added successfully, False if amount <= 0.
        """
        if amount <= 0:
            return False
        self.__balance += amount
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "recharge", f"Added ${amount}", amount))
        return True

    def deposit_funds(self, amount: float) -> None:
        """Convenience wrapper to add funds without checking return value."""
        self.add_funds(amount)

    def deduct_balance(self, amount: float) -> bool:
        """Deduct from balance if sufficient funds exist (Checkout 2).

        Returns:
            True if deduction succeeded, False if insufficient balance.
        """
        if self.__balance >= amount:
            self.__balance -= amount
            return True
        return False

    def is_eligible_to_book(self) -> bool:
        """Return True if the student is not banned from booking (Book 3.7)."""
        return not self.__booking_ban_status

    def has_reached_booking_limit(self) -> bool:
        """Return True if the student has MAX_ACTIVE_BOOKINGS active bookings (Book 3.10).

        Business Rules:
            - Only bookings with 'confirmed' status count towards the limit.
            - Maximum active bookings = MAX_ACTIVE_BOOKINGS (default 3).
        """
        active = [b for b in self.__bookings if b.get_status() == BOOKING_STATUS_CONFIRMED]
        return len(active) >= MAX_ACTIVE_BOOKINGS

    def add_booking(self, booking: 'Booking') -> None:
        """Add a booking to the student's booking list and record activity (Book 3.4)."""
        self.__bookings.append(booking)
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "booking", str(booking), booking.get_total_price()))

    def remove_booking(self, booking: 'Booking') -> None:
        """Remove a booking from the student's list after cancellation (Book 3.2)."""
        if booking in self.__bookings:
            self.__bookings.remove(booking)

    def record_late_cancellation(self) -> None:
        """Increment late cancellation count and check ban threshold (Book 3.3).

        Business Rules:
            - Late cancellations contribute to the ban threshold.
            - If (late_cancellations + no_shows) >= BAN_THRESHOLD, student is banned.
        """
        self.__late_cancellation_count += 1
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "late_cancellation", "Late cancellation recorded", 0.0))
        self._check_ban_threshold()

    def record_no_show(self) -> None:
        """Increment no-show count and check ban threshold (Room 9)."""
        self.__no_show_count += 1
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "no_show", "No show recorded", 0.0))
        self._check_ban_threshold()

    def _check_ban_threshold(self) -> None:
        """Ban the student if combined late cancellations and no-shows reach BAN_THRESHOLD."""
        if (self.__late_cancellation_count + self.__no_show_count) >= BAN_THRESHOLD:
            self.__booking_ban_status = True

    def add_deal_package_hours(self, hours: float) -> None:
        """Add pre-paid deal package hours to the student's balance (Checkout 7)."""
        self.__deal_package_hours += hours

    def deduct_deal_package_hours(self, hours: float) -> bool:
        """Deduct deal package hours if sufficient hours remain (Checkout 5).

        Returns:
            True if deduction succeeded, False if insufficient hours.
        """
        if self.__deal_package_hours >= hours:
            self.__deal_package_hours -= hours
            return True
        return False

    def has_used_promo_code(self, code: str) -> bool:
        """Return True if the student has already used this promo code (Checkout 4)."""
        return code in self.__used_promo_codes

    def mark_promo_code_used(self, code: str) -> None:
        """Record that a promo code has been redeemed by this student (Checkout 5)."""
        self.__used_promo_codes.append(code)

    def get_active_bookings(self) -> List['Booking']:
        """Return all bookings with 'confirmed' status (Book 3.11)."""
        return [b for b in self.__bookings if b.get_status() == BOOKING_STATUS_CONFIRMED]

    def get_activity_history_page(self, page: int, page_size: int = 10) -> List['ActivityRecord']:
        """Return a paginated slice of activity history (Acct 9-10).

        Args:
            page: 1-based page number.
            page_size: Number of records per page (default 10).
        """
        start = (page - 1) * page_size
        end = start + page_size
        return self.__activity_history[start:end]

