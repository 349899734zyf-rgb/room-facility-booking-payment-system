"""
Module: booking.py
Layer: Entity
User Stories: Book 3.1-3.15

Represents a single room booking with its time period, pricing,
equipment rental, and cancellation logic (regular vs late).
"""

from datetime import datetime, timedelta
from typing import Optional

from booking_constants import (
    BOOKING_STATUS_CANCELLED,
    BOOKING_STATUS_CONFIRMED,
    CANCELLATION_LATE,
    CANCELLATION_REGULAR,
    DISPLAY_TIME_FORMAT,
    LARGE_LATE_CANCEL_WINDOW_HOURS,
    LATE_CANCELLATION_MINUTES,
    MEDIUM_LATE_CANCEL_WINDOW_HOURS,
    ROOM_TYPE_LARGE,
    ROOM_TYPE_MEDIUM,
    ROOM_TYPE_SMALL,
    SECONDS_PER_HOUR,
    SMALL_LATE_CANCEL_WINDOW_MINUTES,
)


class Booking:
    """Entity for a room booking.

    Responsibilities:
        - Store booking details: student, room, time, price, status (Book 3.4-3.5)
        - Calculate booking duration in hours (Book 3.8)
        - Determine late cancellation based on room-type-specific time windows (Book 3.3)
        - Execute cancellation and return cancellation type (Book 3.2, 3.6)

    Business Rules:
        - Late cancellation window varies by room type:
          Small = 30 min, Medium = 3 hours, Large = 4 hours.
        - Status transitions: 'confirmed' -> 'cancelled'.

    Collaborators:
        - Student: the booking owner
        - Room: the booked room (provides room_type for cancellation rules)
    """

    def __init__(
        self,
        booking_id: str,
        student: object,
        room: object,
        start_time: datetime,
        end_time: datetime,
        equipment_rental: bool,
        total_price: float,
        equipment_deposit: float = 0.0,
    ) -> None:
        """Create a booking record.

        Args:
            booking_id: Unique booking identifier (e.g. 'BK0001').
            student: The Student entity who owns this booking.
            room: The Room entity being booked.
            start_time: Booking start datetime.
            end_time: Booking end datetime.
            equipment_rental: Whether equipment is rented with this booking.
            total_price: Room booking price (excl. deposit).
            equipment_deposit: Refundable equipment deposit amount.
        """
        self.__booking_id = booking_id
        self.__student = student
        self.__room = room
        self.__start_time = start_time
        self.__end_time = end_time
        self.__equipment_rental = equipment_rental
        self.__total_price = total_price
        self.__equipment_deposit = equipment_deposit
        self.__status = BOOKING_STATUS_CONFIRMED
        self.__payment_method: Optional[str] = None
        self.__promo_code_used: Optional[str] = None

    def get_booking_id(self) -> str:
        """Return the unique booking ID."""
        return self.__booking_id

    def get_student(self) -> object:
        """Return the student who owns this booking."""
        return self.__student

    def get_room(self) -> object:
        """Return the booked room."""
        return self.__room

    def get_start_time(self) -> datetime:
        """Return the booking start time."""
        return self.__start_time

    def get_end_time(self) -> datetime:
        """Return the booking end time."""
        return self.__end_time

    def get_equipment_rental(self) -> bool:
        """Return whether equipment is included in this booking."""
        return self.__equipment_rental

    def get_total_price(self) -> float:
        """Return the room booking price excluding refundable deposit."""
        return self.__total_price

    def get_equipment_deposit(self) -> float:
        """Return the equipment deposit attached to this booking."""
        return self.__equipment_deposit

    def get_status(self) -> str:
        """Return the current booking status."""
        return self.__status

    def get_payment_method(self) -> str:
        """Return the payment method used for this booking."""
        return self.__payment_method or ""

    def get_promo_code_used(self) -> Optional[str]:
        """Return the promo code used for this booking."""
        return self.__promo_code_used

    def set_status(self, status: str) -> None:
        """Update the current booking status."""
        self.__status = status

    def set_payment_method(self, payment_method: str) -> None:
        """Store the payment method used for this booking."""
        self.__payment_method = payment_method

    def set_promo_code_used(self, code: str) -> None:
        """Record which promo code was applied to this booking."""
        self.__promo_code_used = code

    def set_total_price(self, total_price: float) -> None:
        """Update the room booking price."""
        self.__total_price = total_price

    def calculate_duration_hours(self) -> float:
        """Calculate and return the booking duration in hours (Book 3.8)."""
        duration = self.__end_time - self.__start_time
        return duration.total_seconds() / SECONDS_PER_HOUR

    def is_late_cancellation(
        self,
        current_time: Optional[datetime] = None,
    ) -> bool:
        """Return True when cancellation happens in the late window."""
        check_time = current_time or datetime.now()
        time_before_start = self.__start_time - check_time
        
        room_type = ROOM_TYPE_SMALL
        if hasattr(self.__room, "get_room_type"):
            room_type = self.__room.get_room_type()
            
        if room_type == ROOM_TYPE_MEDIUM:
            late_window = timedelta(hours=MEDIUM_LATE_CANCEL_WINDOW_HOURS)
        elif room_type == ROOM_TYPE_LARGE:
            late_window = timedelta(hours=LARGE_LATE_CANCEL_WINDOW_HOURS)
        else:
            late_window = timedelta(minutes=SMALL_LATE_CANCEL_WINDOW_MINUTES)
            
        return timedelta(0) <= time_before_start <= late_window

    def cancel(self, current_time: Optional[datetime] = None) -> str:
        """Cancel the booking and return the cancellation type."""
        self.__status = BOOKING_STATUS_CANCELLED
        if self.is_late_cancellation(current_time):
            return CANCELLATION_LATE
        return CANCELLATION_REGULAR

    def __str__(self) -> str:
        """Return a readable summary of the booking."""
        room_desc = "unknown room"
        if self.__room:
            if hasattr(self.__room, "get_room_name") and hasattr(self.__room, "get_room_id"):
                room_desc = f"{self.__room.get_room_id()} ({self.__room.get_room_name()})"
            elif hasattr(self.__room, "get_room_id"):
                room_desc = self.__room.get_room_id()

        start_text = self.__start_time.strftime(DISPLAY_TIME_FORMAT)
        end_text = self.__end_time.strftime(DISPLAY_TIME_FORMAT)
        return (
            f"{self.__booking_id} | {room_desc} | "
            f"{start_text} - {end_text} | {self.__status}"
        )

