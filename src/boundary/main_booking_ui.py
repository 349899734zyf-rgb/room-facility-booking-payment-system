import datetime
import sys
from pathlib import Path

# Add parent directory of src to sys.path for direct execution support
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from entities.student import Student
from entities.room import Room
from controllers.booking_controller import BookingController
from boundary.booking_ui import BookingUI
from booking_constants import REASON_INVALID_INPUT, REASON_NO_ROOMS


def main():
    """
    Booking demo entry point — uses BookingUI for all user interaction.
    """
    print("=== Booking System Demo ===")

    # Initialize controller and UI
    controller = BookingController()
    booking_ui = BookingUI()

    # Create sample data
    student = Student(
        "test@student.monash.edu",
        "Password1",
        "Yan",
        "Student",
        "0412345678",
        "S001"
    )

    room = Room("R001", "Study Room 1", "Building A", 4, 15.0, "09:00-18:00")
    room.set_available_time_slots([
        "2026-05-06 10:00-2026-05-06 12:00"
    ])
    controller.get_rooms().append(room)

    # --- Book 7: Check eligibility ---
    eligibility = controller.check_eligibility(student)
    booking_ui.display_eligibility_status(
        eligibility['is_banned'],
        3 - len(student.get_active_bookings())
    )

    if not eligibility['can_make_booking']:
        if eligibility['is_banned']:
            booking_ui.display_booking_ban_info(student.get_active_bookings())
        elif eligibility['has_reached_limit']:
            booking_ui.display_booking_limit_message()
        return

    # --- Book 1: Filter rooms by criteria ---
    criteria = booking_ui.get_search_criteria()
    result = controller.search_rooms(
        criteria['building'],
        criteria['start_time'],
        criteria['end_time']
    )

    if result['reason'] == REASON_INVALID_INPUT:
        booking_ui.display_invalid_input_message()
        return
    if result['reason'] == REASON_NO_ROOMS:
        booking_ui.display_no_rooms_message()
        return

    # --- Book 13: View current bookings before decision ---
    booking_ui.display_current_bookings(student.get_active_bookings())

    # Display available rooms
    available_rooms = result['rooms']
    booking_ui.display_available_rooms(available_rooms)

    # --- Book 9: Select an available room ---
    room_id = booking_ui.get_room_selection()
    selected_room = controller.select_room(available_rooms, room_id)

    if selected_room is None:
        booking_ui.display_room_selection_error()
        return

    # --- Book 8: Duration rules ---
    start_time = datetime.datetime.strptime(criteria['start_time'], "%Y-%m-%d %H:%M")
    end_time = datetime.datetime.strptime(criteria['end_time'], "%Y-%m-%d %H:%M")

    if not controller.validate_duration(start_time, end_time):
        booking_ui.display_duration_rule_message()
        return

    # --- Book 4: Equipment bundle choice ---
    booking_ui.display_equipment_options()
    try:
        equipment = booking_ui.get_equipment_choice()
    except ValueError:
        equipment = False

    if equipment:
        booking_ui.display_deposit_requirement(controller.get_equipment_deposit())

    # --- Book 15: Make booking ---
    booking_result = controller.create_booking(
        student,
        selected_room,
        start_time,
        end_time,
        equipment
    )

    if booking_result['success']:
        booking_ui.display_booking_confirmation(booking_result['booking'])
    else:
        booking_ui.display_booking_failure_message(booking_result['reason'])


if __name__ == "__main__":
    main()
