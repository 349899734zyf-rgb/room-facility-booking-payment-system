from datetime import datetime
from typing import Dict, List, Optional

from entities.booking import Booking
from entity_classes import Room, Student


class BookingController:
    """Controller class for Booking Management user stories 3.1 to 3.15."""

    def __init__(self) -> None:
        self.__rooms: List[Room] = []
        self.__all_bookings: List[Booking] = []
        self.__booking_counter = 0
        self.__equipment_deposit = 50.0

    # Basic accessors
    def get_rooms(self) -> List[Room]:
        return self.__rooms

    def get_all_bookings(self) -> List[Booking]:
        return self.__all_bookings

    def add_room(self, room: Room) -> None:
        """Add a room into the booking controller's searchable room list."""
        self.__rooms.append(room)

    def get_equipment_deposit(self) -> float:
        return self.__equipment_deposit

    def set_equipment_deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.__equipment_deposit = amount
        return True

    # Time and search helpers
    def parse_time(self, time_text: str) -> Optional[datetime]:
        """Convert user input text into a datetime object."""
        try:
            return datetime.strptime(time_text, "%Y-%m-%d %H:%M")
        except ValueError:
            return None

    def format_time(self, time_value: datetime) -> str:
        """Keep the same time format used by Room.available_time_slots."""
        return time_value.strftime("%Y-%m-%d %H:%M")

    def validate_search_criteria(self, building: str, start_time: str, end_time: str) -> Dict[str, object]:
        """Validate building code and time input before searching rooms."""
        start_dt = self.parse_time(start_time)
        end_dt = self.parse_time(end_time)

        if not building.strip() or start_dt is None or end_dt is None or end_dt <= start_dt:
            return {"valid": False, "start_time": None, "end_time": None}

        return {"valid": True, "start_time": start_dt, "end_time": end_dt}

    def search_rooms(self, building: str, start_time: str, end_time: str) -> Dict[str, object]:
        """Book 3.1: search available rooms by building and time period."""
        criteria = self.validate_search_criteria(building, start_time, end_time)
        if not criteria["valid"]:
            return {"success": False, "reason": "invalid_input", "rooms": []}

        available_rooms = []
        for room in self.__rooms:
            same_building = room.get_building().upper() == building.upper()
            if same_building and room.is_available(start_time, end_time):
                available_rooms.append(room)

        if not available_rooms:
            return {"success": False, "reason": "no_rooms", "rooms": []}

        return {"success": True, "reason": "rooms_found", "rooms": available_rooms}

    def validate_duration(self, start_time: datetime, end_time: datetime) -> bool:
        """Book 3.8: booking duration must be at least 1 hour and in 30-minute blocks."""
        duration_minutes = int((end_time - start_time).total_seconds() / 60)
        return duration_minutes >= 60 and duration_minutes % 30 == 0

    # Eligibility and selection
    def check_eligibility(self, student: Student) -> Dict[str, object]:
        """Book 3.7 and 3.10: check ban status and active booking limit."""
        is_banned = student.get_booking_ban_status()
        has_reached_limit = student.has_reached_booking_limit()

        return {
            "is_banned": is_banned,
            "has_reached_limit": has_reached_limit,
            "can_make_booking": not is_banned and not has_reached_limit,
            "active_bookings": student.get_active_bookings(),
        }

    def select_room(self, available_rooms: List[Room], room_id: str) -> Optional[Room]:
        """Book 3.9: select a room only from the displayed available room list."""
        for room in available_rooms:
            if room.get_room_id() == room_id:
                return room
        return None

    # Price and booking creation
    def calculate_booking_price(self, room: Room, start_time: datetime, end_time: datetime) -> float:
        duration_hours = (end_time - start_time).total_seconds() / 3600
        return duration_hours * room.get_price_per_hour()

    def calculate_total_required(self, room: Room, start_time: datetime, end_time: datetime,
                                 equipment_rental: bool) -> float:
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
        payment_method: str = "balance",
    ) -> Dict[str, object]:
        """Book 3.4, 3.5 and 3.15: create a booking after all rules are satisfied."""
        eligibility = self.check_eligibility(student)
        if eligibility["is_banned"]:
            return {"success": False, "reason": "banned"}
        if eligibility["has_reached_limit"]:
            return {"success": False, "reason": "booking_limit_reached"}
        if not self.validate_duration(start_time, end_time):
            return {"success": False, "reason": "invalid_duration"}

        start_text = self.format_time(start_time)
        end_text = self.format_time(end_time)
        if not room.is_available(start_text, end_text):
            return {"success": False, "reason": "room_unavailable"}

        room_price = self.calculate_booking_price(room, start_time, end_time)
        deposit = self.__equipment_deposit if equipment_rental else 0.0
        total_required = room_price + deposit

        if payment_method == "balance":
            if student.get_balance() < total_required:
                return {"success": False, "reason": "insufficient_balance"}
            student.deduct_balance(total_required)
        elif payment_method == "deal_package":
            if equipment_rental:
                return {"success": False, "reason": "deal_package_equipment_restricted"}

            duration_hours = (end_time - start_time).total_seconds() / 3600
            if student.get_deal_package_hours() < duration_hours:
                return {"success": False, "reason": "insufficient_deal_hours"}
            student.deduct_deal_package_hours(duration_hours)
        else:
            return {"success": False, "reason": "invalid_payment_method"}

        self.__booking_counter += 1
        booking_id = f"BK{self.__booking_counter:04d}"
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

        return {"success": True, "reason": "booking_created", "booking": booking}

    # Existing bookings and cancellation
    def get_student_bookings(self, student: Student) -> List[Booking]:
        """Book 3.11, 3.12 and 3.13: return active bookings for display."""
        return student.get_active_bookings()

    def find_student_booking(self, student: Student, booking_id: str) -> Optional[Booking]:
        for booking in student.get_active_bookings():
            if booking.get_booking_id() == booking_id:
                return booking
        return None

    def review_booking_before_cancel(self, student: Student, booking_id: str) -> Dict[str, object]:
        """Book 3.11: show selected booking details before cancellation."""
        if not booking_id.strip():
            return {"success": False, "reason": "invalid_input"}

        booking = self.find_student_booking(student, booking_id)
        if booking is None:
            return {"success": False, "reason": "booking_not_found"}

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
        booking_id: str,
        confirm_cancel: bool,
        current_time: Optional[datetime] = None,
    ) -> Dict[str, object]:
        """Book 3.2, 3.3, 3.6 and 3.14: cancel or stop a cancellation request."""
        booking = self.find_student_booking(student, booking_id)
        if booking is None:
            return {"success": False, "reason": "booking_not_found"}

        if not confirm_cancel:
            return {"success": True, "reason": "cancellation_stopped", "booking": booking, "refund": 0.0}

        cancel_type = booking.cancel(current_time)
        start_text = self.format_time(booking.get_start_time())
        end_text = self.format_time(booking.get_end_time())
        booking.get_room().update_availability(f"{start_text}-{end_text}", True)

        refund = 0.0
        if cancel_type == "regular_cancellation":
            refund = booking.get_total_price() + booking.get_equipment_deposit()
            student.add_funds(refund)
        else:
            student.record_late_cancellation()

        student.remove_booking(booking)

        return {
            "success": True,
            "reason": cancel_type,
            "booking": booking,
            "refund": refund,
            "ban_applied": student.get_booking_ban_status(),
        }

    def get_booking_system_status(self, student: Student) -> Dict[str, object]:
        """Book 3.7 and 3.12: provide booking status when entering the booking system."""
        eligibility = self.check_eligibility(student)
        available_slot_count = sum(len(room.get_available_time_slots()) for room in self.__rooms)

        return {
            "can_make_booking": eligibility["can_make_booking"],
            "is_banned": eligibility["is_banned"],
            "has_reached_limit": eligibility["has_reached_limit"],
            "available_slot_count": available_slot_count,
            "current_bookings": student.get_active_bookings(),
        }
