"""
This file defines the Booking entity class used to store booking details,
calculate booking duration, and determine cancellation type.
"""

from datetime import datetime, timedelta
from typing import Optional

from booking_constants import (
    BOOKING_STATUS_CANCELLED,
    BOOKING_STATUS_CONFIRMED,
    CANCELLATION_LATE,
    CANCELLATION_REGULAR,
    DISPLAY_TIME_FORMAT,
    LATE_CANCELLATION_MINUTES,
    SECONDS_PER_HOUR,
)


class Booking:
    """Entity class for Booking Management user stories."""

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
        """Create a booking record with room, time, price, and status."""
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

    def get_payment_method(self) -> Optional[str]:
        """Return the payment method used for this booking."""
        return self.__payment_method

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
        """Calculate the booking duration in hours."""
        duration = self.__end_time - self.__start_time
        return duration.total_seconds() / SECONDS_PER_HOUR

    def is_late_cancellation(
        self,
        current_time: Optional[datetime] = None,
    ) -> bool:
        """Return True when cancellation happens in the late window."""
        check_time = current_time or datetime.now()
        time_before_start = self.__start_time - check_time
        late_window = timedelta(minutes=LATE_CANCELLATION_MINUTES)
        return timedelta(0) <= time_before_start <= late_window

    def cancel(self, current_time: Optional[datetime] = None) -> str:
        """Cancel the booking and return the cancellation type."""
        self.__status = BOOKING_STATUS_CANCELLED
        if self.is_late_cancellation(current_time):
            return CANCELLATION_LATE
        return CANCELLATION_REGULAR

    def __str__(self) -> str:
        """Return a readable summary of the booking."""
        if hasattr(self.__room, "get_room_id"):
            room_id = self.__room.get_room_id()
        else:
            room_id = "unknown room"

        start_text = self.__start_time.strftime(DISPLAY_TIME_FORMAT)
        end_text = self.__end_time.strftime(DISPLAY_TIME_FORMAT)
        return (
            f"{self.__booking_id} | {room_id} | "
            f"{start_text} - {end_text} | {self.__status}"
        )

