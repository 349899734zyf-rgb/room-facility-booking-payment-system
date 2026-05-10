from datetime import datetime
from typing import List

from boundary.booking_ui import BookingUI


class CancellationUI:
    """Boundary class for reviewing and cancelling bookings."""

    def display_booking_list_for_cancel(self, bookings: List[object]) -> None:
        """Show bookings that can be selected for cancellation."""
        print("\nBookings available for cancellation:")
        BookingUI().display_current_bookings(bookings)

    def get_booking_selection(self) -> str:
        """Get the booking ID the student wants to cancel."""
        return input("Enter booking ID to cancel: ").strip()

    def display_booking_details(self, booking: object, current_time: datetime) -> None:
        """Show selected booking details before final confirmation."""
        print(f"Current time: {current_time:%Y-%m-%d %H:%M}")
        print("Selected booking:")
        BookingUI().display_booking_line(booking)

    def display_late_cancellation_warning(self) -> None:
        """Warn the student when the cancellation is late."""
        print("Warning: this is a late cancellation. No refund will be returned.")

    def get_cancellation_confirmation(self) -> bool:
        """Return True only when the student confirms cancellation."""
        answer = input("Confirm cancellation? (y/n): ").strip().lower()
        return answer == "y"

    def display_cancellation_result(self, cancel_type: str, refund: float) -> None:
        """Display the final result after cancellation."""
        if cancel_type == "regular_cancellation":
            print(f"Booking cancelled successfully. Refund returned: ${refund:.2f}")
        elif cancel_type == "late_cancellation":
            print("Booking cancelled as a late cancellation. No refund was returned.")
        elif cancel_type == "cancellation_stopped":
            print("Cancellation stopped. The original booking remains unchanged.")
        else:
            print("Cancellation finished.")

    def display_booking_not_found_message(self) -> None:
        print("Booking not found.")

    def display_invalid_input_message(self) -> None:
        print("Invalid booking number.")

    def display_negative_record_warning(self) -> None:
        print("This late cancellation has been recorded in the student's activity history.")

    def display_ban_applied_message(self) -> None:
        print("A booking ban has been applied because the late cancellation threshold was reached.")
