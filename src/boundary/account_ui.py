"""
AccountUI - Account management UI for login, registration, and menus.
Extracted from Amanda's main.py. No new content added.
Covers: Acct 1-4 (Login/Registration)
"""


class AccountUI:
    """Boundary class for account-related user interactions."""

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

    # ==================== Login ====================

    @staticmethod
    def display_login_header():
        """Display login section header."""
        print()
        print("=== Account Login ===")

    @staticmethod
    def get_login_credentials():
        """Get email and password from user."""
        email = input("Enter Email: ").strip()
        password = input("Enter Password: ").strip()
        return email, password

    @staticmethod
    def display_login_success(role):
        """Display login success message based on role."""
        print()
        if role == "admin":
            print("Login Successful! Welcome to the Admin Portal!")
        else:
            print("Login Successful! Welcome to the Student Portal!")

    @staticmethod
    def display_login_error():
        """Display login error message."""
        print("Error: Invalid email or password!")

    # ==================== Registration ====================

    @staticmethod
    def display_registration_header():
        """Display registration section header."""
        print()
        print("=== Student Registration ===")

    @staticmethod
    def get_registration_info():
        """Get all registration fields from user."""
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        student_id = input("Student ID: ").strip()
        phone = input("Phone Number: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        return first_name, last_name, student_id, phone, email, password

    @staticmethod
    def display_registration_success():
        """Display registration success message."""
        print("Registration Successful!")

    @staticmethod
    def display_registration_error():
        """Display registration error message."""
        print("Error: Registration Failed!")

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
