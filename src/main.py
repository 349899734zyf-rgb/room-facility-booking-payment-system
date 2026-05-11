from datetime import datetime
from entity_classes import Student, Room
from controller_classes import BookingController


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


# Call in main.py's if __name__ == "__main__":
if __name__ == "__main__":
    main_admin_room_management()



