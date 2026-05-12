"""
MSSRB - Feature 3: Booking Management
Covers: Book 1 ~ Book 15
Contains: <<Entity>> Booking
          <<Controller>> BookingController
          <<Boundary>> BookingUI
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from account import Student
from room import Room


# ================================================================
# <<Entity>> Section
# ================================================================

class Booking:
    """Booking entity class.
    Links a Student to a Room for a specific time period.
    Tracks status (confirmed/cancelled/completed), payment method,
    and promo code usage.
    Referenced by: Book 2-3, 5-6, 11, 14-15, Check 10
    """

    def __init__(self, booking_id: str, student: Student, room: Room,
                 start_time: datetime, end_time: datetime,
                 equipment_rental: bool, total_price: float) -> None:
        self.__booking_id: str = booking_id
        self.__student: Student = student
        self.__room: Room = room
        self.__start_time: datetime = start_time
        self.__end_time: datetime = end_time
        self.__equipment_rental: bool = equipment_rental
        self.__total_price: float = total_price
        self.__status: str = "confirmed"
        self.__payment_method: str = ""
        self.__promo_code_used: Optional[str] = None

    # --- Accessors ---
    def get_booking_id(self) -> str:
        return self.__booking_id

    def get_student(self) -> Student:
        return self.__student

    def get_room(self) -> Room:
        return self.__room

    def get_start_time(self) -> datetime:
        return self.__start_time

    def get_end_time(self) -> datetime:
        return self.__end_time

    def get_equipment_rental(self) -> bool:
        return self.__equipment_rental

    def get_total_price(self) -> float:
        return self.__total_price

    def get_status(self) -> str:
        return self.__status

    def get_payment_method(self) -> str:
        return self.__payment_method

    def get_promo_code_used(self) -> Optional[str]:
        return self.__promo_code_used

    # --- Mutators ---
    def set_status(self, status: str) -> None:
        self.__status = status

    def set_payment_method(self, method: str) -> None:
        self.__payment_method = method

    def set_promo_code_used(self, code: str) -> None:
        self.__promo_code_used = code

    def set_total_price(self, price: float) -> None:
        self.__total_price = price

    # --- Business Methods ---
    def calculate_duration_hours(self) -> float:
        """Book 15: Calculate booking duration in hours."""
        delta = self.__end_time - self.__start_time
        return delta.total_seconds() / 3600

    def is_late_cancellation(self) -> bool:
        """Book 3: Late = cancellation within 30 min of start."""
        remaining = self.__start_time - datetime.now()
        return remaining <= timedelta(minutes=30)

    def cancel(self) -> str:
        """Book 2/3: Cancel and return type.
        'regular_cancellation' if > 30 min before start (full refund).
        'late_cancellation' if <= 30 min (no refund, negative record).
        """
        self.__status = "cancelled"
        if self.is_late_cancellation():
            return "late_cancellation"
        return "regular_cancellation"

    def __str__(self) -> str:
        equip = "Yes" if self.__equipment_rental else "No"
        return (f"[{self.__booking_id}] {self.__room.get_room_name()} | "
                f"{self.__start_time.strftime('%Y-%m-%d %H:%M')} - "
                f"{self.__end_time.strftime('%H:%M')} | "
                f"${self.__total_price:.2f} | Equipment: {equip} | "
                f"Status: {self.__status}")


# ================================================================
# <<Controller>> Section
# ================================================================

class BookingController:
    """Booking management controller.
    Handles: Book 1 (Search), Book 2-3 (Cancel), Book 5 (Create),
             Book 7 (Eligibility), Book 8 (Duration), Book 9 (Select),
             Book 10 (Limit), Book 11 (Review), Book 15 (E2E)
    """

    def __init__(self) -> None:
        self.__rooms: List[Room] = []
        self.__all_bookings: List[Booking] = []
        self.__booking_counter: int = 0

    def get_rooms(self) -> List[Room]:
        return self.__rooms

    def set_rooms(self, rooms: List[Room]) -> None:
        self.__rooms = rooms

    def get_all_bookings(self) -> List[Booking]:
        return self.__all_bookings

    def search_rooms(self, building: str = "",
                     time_slot: str = "") -> List[Room]:
        """Book 1: Search rooms by building and/or time slot.
        Empty filter = show all.
        """
        result = []
        for room in self.__rooms:
            if building and room.get_building().lower() != building.lower():
                continue
            if time_slot and not room.is_available(time_slot):
                continue
            result.append(room)
        return result

    def validate_duration(self, start_time: datetime,
                          end_time: datetime) -> bool:
        """Book 8: Duration >= 1 hour, in 30-min increments."""
        duration = (end_time - start_time).total_seconds() / 3600
        if duration < 1.0:
            return False
        if (duration * 2) != int(duration * 2):
            return False
        return True

    def check_eligibility(self, student: Student) -> Dict[str, bool]:
        """Book 7: Check eligibility (ban status + booking limit)."""
        return {
            "is_eligible": student.is_eligible_to_book(),
            "is_banned": student.get_booking_ban_status(),
            "has_reached_limit": student.has_reached_booking_limit()
        }

    def create_booking(self, student: Student, room: Room,
                       start_time: datetime, end_time: datetime,
                       equipment_rental: bool) -> Optional[Booking]:
        """Book 5/15: Create a new booking after all validations.
        Price = duration_hours × price_per_hour.
        """
        if not student.is_eligible_to_book():
            return None
        if student.has_reached_booking_limit():
            return None
        if not self.validate_duration(start_time, end_time):
            return None
        duration = (end_time - start_time).total_seconds() / 3600
        total_price = duration * room.get_price_per_hour()
        self.__booking_counter += 1
        bid = f"BK{self.__booking_counter:04d}"
        booking = Booking(bid, student, room, start_time, end_time,
                          equipment_rental, total_price)
        self.__all_bookings.append(booking)
        student.add_booking(booking)
        return booking

    def cancel_booking(self, student: Student,
                       booking: Booking) -> Dict[str, object]:
        """Book 2/3: Cancel a booking.
        Regular: full refund. Late: no refund, negative record.
        """
        cancel_type = booking.cancel()
        result = {"type": cancel_type, "refund": 0.0}
        if cancel_type == "regular_cancellation":
            result["refund"] = booking.get_total_price()
            student.add_funds(booking.get_total_price())
        else:
            student.record_late_cancellation()
        student.remove_booking(booking)
        room = booking.get_room()
        st = booking.get_start_time()
        et = booking.get_end_time()
        time_slot = f"{st.strftime('%H:%M')}-{et.strftime('%H:%M')}"
        room.update_availability(time_slot, True)
        return result

    def get_student_bookings(self, student: Student) -> List[Booking]:
        """Book 11/12: Return the student's active bookings."""
        return student.get_active_bookings()

    def find_room_by_id(self, room_id: str) -> Optional[Room]:
        """Helper: Find a room by its ID."""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                return room
        return None

    def find_booking_by_id(self, booking_id: str) -> Optional[Booking]:
        """Helper: Find a booking by its ID."""
        for b in self.__all_bookings:
            if b.get_booking_id() == booking_id:
                return b
        return None


# ================================================================
# <<Boundary>> Section
# ================================================================

class BookingUI:
    """Booking search, creation, and cancellation UI.
    Covers: Book 1-15
    """

    @staticmethod
    def get_search_criteria() -> dict:
        print("\n--- Search Rooms (Book 1) ---")
        building = input("Building (or blank for all): ").strip()
        slot = input("Time slot (HH:MM-HH:MM, or blank): ").strip()
        return {"building": building, "time_slot": slot}

    @staticmethod
    def show_room_list(rooms: list):
        print(f"\n--- Available Rooms ({len(rooms)} found) ---")
        if not rooms:
            print("  No rooms found matching your criteria.")
            return
        for i, r in enumerate(rooms, 1):
            print(f"  {i}. {r}")

    @staticmethod
    def select_room(max_idx: int) -> int:
        print(f"\n(Book 9) Select a room [1-{max_idx}] or 0 to cancel:")
        try:
            return int(input("Select: ").strip())
        except ValueError:
            return 0

    @staticmethod
    def get_booking_time() -> tuple:
        print("\n--- Booking Time (Book 5/8) ---")
        date_str = input("Date (YYYY-MM-DD): ").strip()
        start = input("Start time (HH:MM): ").strip()
        end = input("End time (HH:MM): ").strip()
        return date_str, start, end

    @staticmethod
    def ask_equipment() -> bool:
        print("\n(Book 4) Borrow equipment bundle? (y/n):")
        return input("Select: ").strip().lower() == "y"

    @staticmethod
    def show_booking_summary(booking):
        print("\n--- Booking Created (Book 15) ---")
        print(f"  {booking}")

    @staticmethod
    def show_student_bookings(bookings: list):
        print(f"\n--- Your Bookings ({len(bookings)}) (Book 11/13) ---")
        if not bookings:
            print("  No active bookings.")
            return
        for i, b in enumerate(bookings, 1):
            print(f"  {i}. {b}")

    @staticmethod
    def select_booking_to_cancel(max_idx: int) -> int:
        print(f"\n(Book 6) Select booking to cancel [1-{max_idx}], 0 to go back:")
        try:
            return int(input("Select: ").strip())
        except ValueError:
            return 0

    @staticmethod
    def confirm_cancellation() -> bool:
        print("\n(Book 14) Confirm cancellation? (y/n):")
        return input("Select: ").strip().lower() == "y"

    @staticmethod
    def show_cancellation_result(result: dict):
        ctype = result["type"].replace("_", " ").title()
        print(f"\n--- Cancellation Result (Book 2/3) ---")
        print(f"  Type   : {ctype}")
        print(f"  Refund : ${result['refund']:.2f}")

    @staticmethod
    def show_eligibility(elig: dict):
        print("\n--- Booking Eligibility (Book 7) ---")
        if elig["is_banned"]:
            print("  [!] You are BANNED from booking. (Book 12)")
        elif elig["has_reached_limit"]:
            print("  [!] You have reached the maximum 3 bookings. (Book 10)")
        else:
            print("  [OK] You are eligible to book.")
