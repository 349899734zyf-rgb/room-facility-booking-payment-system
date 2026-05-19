"""
LoginUI - Login interface.
Covers: Acct 4, 15
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
