import datetime
from entities.student import Student
from entities.room import Room
from controllers.booking_controller import BookingController
from controllers.room_controller import RoomController
from controllers.admin_controller import AdminController
from boundary.room_management_ui import RoomManagementUI
from boundary.booking_ui import BookingUI
from boundary.admin_ui import AdminUI
from boundary.booking_status_ui import BookingStatusUI
from boundary.ban_student_ui import BanStudentUI
from boundary.equipment_deposit_ui import EquipmentDepositUI
from booking_constants import REASON_ROOMS_FOUND, REASON_INVALID_INPUT, REASON_NO_ROOMS


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



def main_admin_room_management():
    """Room Management Main Program - Admin Operations"""

    # Create controller and UI
    room_controller = RoomController()
    room_ui = RoomManagementUI(room_controller)

    while True:
        # Display menu
        room_ui.display_room_management_menu()
        choice = room_ui.get_management_choice()

        if choice == "1":
            # ============ 1. Add New Room ============
            details = room_ui.get_room_details_input()
            if details:
                try:
                    room = room_controller.add_room(
                        name=details['name'],
                        building=details['building'],
                        capacity=int(details['capacity']),
                        price=float(details['price']),
                        opening_hours=details['opening_hours']
                    )
                    if room:
                        room_ui.display_add_room_success()
                    else:
                        room_ui.display_invalid_input_message()
                except Exception as e:
                    print(f"Error: {str(e)}")

        elif choice == "2":
            # ============ 2. View All Rooms ============
            rooms = room_controller.get_rooms()
            room_ui.display_room_list(rooms)

        elif choice == "3":
            # ============ 3. Delete Room ============
            rooms = room_controller.get_rooms()
            room_ui.display_room_list(rooms)
            room_id = room_ui.get_room_number_input()

            if room_controller.find_room(room_id) is None:
                room_ui.display_room_not_found_message()
            else:
                if room_controller.remove_room(room_id):
                    room_ui.display_remove_success()
                else:
                    room_ui.display_invalid_input_message()

        elif choice == "4":
            # ============ 4. Update Room Information ============
            rooms = room_controller.get_rooms()
            room_ui.display_room_list(rooms)
            room_id = room_ui.get_room_number_input()
            room = room_controller.find_room(room_id)

            if room is None:
                room_ui.display_room_not_found_message()
            else:
                room_ui.display_current_room_details(room)
                updates = room_ui.get_room_update_input()

                if updates:
                    # Convert string values to appropriate types
                    updates_dict = {}
                    for key, value in updates.items():
                        if key == 'capacity':
                            updates_dict[key] = int(value)
                        elif key == 'price':
                            updates_dict[key] = float(value)
                        else:
                            updates_dict[key] = value

                    if room_controller.update_room_info(room_id, updates_dict):
                        room_ui.display_update_success()
                        updated_room = room_controller.find_room(room_id)
                        room_ui.display_current_room_details(updated_room)
                    else:
                        room_ui.display_invalid_input_message()

        elif choice == "5":
            # ============ 5. Update Room Status ============
            rooms = room_controller.get_rooms()
            room_ui.display_room_list(rooms)
            room_id = room_ui.get_room_number_input()
            room = room_controller.find_room(room_id)

            if room is None:
                room_ui.display_room_not_found_message()
            else:
                status = room_ui.get_usage_status_input()

                if status:
                    is_student_in = status['is_student_in']
                    is_equipment_rented = status['is_equipment_rented']

                    if room_controller.update_room_usage_status(
                            room_id,
                            is_student_in,
                            is_equipment_rented
                    ):
                        print("\nRoom status updated successfully")
                    else:
                        room_ui.display_invalid_input_message()

        elif choice == "6":
            # ============ 6. Update Time Slots ============
            rooms = room_controller.get_rooms()
            room_ui.display_room_list(rooms)
            room_id = room_ui.get_room_number_input()
            room = room_controller.find_room(room_id)

            if room is None:
                room_ui.display_room_not_found_message()
            else:
                # Display current slots
                room_ui.display_available_time_slots(room)

                # Get new time slots using UI method
                time_slots = room_ui.get_time_slots_input()

                if time_slots:
                    if room_controller.update_room_time_slots(room_id, time_slots):
                        room_ui.display_update_success()
                    else:
                        room_ui.display_invalid_input_message()

        elif choice == "7":
            # ============ 7. View Predicted Income ============
            rooms = room_controller.get_rooms()
            room_ui.display_room_list(rooms)
            room_id = room_ui.get_room_number_input()
            room = room_controller.find_room(room_id)

            if room is None:
                room_ui.display_room_not_found_message()
            else:
                income = room_controller.get_predicted_income(room_id)
                booked_slots = room.get_available_time_slots()
                room_ui.display_room_usage_status(booked_slots, income)

        elif choice == "8":
            # ============ 8. Return to Main Menu ============
            print("\nReturning to main menu")
            break

        else:
            room_ui.display_invalid_input_message()





def main_admin_booking_status(admin_controller, booking_controller, booking_status_ui):
    """
    Story 2.9: Update Booking Status
    Administrator wants to update booking status for accurate records
    """

    while True:
        print("\n" + "=" * 80)
        print(" " * 20 + "UPDATE BOOKING STATUS")
        print("=" * 80)

        # Display all bookings
        bookings = booking_controller.get_all_bookings()
        booking_status_ui.display_booking_records(bookings)

        # Get booking to update
        booking_id = booking_status_ui.get_booking_selection()

        booking = None
        for b in booking_controller.get_all_bookings():
            if b.get_booking_id() == booking_id:
                booking = b
                break

        if booking is None:
            print("Error: Booking not found")
        else:
            # Display booking details (if method exists)
            booking_status_ui.display_booking_details(booking)

            # Get new status
            new_status = booking_status_ui.get_new_status()

            if new_status:
                if admin_controller.update_booking_status(booking_id, new_status):
                    booking_status_ui.display_status_update_success()
                else:
                    print("Error: Failed to update booking status")

        # Ask to continue
        continue_choice = input("\nUpdate another booking? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break

def main_admin_ban_student(admin_controller, auth_controller, ban_student_ui):
    """
    Story 2.10: Ban Student
    Administrator wants to ban a student for inappropriate behavior
    """

    while True:
        print("\n" + "=" * 80)
        print(" " * 25 + "BAN STUDENT")
        print("=" * 80)

        # Display all students
        students = auth_controller.get_students()

        ban_student_ui.display_students(students)

        # Get student selection
        student_id = ban_student_ui.get_student_selection()

        student = None
        for s in auth_controller.get_students():
            if s.get_student_id() == student_id:
                student = s
                break

        if student is None:
            ban_student_ui.display_student_not_found_message()
        else:
            is_banned = student.get_booking_ban_status()
            ban_student_ui.display_student_info(student_id, is_banned)

            if is_banned:
                # If already banned, ask to unban
                if ban_student_ui.get_unban_confirmation():
                    if admin_controller.unban_student(student):
                        ban_student_ui.display_unban_success()
            else:
                # If not banned, ask to ban
                if ban_student_ui.get_ban_confirmation():
                    if admin_controller.ban_student(student):
                        ban_student_ui.display_ban_success()

        continue_choice = input("\nManage another student? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break

def main_admin_equipment_deposit(admin_controller, equipment_deposit_ui):
    """
    Story 2.11: Set Equipment Deposit
    Administrator wants to set deposit amounts for equipment packages
    """

    while True:
        print("\n" + "=" * 80)
        print(" " * 20 + "SET EQUIPMENT DEPOSIT")
        print("=" * 80)

        # Display all equipment
        equipments = admin_controller.get_equipments()
        equipment_deposit_ui.display_equipment_list(equipments)

        # Get equipment selection
        equipment_id = equipment_deposit_ui.get_equipment_selection()

        equipment = None
        for eq in admin_controller.get_equipments():
            if eq.get_equipment_id() == equipment_id:
                equipment = eq
                break

        if equipment is None:
            print("Error: Equipment not found")
        else:
            current_deposit = equipment.get_deposit_amount()
            equipment_deposit_ui.display_current_deposit(equipment_id, current_deposit)

            # Get deposit amount
            amount = equipment_deposit_ui.get_deposit_amount_input()

            if amount > 0:
                if equipment_deposit_ui.get_deposit_confirmation():
                    if admin_controller.set_equipment_deposit(equipment, amount):
                        equipment_deposit_ui.display_deposit_set_success(amount)
                    else:
                        print("Error: Failed to set equipment deposit")

        continue_choice = input("\nSet deposit for another equipment? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break

def main_admin_menu(admin_controller, auth_controller, room_controller, booking_controller):
    """
    Main Admin Menu - Integrates all admin management functions
    This is the main entry point for admin operations
    """

    # Initialize all UI instances
    room_ui = RoomManagementUI(room_controller)
    admin_ui = AdminUI(admin_controller)
    booking_status_ui = BookingStatusUI(booking_controller)
    ban_student_ui = BanStudentUI(admin_controller)
    equipment_deposit_ui = EquipmentDepositUI(admin_controller)

    while True:
        # Display admin home menu
        admin_ui.display_admin_home()

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            # Room Management
            main_admin_room_management()

        elif choice == "2":
            # Update Booking Status
            main_admin_booking_status(admin_controller, booking_controller, booking_status_ui)

        elif choice == "3":
            # Ban Student
            main_admin_ban_student(admin_controller, auth_controller, ban_student_ui)

        elif choice == "4":
            # Set Equipment Deposit
            main_admin_equipment_deposit(admin_controller, equipment_deposit_ui)

        elif choice == "5":
            # Logout
            print("\nSuccess: Admin logged out successfully")
            break

        else:
            print("\nError: Invalid choice")

# Call in main.py's if __name__ == "__main__":
if __name__ == "__main__":
    main_admin_room_management()



