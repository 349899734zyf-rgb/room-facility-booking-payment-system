from typing import Dict


class ProfileUI:
    """Profile UI (Account Management 5-7)"""
    def display_profile(self, first_name: str, last_name: str, student_id: str,
                        email: str, phone: str, balance: float) -> None:
        print()
        print("=== Student Profile Information ===")
        print("First Name:     {}".format(first_name))
        print("Last Name:      {}".format(last_name))
        print("Student ID:     {}".format(student_id))
        print("Email Address:  {}".format(email))
        print("Mobile Number:  {}".format(phone))
        print("Account Balance:${:.2f}".format(balance))
        print("-" * 35)
        print("1. Update Mobile Number")
        print("2. Change Password")
        print("3. Return to Main Menu")

    def get_new_mobile_number(self) -> str:
        print()
        print("=== Update Mobile Number ===")
        print("Type 'CANCEL' to return without saving.")
        print()
        return input("Enter New Mobile Number: ").strip()

    def get_confirm_mobile_number(self) -> str:
        return input("Confirm New Mobile Number: ").strip()

    def display_mobile_update_success(self) -> None:
        print("Update Result: Mobile number updated successfully!")

    def display_invalid_mobile_format_message(self) -> None:
        print("Error: Invalid format or mismatch! Follow the 04XXXXXXXX layout.")

    def get_password_change_input(self) -> Dict[str, str]:
        print()
        print("=== Change Account Password ===")
        print("Type 'CANCEL' at any prompt to exit.")
        print()
        return {
            "current": input("Enter Current Password: ").strip(),
            "new": input("Enter New Password: ").strip(),
            "confirm": input("Confirm New Password: ").strip()
        }

    def display_password_change_success(self) -> None:
        print("Password update result: Password updated successfully!")

    def display_password_requirement_message(self) -> None:
        print("Error: Passwords must match and contain 8+ characters, 1 uppercase and 1 number.")

    def get_profile_choice(self) -> str:
        return input("Selection: ").strip()

