import datetime
from entity_classes import Student, Room
from controller_classes import BookingController, RoomController, AdminController
from boundary_classes import (
    RoomManagementUI,
    AdminUI,
    BookingStatusUI,
    BanStudentUI,
    EquipmentDepositUI
)


def main():
    """
    Entry point of the booking system.
    """
    print("=== Booking System Test ===")

    # Initialize controller
    controller = BookingController()

    # Create a sample student
    student = Student(
        "test@student.monash.edu",
        "Password1",
        "Yan",
        "Student",
        "0412345678",
        "S001"
    )

    # Create a sample room
    room = Room("R001", "Study Room 1", "Building A", 4, 15.0, "09:00-18:00")

    # Set available time slots for the room
    room.set_available_time_slots([
        "2026-05-06 10:00-2026-05-06 12:00"
    ])

    # Add room to controller
    controller.get_rooms().append(room)

    # --- Book 1: Filter rooms by criteria ---
    building = input("Enter building: ")
    start_time_str = input("Enter start time (YYYY-MM-DD HH:MM): ")
    end_time_str = input("Enter end time (YYYY-MM-DD HH:MM): ")

    rooms = controller.search_rooms(building, start_time_str, end_time_str)

    if not rooms:
        print("No available rooms found.")
        return

    print("\nAvailable rooms:")
    for i, room in enumerate(rooms):
        print(f"{i + 1}. {room.get_room_name()}")

    # --- Book 5: Create a new booking draft ---
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")

    print("\nBooking Summary:")
    print("Room:", selected_room.get_room_name())
    print("Building:", selected_room.get_building())
    print("Start time:", start_time_str)
    print("End time:", end_time_str)

    # --- Book 9: Select an available room ---
    choice = int(input("\nSelect a room number: ")) - 1
    selected_room = rooms[choice]

    print("\nSelected room:")
    print(selected_room.get_room_name())

    # --- Book 15: Make booking ---
    confirm = input("\nConfirm booking? (y/n): ")

    if confirm.lower() == "y":
        booking = controller.create_booking(
            student,
            selected_room,
            start_time,
            end_time,
            False
        )

        if booking:
            print("Booking created successfully:", booking.get_booking_id())
        else:
            print("Booking failed.")
    else:
        print("Booking cancelled.")


if __name__ == "__main__":
    main()





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
                    print(f"❌ Error: {str(e)}")

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
                    is_student_in = status['is_student_in'] == 'y'
                    is_equipment_rented = status['is_equipment_rented'] == 'y'

                    if room_controller.update_room_usage_status(
                            room_id,
                            is_student_in,
                            is_equipment_rented
                    ):
                        print("\n✅ Room status updated successfully")
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
                current_slots = room.get_available_time_slots()
                if current_slots:
                    print(f"\nCurrent time slots for {room_id}:")
                    for i, slot in enumerate(current_slots, 1):
                        print(f"  {i}. {slot}")
                else:
                    print(f"\nNo time slots available for {room_id}")

                # Get new time slots
                print("\nEnter new time slots (format: 09:00-10:00), one per line")
                print("Enter blank line to finish")

                time_slots = []
                while True:
                    slot = input("Time slot: ").strip()

                    if not slot:
                        break

                    if '-' not in slot:
                        print("❌ Format error, should be HH:MM-HH:MM")
                        continue

                    parts = slot.split('-')
                    if len(parts) != 2:
                        print("❌ Format error, should be HH:MM-HH:MM")
                        continue

                    time_slots.append(slot)

                if time_slots:
                    if room_controller.update_room_time_slots(room_id, time_slots):
                        print("\n✅ Time slots updated successfully")
                    else:
                        room_ui.display_invalid_input_message()
                else:
                    print("❌ Please enter at least one time slot")

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
            print("\n✅ Returning to main menu")
            break

        else:
            room_ui.display_invalid_input_message()

        room_ui.pause()

def main_admin_login():
    """
    Story 1.15: Admin Login
    Administrator wants to log in so they can manage rooms and system settings
    """
    print("\n" + "=" * 80)
    print(" " * 25 + "ADMIN LOGIN")
    print("=" * 80)

    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()

    # TODO: Call auth_controller to verify credentials
    # If verification succeeds, return admin object
    print("Success: Admin logged in successfully!")
    return True


def main_admin_booking_status(booking_controller, booking_status_ui):
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

        booking = booking_controller.find_booking(booking_id)

        if booking is None:
            print("Error: Booking not found")
        else:
            # Display booking details (if method exists)
            if hasattr(booking_status_ui, 'display_booking_details'):
                booking_status_ui.display_booking_details(booking)

            # Get new status
            new_status = booking_status_ui.get_new_status()

            if new_status:
                if booking_controller.update_booking_status(booking_id, new_status):
                    booking_status_ui.display_status_update_success()
                else:
                    print("Error: Failed to update booking status")

        # Ask to continue
        continue_choice = input("\nUpdate another booking? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break

def main_admin_ban_student(admin_controller, ban_student_ui):
    """
    Story 2.10: Ban Student
    Administrator wants to ban a student for inappropriate behavior
    """

    while True:
        print("\n" + "=" * 80)
        print(" " * 25 + "BAN STUDENT")
        print("=" * 80)

        # Display all students
        students = admin_controller.get_all_students()

        if hasattr(ban_student_ui, 'display_students'):
            ban_student_ui.display_students(students)

        # Get student selection
        student_id = ban_student_ui.get_student_selection()

        student = admin_controller.find_student(student_id)

        if student is None:
            ban_student_ui.display_student_not_found_message()
        else:
            is_banned = student.is_banned()
            ban_student_ui.display_student_info(student_id, is_banned)

            if is_banned:
                # If already banned, ask to unban
                if ban_student_ui.get_unban_confirmation():
                    if admin_controller.unban_student(student_id):
                        ban_student_ui.display_unban_success()
            else:
                # If not banned, ask to ban
                if ban_student_ui.get_ban_confirmation():
                    if admin_controller.ban_student(student_id):
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
        equipments = admin_controller.get_all_equipment()
        equipment_deposit_ui.display_equipment_list(equipments)

        # Get equipment selection
        equipment_id = equipment_deposit_ui.get_equipment_selection()

        equipment = admin_controller.find_equipment(equipment_id)

        if equipment is None:
            print("Error: Equipment not found")
        else:
            current_deposit = equipment.get_deposit_amount()
            equipment_deposit_ui.display_current_deposit(equipment_id, current_deposit)

            # Get deposit amount
            amount = equipment_deposit_ui.get_deposit_amount_input()

            if amount > 0:
                if equipment_deposit_ui.get_deposit_confirmation():
                    if admin_controller.set_equipment_deposit(equipment_id, amount):
                        equipment_deposit_ui.display_deposit_set_success(amount)
                    else:
                        print("Error: Failed to set equipment deposit")

        continue_choice = input("\nSet deposit for another equipment? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break

def main_admin_menu(admin_controller, room_controller, booking_controller):
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
            main_admin_booking_status(booking_controller, booking_status_ui)

        elif choice == "3":
            # Ban Student
            main_admin_ban_student(admin_controller, ban_student_ui)

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



