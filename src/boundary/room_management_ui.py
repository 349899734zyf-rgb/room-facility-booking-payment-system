"""
Module: room_management_ui.py
Layer: Boundary
User Stories: Room 1-8

Text-based admin interface for room CRUD operations: adding rooms,
viewing/searching room listings, updating room details, managing
time slots, and viewing predicted income.
"""
from typing import Dict, List, Optional


class RoomManagementUI:
    """Boundary class for admin room management console (Room 1-8)."""

    def __init__(self, room_controller, admin_controller=None):
        """Initialize RoomManagementUI with controllers"""
        self.room_controller = room_controller
        self.admin_controller = admin_controller

    # ==================== Story 2.3: View Room Management Menu ====================

    def display_room_management_menu(self) -> None:
        """Display the room management menu"""
        print("\n" + "=" * 80)
        print(" " * 20 + "ROOM MANAGEMENT MENU")
        print("=" * 80)
        print("1.  Add a New Room (Story 2.1)")
        print("2.  Record Promotion Idea (Story 2.2)")
        print("3.  Return to Main Menu")
        print("4.  Delete a Room (Story 2.4)")
        print("5.  Update Room Status - Student Presence & Equipment (Story 2.5)")
        print("6.  Update Available Time Slots (Story 2.6)")
        print("7.  View Predicted Income (Story 2.7)")
        print("8.  Change Room Information (Story 2.8)")
        print("9.  View All Rooms")
        print("=" * 80)

    def get_management_choice(self) -> str:
        """Get the user's menu choice"""
        return input("Please select an option (1-9, or enter 'CANCEL' to return): ").strip()

    def display_room_list(self, rooms: list) -> None:
        """Display all rooms in a formatted table"""
        if not rooms:
            print("\nNo rooms available")
            return

        print("\n" + "=" * 150)
        print(" " * 50 + "ROOM LIST")
        print("=" * 150)
        print(f"{'Room ID':<12} {'Room Name':<20} {'Building':<15} {'Capacity':<10} "
              f"{'Price/Hour':<12} {'Hours':<20} {'Student In':<12} {'Equipment':<12}")
        print("-" * 150)

        for room in rooms:
            student_status = 'Yes' if room.get_is_student_in_room() else 'No'
            equipment_status = 'Yes' if room.get_is_equipment_rented() else 'No'
            print(f"{room.get_room_id():<12} {room.get_room_name():<20} "
                  f"{room.get_building():<15} {room.get_capacity():<10} "
                  f"${room.get_price_per_hour():<11.2f} {room.get_opening_hours():<20} "
                  f"{student_status:<12} {equipment_status:<12}")

        print("=" * 150)

    # ==================== Story 2.1: Add a New Room ====================

    def get_room_details_input(self) -> Optional[Dict[str, str]]:
        """Get new room details from user input"""
        print("\n" + "-" * 80)
        print(" " * 25 + "ADD NEW ROOM")
        print("-" * 80)

        try:
            name = input("Enter room name (or enter 'CANCEL' to return): ").strip()
            if name.upper() == "CANCEL":
                return None
            if not name:
                print("Error: Room name cannot be empty")
                return None

            building = input("Enter building (or enter 'CANCEL' to return): ").strip()
            if building.upper() == "CANCEL":
                return None
            if not building:
                print("Error: Building cannot be empty")
                return None

            capacity_str = input("Enter capacity (positive integer, or enter 'CANCEL' to return): ").strip()
            if capacity_str.upper() == "CANCEL":
                return None
            if not capacity_str:
                print("Error: Capacity cannot be empty")
                return None

            try:
                capacity = int(capacity_str)
                if capacity <= 0:
                    print("Error: Capacity must be greater than 0")
                    return None
            except ValueError:
                print("Error: Capacity must be a valid positive integer")
                return None

            price_str = input("Enter price per hour ($) (positive number, or enter 'CANCEL' to return): ").strip()
            if price_str.upper() == "CANCEL":
                return None
            if not price_str:
                print("Error: Price cannot be empty")
                return None

            try:
                price = float(price_str)
                if price <= 0:
                    print("Error: Price must be greater than 0")
                    return None
            except ValueError:
                print("Error: Price must be a valid positive number")
                return None

            opening_hours = input("Enter opening hours (format: HH:MM-HH:MM, or enter 'CANCEL' to return): ").strip()
            if opening_hours.upper() == "CANCEL":
                return None
            if not opening_hours:
                print("Error: Opening hours cannot be empty")
                return None

            if '-' not in opening_hours or len(opening_hours.split('-')) != 2:
                print("Error: Invalid format. Please use HH:MM-HH:MM (e.g., 09:00-17:00)")
                return None

            return {
                'name': name,
                'building': building,
                'capacity': str(capacity),
                'price': str(price),
                'opening_hours': opening_hours
            }

        except Exception as e:
            print(f"Error: {e}")
            return None

    def display_add_room_success(self) -> None:
        """Display success message when room is added"""
        print("\nSuccess: Room added successfully!")

    def display_invalid_input_message(self) -> None:
        """Display invalid input error message"""
        print("\nError: Invalid input. Please try again.")

    # ==================== Story 2.2: Record Promotion Idea ====================

    def get_promotion_idea_input(self) -> Optional[str]:
        """Get promotion idea from user"""
        print("\n" + "-" * 80)
        print(" " * 20 + "RECORD PROMOTION IDEA")
        print("-" * 80)

        idea = input("Enter promotion idea (or enter 'CANCEL' to return): ").strip()
        if idea.upper() == "CANCEL":
            return None
        if not idea:
            print("Error: Promotion idea cannot be empty")
            return None

        return idea

    def display_promotion_recorded(self) -> None:
        """Display success message when promotion idea is recorded"""
        print("\nSuccess: Promotion idea recorded successfully!")

    # ==================== Story 2.4: Remove a Room ====================

    def get_room_number_input(self) -> str:
        """Get room ID input from user"""
        return input("Enter room ID (e.g., RM0001, or enter 'CANCEL' to return): ").strip()

    def display_remove_success(self) -> None:
        """Display success message when room is deleted"""
        print("\nSuccess: Room deleted successfully!")

    def display_room_not_found_message(self) -> None:
        """Display error message when room is not found"""
        print("\nError: Room not found. Please check the room ID.")

    # ==================== Story 2.5: Record Student Presence & Equipment ====================

    def get_usage_status_input(self) -> Optional[Dict[str, bool]]:
        """Get room usage status input from user"""
        print("\n" + "-" * 80)
        print(" " * 20 + "UPDATE ROOM STATUS (STUDENT & EQUIPMENT)")
        print("-" * 80)

        try:
            student_input = input("Is there a student in the room? (y/n, or enter 'CANCEL' to return): ").strip().lower()
            if student_input.upper() == "CANCEL":
                return None
            if student_input not in ['y', 'n', 'yes', 'no', 'true', 'false', '1', '0']:
                print("Error: Input must be y or n")
                return None
            is_student_in = student_input in ['y', 'yes', 'true', '1']

            equipment_input = input("Is equipment rented? (y/n, or enter 'CANCEL' to return): ").strip().lower()
            if equipment_input.upper() == "CANCEL":
                return None
            if equipment_input not in ['y', 'n', 'yes', 'no', 'true', 'false', '1', '0']:
                print("Error: Input must be y or n")
                return None
            is_equipment_rented = equipment_input in ['y', 'yes', 'true', '1']

            return {
                'is_student_in': is_student_in,
                'is_equipment_rented': is_equipment_rented
            }
        except Exception:
            print("Error: Input error occurred")
            return None

    def display_room_usage_status(self, booked_slots: list, predicted_income: float) -> None:
        """Display room usage status"""
        print("\n" + "-" * 80)
        print(" " * 25 + "ROOM USAGE STATUS")
        print("-" * 80)
        print(f"Available Time Slots: {len(booked_slots)}")

        if booked_slots:
            print("Time Slots:")
            for i, slot in enumerate(booked_slots, 1):
                print(f"  {i}. {slot}")
        else:
            print("  (No time slots available)")

        print(f"\nPredicted Income: ${predicted_income:.2f}")
        print("-" * 80)

    # ==================== Story 2.6: Update Time Slots ====================

    def get_time_slots_input(self) -> Optional[List[str]]:
        """Get time slots input from user"""
        print("\n" + "-" * 80)
        print(" " * 20 + "UPDATE AVAILABLE TIME SLOTS")
        print("-" * 80)
        print("Enter time slots (format: HH:MM-HH:MM), one per line")
        print("Enter blank line to finish, or enter 'CANCEL' to return")

        time_slots = []
        while True:
            slot = input("Time slot (or enter 'CANCEL' to return): ").strip()

            if slot.upper() == "CANCEL":
                return None

            if not slot:
                break

            if '-' not in slot:
                print("Error: Format should be HH:MM-HH:MM (e.g., 09:00-10:00)")
                continue

            parts = slot.split('-')
            if len(parts) != 2:
                print("Error: Format should be HH:MM-HH:MM")
                continue

            try:
                start_time, end_time = parts[0].strip(), parts[1].strip()
                if ':' not in start_time or ':' not in end_time:
                    print("Error: Format should be HH:MM-HH:MM")
                    continue

                time_slots.append(f"{start_time}-{end_time}")
            except Exception:
                print("Error: Format should be HH:MM-HH:MM")
                continue

        if not time_slots:
            print("Error: Please enter at least one time slot")
            return None

        return time_slots

    def display_available_time_slots(self, room) -> None:
        """Display available time slots for a room"""
        slots = room.get_available_time_slots()
        print(f"\nRoom {room.get_room_id()} available time slots:")

        if not slots:
            print("  (No time slots available)")
        else:
            for i, slot in enumerate(slots, 1):
                print(f"  {i}. {slot}")

    # ==================== Story 2.7: View Predicted Income ====================

    def display_predicted_income(self, income: float) -> None:
        """Display predicted income for a room"""
        print("\n" + "-" * 80)
        print(" " * 25 + "PREDICTED INCOME")
        print("-" * 80)
        print(f"Predicted Income: ${income:.2f}")
        print("-" * 80)

    # ==================== Story 2.8: Change Room Information ====================

    def display_current_room_details(self, room) -> None:
        """Display current room information"""
        print("\n" + "-" * 80)
        print(" " * 20 + "CURRENT ROOM INFORMATION")
        print("-" * 80)
        print(f"Room ID:        {room.get_room_id()}")
        print(f"Room Name:      {room.get_room_name()}")
        print(f"Building:       {room.get_building()}")
        print(f"Capacity:       {room.get_capacity()} students")
        print(f"Price:          ${room.get_price_per_hour():.2f}/hour")
        print(f"Opening Hours:  {room.get_opening_hours()}")
        student_in = 'Yes' if room.get_is_student_in_room() else 'No'
        equipment = 'Yes' if room.get_is_equipment_rented() else 'No'
        print(f"Student In:     {student_in}")
        print(f"Equipment:      {equipment}")
        print("-" * 80)

    def get_room_update_input(self) -> Optional[Dict[str, str]]:
        """Get room update information from user"""
        print("\nEnter information to update (leave blank to skip, or enter 'CANCEL' to return)")
        print("-" * 80)

        updates = {}

        room_name = input("New room name (or enter 'CANCEL' to return): ").strip()
        if room_name.upper() == "CANCEL":
            return None
        if room_name:
            updates['name'] = room_name

        building = input("New building (or enter 'CANCEL' to return): ").strip()
        if building.upper() == "CANCEL":
            return None
        if building:
            updates['building'] = building

        capacity_str = input("New capacity (positive integer, or enter 'CANCEL' to return): ").strip()
        if capacity_str.upper() == "CANCEL":
            return None
        if capacity_str:
            try:
                capacity = int(capacity_str)
                if capacity <= 0:
                    print("Error: Capacity must be greater than 0")
                    return None
                updates['capacity'] = capacity
            except ValueError:
                print("Error: Capacity must be a valid positive integer")
                return None

        price_str = input("New price ($) (positive number, or enter 'CANCEL' to return): ").strip()
        if price_str.upper() == "CANCEL":
            return None
        if price_str:
            try:
                price = float(price_str)
                if price <= 0:
                    print("Error: Price must be greater than 0")
                    return None
                updates['price'] = price
            except ValueError:
                print("Error: Price must be a valid positive number")
                return None

        opening_hours = input("New opening hours (format: HH:MM-HH:MM, or enter 'CANCEL' to return): ").strip()
        if opening_hours.upper() == "CANCEL":
            return None
        if opening_hours:
            if '-' not in opening_hours or len(opening_hours.split('-')) != 2:
                print("Error: Invalid format. Please use HH:MM-HH:MM (e.g., 09:00-17:00)")
                return None
            updates['opening_hours'] = opening_hours

        if not updates:
            print("Error: No information entered to update")
            return None

        return updates

    def display_update_success(self) -> None:
        """Display success message when room is updated"""
        print("\nSuccess: Room information updated successfully!")

    def display_update_failure(self) -> None:
        """Display failure message when room update fails"""
        print("\nError: Failed to update room information")

    def get_update_slot_action(self) -> Optional[str]:
        """Prompt to select action (AVAILABLE or UNAVAILABLE) (Room 6)."""
        print("\n" + "-" * 80)
        print(" " * 20 + "SELECT SLOT ACTION")
        print("-" * 80)
        print("1. AVAILABLE (Make time slot available / cancel booked)")
        print("2. UNAVAILABLE (Make time slot unavailable / book)")
        print("-" * 80)
        while True:
            choice = input("Please select an action (1 or 2, or enter 'CANCEL' to return): ").strip()
            if choice.upper() == "CANCEL":
                return None
            if choice == "1":
                return "AVAILABLE"
            elif choice == "2":
                return "UNAVAILABLE"
            print("Error: Invalid choice. Please enter 1 or 2.")

    def get_single_time_slot_input(self, action_name: str) -> Optional[str]:
        """Prompt for a single time slot input for a specific action (Room 6)."""
        print(f"\nEnter time slot to mark as {action_name}")
        print("Format: HH:MM-HH:MM (e.g., 09:00-18:00) or with date prefix")
        print("Enter 'CANCEL' to return")
        while True:
            slot = input(f"Time slot ({action_name}, or enter 'CANCEL' to return): ").strip()
            if slot.upper() == "CANCEL":
                return None
            if not slot:
                print("Error: Time slot cannot be empty")
                continue
            if '-' not in slot:
                print("Error: Format should be HH:MM-HH:MM (e.g., 09:00-10:00)")
                continue
            parts = slot.split('-')
            if len(parts) != 2:
                print("Error: Format should be HH:MM-HH:MM")
                continue
            try:
                start_part, end_part = parts[0].strip(), parts[1].strip()
                if ':' not in start_part or ':' not in end_part:
                    print("Error: Format should be HH:MM-HH:MM")
                    continue
                return slot
            except Exception:
                print("Error: Format should be HH:MM-HH:MM")
                continue

