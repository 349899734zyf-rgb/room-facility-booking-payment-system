"""
Module: booking_status_ui.py
Layer: Boundary
User Stories: Room 9

Text-based interface for viewing all booking records, selecting a
booking, and updating its status (confirmed/completed/cancelled/no-show).
"""


class BookingStatusUI:
    """Boundary class for booking status management (Room 9)."""

    def __init__(self, booking_controller):
        self.booking_controller = booking_controller

    def display_booking_records(self, bookings: list) -> None:
        """Display all booking records"""
        if not bookings:
            print("\nNo booking records found")
            return

        print("\n" + "=" * 150)
        print(" " * 50 + "BOOKING RECORDS")
        print("=" * 150)
        print(f"{'Booking ID':<15} {'Student ID':<15} {'Room ID':<15} {'Status':<15} {'Date':<15}")
        print("-" * 150)

        for booking in bookings:
            sid = booking.get_student().get_student_id() if hasattr(booking.get_student(), 'get_student_id') else 'N/A'
            rid = booking.get_room().get_room_id() if hasattr(booking.get_room(), 'get_room_id') else 'N/A'
            date_str = str(booking.get_start_time().strftime('%Y-%m-%d %H:%M'))
            print(f"{booking.get_booking_id():<15} {sid:<15} "
                  f"{rid:<15} {booking.get_status():<15} "
                  f"{date_str:<15}")

        print("=" * 150)

    def get_booking_selection(self) -> str:
        """Get booking selection from user"""
        print("\n" + "-" * 80)
        print(" " * 25 + "SELECT BOOKING TO UPDATE")
        print("-" * 80)
        return input("Enter booking ID (e.g., BK001, or enter 'CANCEL' to return): ").strip()

    def display_booking_details(self, booking) -> None:
        """Display booking details"""
        print("\n" + "-" * 80)
        print("Booking Details:")
        print(f"  Booking ID: {booking.get_booking_id()}")
        sid = booking.get_student().get_student_id() if hasattr(booking.get_student(), 'get_student_id') else 'N/A'
        rid = booking.get_room().get_room_id() if hasattr(booking.get_room(), 'get_room_id') else 'N/A'
        print(f"  Student ID: {sid}")
        print(f"  Room ID: {rid}")
        print(f"  Current Status: {booking.get_status()}")
        print(f"  Date: {booking.get_start_time().strftime('%Y-%m-%d %H:%M')}")
        print("-" * 80)

    def get_new_status(self) -> str:
        """Get new booking status from user"""
        print("\nAvailable statuses:")
        print("1. Pending")
        print("2. Confirmed")
        print("3. Completed")
        print("4. Cancelled")
        print("5. No Show")

        choice = input("Select new status (1-5, or enter 'CANCEL' to return): ").strip()
        if choice.upper() == "CANCEL":
            return "CANCEL"

        status_map = {
            '1': 'Pending',
            '2': 'Confirmed',
            '3': 'Completed',
            '4': 'Cancelled',
            '5': 'no_show'
        }

        return status_map.get(choice, "")

    def display_status_update_success(self) -> None:
        """Display status update success message"""
        print("\nSuccess: Booking status updated successfully!")

