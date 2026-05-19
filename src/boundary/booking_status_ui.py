"""
BookingStatusUI - Booking status management interface.
Covers: Room 9
"""


class BookingStatusUI:
    """Booking Status Management Interface (Room Management 9)"""

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
            print(f"{booking.get_booking_id():<15} {booking.get_student_id():<15} "
                  f"{booking.get_room_id():<15} {booking.get_status():<15} "
                  f"{booking.get_date():<15}")

        print("=" * 150)

    def get_booking_selection(self) -> str:
        """Get booking selection from user"""
        print("\n" + "-" * 80)
        print(" " * 25 + "SELECT BOOKING TO UPDATE")
        print("-" * 80)
        return input("Enter booking ID: ").strip()

    def display_booking_details(self, booking) -> None:
        """Display booking details"""
        print("\n" + "-" * 80)
        print("Booking Details:")
        print(f"  Booking ID: {booking.get_booking_id()}")
        print(f"  Student ID: {booking.get_student_id()}")
        print(f"  Room ID: {booking.get_room_id()}")
        print(f"  Current Status: {booking.get_status()}")
        print(f"  Date: {booking.get_date()}")
        print("-" * 80)

    def get_new_status(self) -> str:
        """Get new booking status from user"""
        print("\nAvailable statuses:")
        print("1. Pending")
        print("2. Confirmed")
        print("3. Completed")
        print("4. Cancelled")

        choice = input("Select new status (1-4): ").strip()

        status_map = {
            '1': 'Pending',
            '2': 'Confirmed',
            '3': 'Completed',
            '4': 'Cancelled'
        }

        return status_map.get(choice, "")

    def display_status_update_success(self) -> None:
        """Display status update success message"""
        print("\nSuccess: Booking status updated successfully!")

