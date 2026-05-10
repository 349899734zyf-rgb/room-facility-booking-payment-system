from typing import Dict, List


class BookingUI:
    """Boundary class for booking search, room selection and booking display."""

    def display_booking_options(self) -> None:
        """Show the main booking menu."""
        print("\n--- Booking Menu ---")
        print("1. Search available rooms")
        print("2. View current bookings")
        print("3. Cancel a booking")
        print("4. Return")

    def get_search_criteria(self) -> Dict[str, str]:
        """Get building and time period from the student."""
        building = input("Enter building code: ").strip()
        start_time = input("Enter start time (YYYY-MM-DD HH:MM): ").strip()
        end_time = input("Enter end time (YYYY-MM-DD HH:MM): ").strip()
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
                f"Building: {room.get_building()} | Capacity: {room.get_capacity()} | "
                f"${room.get_price_per_hour():.2f}/hour"
            )

    def display_no_rooms_message(self) -> None:
        print("No rooms are available during the selected time period.")

    def display_invalid_input_message(self) -> None:
        print("Invalid input. Please check the building code and time format.")

    def get_room_selection(self) -> str:
        """Get the room ID selected by the student."""
        return input("Enter the room ID you want to book: ").strip()

    def display_room_selection_error(self) -> None:
        print("The selected room is not in the available room list.")

    def display_equipment_options(self) -> None:
        """Show optional equipment choices."""
        print("\nEquipment bundle:")
        print("1. Borrow equipment")
        print("2. Do not borrow equipment")

    def get_equipment_choice(self) -> bool:
        """Return True if the student chooses to borrow equipment."""
        choice = input("Choose 1 or 2: ").strip()
        if choice == "1":
            return True
        if choice == "2":
            return False
        raise ValueError("Invalid equipment choice.")

    def display_deposit_requirement(self, amount: float) -> None:
        print(f"Equipment deposit required: ${amount:.2f}")

    def display_booking_limit_message(self) -> None:
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
        print(
            f"{booking.get_booking_id()} | "
            f"{room.get_building()} {room.get_room_id()} {room.get_room_name()} | "
            f"{booking.get_start_time():%Y-%m-%d %H:%M} - {booking.get_end_time():%H:%M} | "
            f"Equipment: {equipment} | Price: ${booking.get_total_price():.2f}"
        )

    def display_eligibility_status(self, is_banned: bool, available_slots: int) -> None:
        """Show whether the student can make a booking."""
        if is_banned:
            print("Booking status: banned from new bookings.")
        else:
            print("Booking status: eligible to make bookings.")
        print(f"Available slot groups: {available_slots}")

    def display_duration_rule_message(self) -> None:
        print("Booking duration must be at least 1 hour and must use 30-minute increments.")

    def display_booking_confirmation(self, booking: object) -> None:
        print("Booking confirmed.")
        self.display_booking_line(booking)

    def display_booking_failure_message(self, reason: str) -> None:
        """Display a friendly message for common booking failure reasons."""
        messages = {
            "banned": "Booking failed because the student is banned.",
            "booking_limit_reached": "Booking failed because the student already has 3 active bookings.",
            "invalid_duration": "Booking failed because the duration rule was not met.",
            "room_unavailable": "Booking failed because the room is no longer available.",
            "insufficient_balance": "Booking failed because the account balance is insufficient.",
            "insufficient_deal_hours": "Booking failed because deal package hours are insufficient.",
            "deal_package_equipment_restricted": "Deal package cannot be used with equipment rental.",
            "invalid_payment_method": "Booking failed because the payment method is invalid.",
        }
        print(messages.get(reason, "Booking failed."))
