"""
Module: registration_ui.py
Layer: Boundary
User Stories: Acct 1-3

Text-based interface for student registration: collecting personal
details, credentials, and displaying success/error messages.
"""


class RegistrationUI:
    """Boundary class for student registration input and feedback (Acct 1-3)."""

    @staticmethod
    def display_registration_header():
        """Display registration section header."""
        print()
        print("=== Student Registration ===")

    @staticmethod
    def get_registration_info():
        """Get all registration fields from user."""
        first_name = input("First Name (or enter 'CANCEL' to return): ").strip()
        if first_name.upper() == "CANCEL":
            return "CANCEL", "", "", "", "", ""
        last_name = input("Last Name (or enter 'CANCEL' to return): ").strip()
        if last_name.upper() == "CANCEL":
            return "CANCEL", "", "", "", "", ""
        student_id = input("Student ID (8 digits, or enter 'CANCEL' to return): ").strip()
        if student_id.upper() == "CANCEL":
            return "CANCEL", "", "", "", "", ""
        phone = input("Phone Number (10 digits starting with 04, or enter 'CANCEL' to return): ").strip()
        if phone.upper() == "CANCEL":
            return "CANCEL", "", "", "", "", ""
        email = input("Email (must end with @student.monash.edu, or enter 'CANCEL' to return): ").strip()
        if email.upper() == "CANCEL":
            return "CANCEL", "", "", "", "", ""
        password = input("Password (min 8 chars, at least 1 uppercase and 1 digit, or enter 'CANCEL' to return): ").strip()
        if password.upper() == "CANCEL":
            return "CANCEL", "", "", "", "", ""
        return first_name, last_name, student_id, phone, email, password

    @staticmethod
    def display_registration_success():
        """Display registration success message."""
        print("Registration Successful!")

    @staticmethod
    def display_registration_error():
        """Display registration error message."""
        print("Error: Registration Failed!")
