"""
RegistrationUI - Registration interface.
Covers: Acct 1-3
"""


class RegistrationUI:
    """Registration boundary class (Account Management 1-3)"""

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
