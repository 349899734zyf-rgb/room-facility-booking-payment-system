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
    """Entity class for Booking Management user stories 3.2, 3.3, 3.5, 3.6 and 3.15."""

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

    def get_booking_id(self) -> str:
        return self.__booking_id

    def get_student(self) -> object:
        return self.__student

    def get_room(self) -> object:
        return self.__room

    def get_start_time(self) -> datetime:
        return self.__start_time

    def get_end_time(self) -> datetime:
        return self.__end_time

    def get_equipment_rental(self) -> bool:
        return self.__equipment_rental

    def get_total_price(self) -> float:
        return self.__total_price

    def get_equipment_deposit(self) -> float:
        return self.__equipment_deposit

    def get_status(self) -> str:
        return self.__status

    def get_payment_method(self) -> Optional[str]:
        return self.__payment_method

    def set_status(self, status: str) -> None:
        self.__status = status

    def set_payment_method(self, payment_method: str) -> None:
        self.__payment_method = payment_method

    def set_total_price(self, total_price: float) -> None:
        self.__total_price = total_price

    def calculate_duration_hours(self) -> float:
        duration = self.__end_time - self.__start_time
        return duration.total_seconds() / SECONDS_PER_HOUR

    def is_late_cancellation(self, current_time: Optional[datetime] = None) -> bool:
        check_time = current_time or datetime.now()
        time_before_start = self.__start_time - check_time
        return timedelta(0) <= time_before_start <= timedelta(minutes=LATE_CANCELLATION_MINUTES)

    def cancel(self, current_time: Optional[datetime] = None) -> str:
        self.__status = BOOKING_STATUS_CANCELLED
        if self.is_late_cancellation(current_time):
            return CANCELLATION_LATE
        return CANCELLATION_REGULAR

    def __str__(self) -> str:
        room_id = self.__room.get_room_id() if hasattr(self.__room, "get_room_id") else "unknown room"
        return (
            f"{self.__booking_id} | {room_id} | "
            f"{self.__start_time:{DISPLAY_TIME_FORMAT}} - {self.__end_time:{DISPLAY_TIME_FORMAT}} | "
            f"{self.__status}"
        )


