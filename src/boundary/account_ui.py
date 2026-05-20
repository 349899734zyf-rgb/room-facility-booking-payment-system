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
        print("=== Monash Student Portal ===")
        print("Welcome, {} {}! (Role: Student)".format(student.get_first_name(), student.get_last_name()))
        print("-" * 45)
        print("Student Profile Details:")
        print("- Student ID:     {}".format(student.get_student_id()))
        print("- Email Address:  {}".format(student.get_email()))
        print("- Mobile Number:  {}".format(student.get_phone()))
        print("- Account Balance:${:.2f}".format(student.get_balance()))
        print("-" * 45)
        print("1. Search & Book Rooms")
        print("2. Checkout & Payment")
        print("3. View Profile & Settings")
        print("4. View Usage Status")
        print("5. Funds Management")
        print("6. View Activity History")
        print("7. Logout")
        print()

    @staticmethod
    def get_student_menu_choice():
        """Get student menu selection."""
        return input("Selection: ").strip()

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
    def display_student_logout_message():
        """Display student logout message."""
        print()
        print("Logging Out Student Portal...")

    # ==================== Admin Menu ====================

    @staticmethod
    def display_admin_menu(admin, adm_prof):
        """Display admin portal menu."""
        print()
        print("=== Admin Control Center Home Dashboard ===")
        print("Status: Logged In Authenticated Dashboard View")
        print("-" * 45)
        print("Admin Profile Details:")
        print("- Staff Name:    {} {}".format(adm_prof["first_name"], adm_prof["last_name"]))
        print("- Staff Email:   {}".format(adm_prof["email"]))
        print("- Staff Phone:   {}".format(adm_prof["phone"]))
        print("- Security ID:   {}".format(admin.get_admin_id()))
        print("-" * 45)
        print("Administrative Control Options:")
        print("1. Room Management Console")
        print("2. Logout Profile Operations")
        print()

    @staticmethod
    def get_admin_menu_choice():
        """Get admin menu selection."""
        return input("Selection: ").strip()

    @staticmethod
    def display_admin_logout_message():
        """Display admin logout message."""
        print()
        print("Logging Out Admin Portal Workspace Dashboard...")

    @staticmethod
    def display_exit_message():
        """Display exit message."""
        print()
        print("Thank you for using MSSRB!")
