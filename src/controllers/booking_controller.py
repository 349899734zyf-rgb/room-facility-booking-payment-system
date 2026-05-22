"""
This file defines the BookingController class, which manages booking search,
eligibility checks, booking creation, and booking cancellation workflows.
"""

from datetime import datetime
from typing import Dict, List, Optional

from booking_constants import (
    BOOKING_ID_DIGITS,
    BOOKING_ID_PREFIX,
    BOOKING_INCREMENT_MINUTES,
    CANCELLATION_REGULAR,
    CANCELLATION_STOPPED,
    DEFAULT_EQUIPMENT_DEPOSIT,
    MINIMUM_BOOKING_MINUTES,
    PAYMENT_METHOD_BALANCE,
    PAYMENT_METHOD_DEAL_PACKAGE,
    REASON_BANNED,
    REASON_BOOKING_CREATED,
    REASON_BOOKING_LIMIT_REACHED,
    REASON_BOOKING_NOT_FOUND,
    REASON_DEAL_PACKAGE_EQUIPMENT_RESTRICTED,
    REASON_INSUFFICIENT_BALANCE,
    REASON_INSUFFICIENT_DEAL_HOURS,
    REASON_INVALID_DURATION,
    REASON_INVALID_INPUT,
    REASON_INVALID_PAYMENT_METHOD,
    REASON_NO_ROOMS,
    REASON_ROOM_UNAVAILABLE,
    REASON_ROOMS_FOUND,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE,
    TIME_FORMAT,
)
from entities.booking import Booking
from entities.student import Student
from entities.room import Room


class BookingController:
    """Controller class for Booking Management user stories 3.1 to 3.15."""

    def __init__(self) -> None:
        """Create an empty booking controller with default settings."""
        self.__rooms: List[Room] = []
        self.__all_bookings: List[Booking] = []
        self.__booking_counter = 0
        self.__equipment_deposit = DEFAULT_EQUIPMENT_DEPOSIT

    def get_rooms(self) -> List[Room]:
        """Return rooms managed by this controller."""
        return self.__rooms

    def get_all_bookings(self) -> List[Booking]:
        """Return all bookings created through this controller."""
        return self.__all_bookings

    def add_room(self, room: Room) -> None:
        """Add a room into the booking controller's searchable room list."""
        self.__rooms.append(room)

    def get_equipment_deposit(self) -> float:
        """Return the current equipment deposit amount."""
        return self.__equipment_deposit

    def set_equipment_deposit(self, amount: float) -> bool:
        """Update the equipment deposit when the amount is valid."""
        if amount <= 0:
            return False
        self.__equipment_deposit = amount
        return True

    def parse_time(self, time_text: str) -> Optional[datetime]:
        """Convert user input text into a datetime object."""
        try:
            return datetime.strptime(time_text, TIME_FORMAT)
        except ValueError:
            return None

    def format_time(self, time_value: datetime) -> str:
        """Keep the same time format used by Room.available_time_slots."""
        return time_value.strftime(TIME_FORMAT)

    def validate_search_criteria(
        self,
        building: str,
        start_time: str,
        end_time: str,
        capacity: int = 1,
    ) -> Dict[str, object]:
        """Validate building code, time input, and capacity before searching rooms."""
        start_dt = self.parse_time(start_time)
        end_dt = self.parse_time(end_time)
        invalid_time_range = (
            start_dt is None
            or end_dt is None
            or end_dt <= start_dt
        )

        if not building.strip() or invalid_time_range or capacity <= 0:
            return {"valid": False, "start_time": None, "end_time": None}

        return {"valid": True, "start_time": start_dt, "end_time": end_dt}

    def search_rooms(
        self,
        building: str,
        start_time: str,
        end_time: str,
        capacity: int = 1,
    ) -> Dict[str, object]:
        """Book 3.1: search rooms by building, time period, and capacity."""
        criteria = self.validate_search_criteria(
            building,
            start_time,
            end_time,
            capacity,
        )
        if not criteria["valid"]:
            return {
                "success": False,
                "reason": REASON_INVALID_INPUT,
                "rooms": [],
            }

        available_rooms = []
        for room in self.__rooms:
            same_building = room.get_building().upper() == building.upper()
            meets_capacity = room.get_capacity() >= capacity
            if same_building and meets_capacity and room.is_available(start_time, end_time):
                available_rooms.append(room)

        if not available_rooms:
            return {"success": False, "reason": REASON_NO_ROOMS, "rooms": []}

        return {
            "success": True,
            "reason": REASON_ROOMS_FOUND,
            "rooms": available_rooms,
        }

    def validate_duration(
        self,
        start_time: datetime,
        end_time: datetime,
        room_type: str = "Small",
    ) -> bool:
        """Book 3.8: check minimum duration and 30-minute blocks."""
        duration_minutes = int(
            (end_time - start_time).total_seconds() / SECONDS_PER_MINUTE,
        )
        min_minutes = 120 if room_type in ["Medium", "Large"] else MINIMUM_BOOKING_MINUTES
        long_enough = duration_minutes >= min_minutes
        follows_increment = duration_minutes % BOOKING_INCREMENT_MINUTES == 0
        return long_enough and follows_increment

    def check_eligibility(self, student: Student) -> Dict[str, object]:
        """Book 3.7 and 3.10: check ban status and booking limit."""
        is_banned = student.get_booking_ban_status()
        has_reached_limit = student.has_reached_booking_limit()

        return {
            "is_banned": is_banned,
            "has_reached_limit": has_reached_limit,
            "can_make_booking": not is_banned and not has_reached_limit,
            "active_bookings": student.get_active_bookings(),
        }

    def select_room(
        self,
        available_rooms: List[Room],
        room_id: str,
    ) -> Optional[Room]:
        """Book 3.9: select a room from the displayed room list."""
        for room in available_rooms:
            if room.get_room_id() == room_id:
                return room
        return None

    def calculate_booking_price(
        self,
        room: Room,
        start_time: datetime,
        end_time: datetime,
    ) -> float:
        """Calculate the room price for the selected booking duration."""
        duration_hours = (
            (end_time - start_time).total_seconds() / SECONDS_PER_HOUR
        )
        return duration_hours * room.get_price_per_hour()

    def calculate_total_required(
        self,
        room: Room,
        start_time: datetime,
        end_time: datetime,
        equipment_rental: bool,
    ) -> float:
        """Calculate total required payment including equipment deposit."""
        room_price = self.calculate_booking_price(room, start_time, end_time)
        if equipment_rental:
            return room_price + self.__equipment_deposit
        return room_price

    def create_booking(
        self,
        student: Student,
        room: Room,
        start_time: datetime,
        end_time: datetime,
        equipment_rental: bool,
        payment_method: str = PAYMENT_METHOD_BALANCE,
        current_time: Optional[datetime] = None,
    ) -> Dict[str, object]:
        """Book 3.4, 3.5 and 3.15: create a valid booking."""
        eligibility = self.check_eligibility(student)
        if eligibility["is_banned"]:
            return {"success": False, "reason": REASON_BANNED}
        if eligibility["has_reached_limit"]:
            return {"success": False, "reason": REASON_BOOKING_LIMIT_REACHED}
            
        room_type = room.get_room_type() if hasattr(room, "get_room_type") else "Small"
        if not self.validate_duration(start_time, end_time, room_type):
            return {"success": False, "reason": REASON_INVALID_DURATION}

        # Enforce advance booking rules
        booking_time = current_time or datetime.now()
        time_diff = start_time - booking_time
        from datetime import timedelta
        if room_type == "Medium" and time_diff < timedelta(hours=3):
            return {"success": False, "reason": "advance_booking_requirement_not_met"}
        elif room_type == "Large" and time_diff < timedelta(hours=24):
            return {"success": False, "reason": "advance_booking_requirement_not_met"}

        start_text = self.format_time(start_time)
        end_text = self.format_time(end_time)
        if not room.is_available(start_text, end_text):
            return {"success": False, "reason": REASON_ROOM_UNAVAILABLE}

        room_price = self.calculate_booking_price(room, start_time, end_time)
        deposit = self.__equipment_deposit if equipment_rental else 0.0
        total_required = room_price + deposit

        if payment_method == PAYMENT_METHOD_BALANCE:
            if student.get_balance() < total_required:
                return {
                    "success": False,
                    "reason": REASON_INSUFFICIENT_BALANCE,
                }
            student.deduct_balance(total_required)
        elif payment_method == PAYMENT_METHOD_DEAL_PACKAGE:
            if room_type != "Small":
                return {
                    "success": False,
                    "reason": "deal_package_room_type_restricted",
                }
            if equipment_rental:
                return {
                    "success": False,
                    "reason": REASON_DEAL_PACKAGE_EQUIPMENT_RESTRICTED,
                }

            duration_hours = (
                (end_time - start_time).total_seconds() / SECONDS_PER_HOUR
            )
            if student.get_deal_package_hours() < duration_hours:
                return {
                    "success": False,
                    "reason": REASON_INSUFFICIENT_DEAL_HOURS,
                }
            student.deduct_deal_package_hours(duration_hours)
        else:
            return {"success": False, "reason": REASON_INVALID_PAYMENT_METHOD}

        self.__booking_counter += 1
        booking_id = (
            f"{BOOKING_ID_PREFIX}"
            f"{self.__booking_counter:0{BOOKING_ID_DIGITS}d}"
        )
        booking = Booking(
            booking_id,
            student,
            room,
            start_time,
            end_time,
            equipment_rental,
            room_price,
            deposit,
        )
        booking.set_payment_method(payment_method)

        self.__all_bookings.append(booking)
        student.add_booking(booking)
        room.update_availability(f"{start_text}-{end_text}", False)

        return {
            "success": True,
            "reason": REASON_BOOKING_CREATED,
            "booking": booking,
        }

    def get_student_bookings(self, student: Student) -> List[Booking]:
        """Book 3.11, 3.12 and 3.13: return active bookings."""
        return student.get_active_bookings()

    def find_student_booking(
        self,
        student: Student,
        booking_id: str,
    ) -> Optional[Booking]:
        """Find one active booking owned by the student."""
        for booking in student.get_active_bookings():
            if booking.get_booking_id() == booking_id:
                return booking
        return None

    def review_booking_before_cancel(
        self,
        student: Student,
        booking_id: str,
    ) -> Dict[str, object]:
        """Book 3.11: show booking details before cancellation."""
        if not booking_id.strip():
            return {"success": False, "reason": REASON_INVALID_INPUT}

        booking = self.find_student_booking(student, booking_id)
        if booking is None:
            return {"success": False, "reason": REASON_BOOKING_NOT_FOUND}

        current_time = datetime.now()
        return {
            "success": True,
            "booking": booking,
            "current_time": current_time,
            "is_late_cancellation": booking.is_late_cancellation(current_time),
        }

    def cancel_booking(
        self,
        student: Student,
        booking_or_id: object,
        confirm_cancel: bool = True,
        current_time: Optional[datetime] = None,
    ) -> Dict[str, object]:
        """Book 3.2, 3.3, 3.6 and 3.14: handle cancellation."""
        if hasattr(booking_or_id, "get_booking_id"):
            booking_id = booking_or_id.get_booking_id()
        else:
            booking_id = str(booking_or_id)

        booking = self.find_student_booking(student, booking_id)
        if booking is None:
            # Fallback: search all student bookings (not just active ones)
            for b in student.get_bookings():
                if b.get_booking_id() == booking_id:
                    booking = b
                    break
        if booking is None:
            return {"success": False, "reason": REASON_BOOKING_NOT_FOUND}

        if not confirm_cancel:
            return {
                "success": True,
                "reason": CANCELLATION_STOPPED,
                "type": CANCELLATION_STOPPED,
                "booking": booking,
                "refund": 0.0,
            }

        cancel_type = booking.cancel(current_time)
        start_text = self.format_time(booking.get_start_time())
        end_text = self.format_time(booking.get_end_time())
        booking.get_room().update_availability(
            f"{start_text}-{end_text}",
            True,
        )

        refund = 0.0
        if cancel_type == CANCELLATION_REGULAR:
            refund = (
                booking.get_total_price()
                + booking.get_equipment_deposit()
            )
            student.add_funds(refund)
        else:
            room_type = "Small"
            room = booking.get_room()
            if room and hasattr(room, "get_room_type"):
                room_type = room.get_room_type()
                
            deposit_refund = booking.get_equipment_deposit()
            
            if room_type == "Small":
                room_refund = booking.get_total_price() * 0.5
            elif room_type == "Medium":
                room_refund = booking.get_total_price() * 0.5
            elif room_type == "Large":
                room_refund = booking.get_total_price() * 0.3
            else:
                room_refund = 0.0
                
            refund = room_refund + deposit_refund
            if refund > 0:
                student.add_funds(refund)
            student.record_late_cancellation()

        student.remove_booking(booking)

        return {
            "success": True,
            "reason": cancel_type,
            "type": cancel_type,
            "booking": booking,
            "refund": refund,
            "ban_applied": student.get_booking_ban_status(),
        }

    def get_booking_system_status(self, student: Student) -> Dict[str, object]:
        """Book 3.7 and 3.12: return booking system status."""
        eligibility = self.check_eligibility(student)
        available_slot_count = sum(
            len(room.get_available_time_slots()) for room in self.__rooms
        )

        return {
            "can_make_booking": eligibility["can_make_booking"],
            "is_banned": eligibility["is_banned"],
            "has_reached_limit": eligibility["has_reached_limit"],
            "available_slot_count": available_slot_count,
            "current_bookings": student.get_active_bookings(),
        }

    # Helper/White-box methods:
    def set_rooms(self, rooms: List[Room]) -> None:
        self.__rooms = rooms

    def find_room_by_id(self, room_id: str) -> Optional[Room]:
        for r in self.__rooms:
            if r.get_room_id() == room_id:
                return r
        return None

    def find_booking_by_id(self, booking_id: str) -> Optional[Booking]:
        for b in self.__all_bookings:
            if b.get_booking_id() == booking_id:
                return b
        return None

