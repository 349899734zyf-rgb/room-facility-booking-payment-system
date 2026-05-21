"""
This file defines the BookingUI class, which handles text-based input and
output for room search, room selection, equipment selection, and booking
display.
"""

from typing import Dict, List

from booking_constants import (
    END_TIME_DISPLAY_FORMAT,
    REASON_BANNED,
    REASON_BOOKING_LIMIT_REACHED,
    REASON_DEAL_PACKAGE_EQUIPMENT_RESTRICTED,
    REASON_INSUFFICIENT_BALANCE,
    REASON_INSUFFICIENT_DEAL_HOURS,
    REASON_INVALID_DURATION,
    REASON_INVALID_PAYMENT_METHOD,
    REASON_ROOM_UNAVAILABLE,
)


class BookingUI:
    """Boundary class for booking search, selection, and display."""

    def display_booking_options(self) -> None:
        """Show the main booking menu."""
        print("\n--- Booking Menu ---")
        print("1. Search available rooms")
        print("2. View current bookings")
        print("3. Cancel a booking")
        print("4. Return")

    def get_search_criteria(self) -> Dict[str, str]:
        """Get building and time period from the student."""
        building = input("Enter building code (or enter 'CANCEL' to return): ").strip()
        if building.upper() == "CANCEL":
            return {"building": "CANCEL", "start_time": "", "end_time": ""}
        start_time = input("Enter start time (YYYY-MM-DD HH:MM, or enter 'CANCEL' to return): ").strip()
        if start_time.upper() == "CANCEL":
            return {"building": "CANCEL", "start_time": "", "end_time": ""}
        end_time = input("Enter end time (YYYY-MM-DD HH:MM, or enter 'CANCEL' to return): ").strip()
        if end_time.upper() == "CANCEL":
            return {"building": "CANCEL", "start_time": "", "end_time": ""}
        return {
            "building": building,
            "start_time": start_time,
            "end_time": end_time,
        }

    def display_available_rooms(self, rooms: List[object]) -> None:
        """Display all rooms found by the search."""
        print("\nAvailable rooms:")
        for room in rooms:
            print(
                f"{room.get_room_id()} | {room.get_room_name()} | "
                f"Building: {room.get_building()} | "
                f"Capacity: {room.get_capacity()} | "
                f"${room.get_price_per_hour():.2f}/hour"
            )

    def display_no_rooms_message(self) -> None:
        """Show a message when no rooms match the search."""
        print("No rooms are available during the selected time period.")

    def display_invalid_input_message(self) -> None:
        """Show a message when the search input is invalid."""
        print("Invalid input. Please check the building code and time format.")

    def get_room_selection(self) -> str:
        """Get the room ID selected by the student."""
        return input("Enter the room ID you want to book (or enter 'CANCEL' to return): ").strip()

    def display_room_selection_error(self) -> None:
        """Show a message when the selected room is invalid."""
        print("The selected room is not in the available room list.")

    def display_equipment_options(self) -> None:
        """Show optional equipment choices."""
        print("\nEquipment bundle:")
        print("1. Borrow equipment")
        print("2. Do not borrow equipment")

    def get_equipment_choice(self) -> bool:
        """Return True if the student chooses to borrow equipment."""
        choice = input("Choose 1 or 2 (or enter 'CANCEL' to return): ").strip()
        if choice.upper() == "CANCEL":
            raise ValueError("CANCEL")
        if choice == "1":
            return True
        if choice == "2":
            return False
        raise ValueError("Invalid equipment choice.")

    def display_deposit_requirement(self, amount: float) -> None:
        """Show the equipment deposit amount."""
        print(f"Equipment deposit required: ${amount:.2f}")

    def display_booking_limit_message(self) -> None:
        """Show a message when the active booking limit is reached."""
        print("You have reached the limit of 3 active bookings.")

    def display_booking_ban_info(self, bookings: List[object]) -> None:
        """Show ban message and existing bookings."""
        print("You are currently banned from making new bookings.")
        print("You can still view your existing bookings:")
        self.display_current_bookings(bookings)

    def display_current_bookings(self, bookings: List[object]) -> None:
        """Display current active bookings."""
        if not bookings:
            print("No current bookings.")
            return

        print("\nCurrent bookings:")
        for booking in bookings:
            self.display_booking_line(booking)

    def display_booking_line(self, booking: object) -> None:
        """Display one booking in a readable format."""
        room = booking.get_room()
        equipment = "Yes" if booking.get_equipment_rental() else "No"
        start_text = booking.get_start_time().strftime("%Y-%m-%d %H:%M")
        end_text = booking.get_end_time().strftime(END_TIME_DISPLAY_FORMAT)
        print(
            f"{booking.get_booking_id()} | "
            f"{room.get_building()} {room.get_room_id()} "
            f"{room.get_room_name()} | "
            f"{start_text} - {end_text} | "
            f"Equipment: {equipment} | "
            f"Price: ${booking.get_total_price():.2f}"
        )

    def display_eligibility_status(
        self,
        is_banned: bool,
        available_slots: int,
    ) -> None:
        """Show whether the student can make a booking."""
        if is_banned:
            print("Booking status: banned from new bookings.")
        else:
            print("Booking status: eligible to make bookings.")
        print(f"Available slot groups: {available_slots}")

    def display_duration_rule_message(self) -> None:
        """Show the booking duration rule."""
        print("Booking duration must be at least 1 hour.")
        print("Booking duration must use 30-minute increments.")

    def display_booking_confirmation(self, booking: object) -> None:
        """Show confirmation after a booking is created."""
        print("Booking confirmed.")
        self.display_booking_line(booking)

    def display_booking_failure_message(self, reason: str) -> None:
        """Display a friendly message for common booking failure reasons."""
        messages = {
            REASON_BANNED: "Booking failed because the student is banned.",
            REASON_BOOKING_LIMIT_REACHED: (
                "Booking failed because the student already has 3 bookings."
            ),
            REASON_INVALID_DURATION: (
                "Booking failed because the duration rule was not met."
            ),
            REASON_ROOM_UNAVAILABLE: (
                "Booking failed because the room is no longer available."
            ),
            REASON_INSUFFICIENT_BALANCE: (
                "Booking failed because the account balance is insufficient."
            ),
            REASON_INSUFFICIENT_DEAL_HOURS: (
                "Booking failed because deal package hours are insufficient."
            ),
            REASON_DEAL_PACKAGE_EQUIPMENT_RESTRICTED: (
                "Deal package cannot be used with equipment rental."
            ),
            REASON_INVALID_PAYMENT_METHOD: (
                "Booking failed because the payment method is invalid."
            ),
        }
        print(messages.get(reason, "Booking failed."))

