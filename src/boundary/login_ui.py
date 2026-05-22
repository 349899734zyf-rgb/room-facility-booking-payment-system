"""
Module: login_ui.py
Layer: Boundary
User Stories: Acct 4, 15

Text-based interface for user login: credential input prompts,
login success/error display messages.
"""


class LoginUI:
    """Login boundary class (Account Management 4, 15)"""

    @staticmethod
    def display_login_header():
        """Display login section header."""
        print()
        print("=== Account Login ===")

    @staticmethod
    def get_login_credentials():
        """Get email and password from user."""
        email = input("Enter Email (or enter 'CANCEL' to return): ").strip()
        if email.upper() == "CANCEL":
            return "CANCEL", ""
        password = input("Enter Password (or enter 'CANCEL' to return): ").strip()
        if password.upper() == "CANCEL":
            return "CANCEL", "CANCEL"
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
