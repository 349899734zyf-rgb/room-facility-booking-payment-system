"""
AdminUI - Admin home screen and admin-specific UI.
Extracted from QIuerying's boundary_classes.py.
Covers: Acct 14, Room 2
"""


class AdminUI:
    def __init__(self, admin_controller):
        self.admin_controller = admin_controller

    def display_admin_info(self, email: str, first_name: str,
                           last_name: str, phone: str) -> None:
        """Display admin information"""
        print("\n" + "=" * 80)
        print(" " * 25 + "ADMIN INFORMATION")
        print("=" * 80)
        print(f"Email:      {email}")
        print(f"First Name: {first_name}")
        print(f"Last Name:  {last_name}")
        print(f"Phone:      {phone}")
        print("=" * 80)

    def display_admin_home(self) -> None:
        """Display admin home screen"""
        print("\n" + "=" * 80)
        print(" " * 20 + "WELCOME TO ADMIN HOME")
        print("=" * 80)
        print("1. Room Management")
        print("2. Student Management")
        print("3. System Settings")
        print("4. View Reports")
        print("5. Logout")
        print("=" * 80)

    def get_promotion_idea_input(self) -> str:
        """Get promotion idea input from admin (Story 2.2)"""
        print("\n" + "-" * 80)
        print(" " * 20 + "RECORD PROMOTION IDEA")
        print("-" * 80)

        idea = input("Enter your promotion idea: ").strip()

        if not idea:
            print("Error: Promotion idea cannot be empty")
            return ""

        return idea

    def display_promotion_recorded(self) -> None:
        """Display confirmation that promotion idea was recorded"""
        print("\nSuccess: Promotion idea recorded successfully!")
