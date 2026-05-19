"""
AccountUI - Account menu navigation UI.
Extracted from Amanda's main.py. No new content added.
Covers: Menu navigation, student/admin portal display
"""


class AccountUI:
    """Boundary class for menu navigation and portal display."""

    # ==================== Main Menu ====================

    @staticmethod
    def display_main_menu():
        """Display the MSSRB main menu."""
        print()
        print("=== Monash Smart Study Room Booking System (MSSRB) ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print()

    @staticmethod
    def get_menu_choice():
        """Get main menu selection."""
        return input("Selection: ")

    # ==================== Student Menu ====================

    @staticmethod
    def display_student_menu(student):
        """Display student portal menu."""
        print()
        print("--- Welcome, {} ---".format(student.get_first_name()))
        print("Student ID: {}".format(student.get_student_id()))
        print("Balance: ${}".format(student.get_balance()))
        print()
        print("1. Search & Filter Rooms")
        print("2. Logout")
        print()

    @staticmethod
    def get_student_menu_choice():
        """Get student menu selection."""
        return input("Selection: ")

    @staticmethod
    def get_search_input():
        """Get room search criteria from user."""
        building = input("Enter Building (e.g., Woodside): ").strip()
        start = input("Enter Start Time (e.g., 09:00): ").strip()
        end = input("Enter End Time (e.g., 11:00): ").strip()
        return building, start, end

    @staticmethod
    def display_search_results(rooms):
        """Display room search results."""
        if not rooms:
            print("No available rooms match your criteria.")
        else:
            print()
            print("Available Rooms:")
            for r in rooms:
                print("- Room ID: {} | {} (Building: {})".format(
                    r.get_room_id(), r.get_room_name(), r.get_building()))

    @staticmethod
    def display_logout_message():
        """Display logout message."""
        print()
        print("Logging Out...")

    # ==================== Admin Menu ====================

    @staticmethod
    def display_admin_menu(admin):
        """Display admin portal menu."""
        print()
        print("--- Admin Portal: {} ---".format(admin.get_first_name()))
        print("Staff ID: {}".format(admin.get_admin_id()))
        print()
        print("1. Logout")
        print()

    @staticmethod
    def get_admin_menu_choice():
        """Get admin menu selection."""
        return input("Selection: ")

    @staticmethod
    def display_admin_logout_message():
        """Display admin logout message."""
        print()
        print("Logging Out Admin Portal...")

    @staticmethod
    def display_exit_message():
        """Display exit message."""
        print()
        print("Thank you for using MSSRB!")
