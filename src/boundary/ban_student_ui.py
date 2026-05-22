"""
Module: ban_student_ui.py
Layer: Boundary
User Stories: Room 10

Text-based interface for viewing students, selecting a student,
and confirming ban/unban actions on student booking eligibility.
"""


class BanStudentUI:
    """Boundary class for student ban/unban management (Room 10)."""

    def __init__(self, admin_controller):
        self.admin_controller = admin_controller

    def display_students(self, students: list) -> None:
        """Display all students"""
        if not students:
            print("\nNo students found")
            return

        print("\n" + "=" * 120)
        print(" " * 45 + "STUDENT LIST")
        print("=" * 120)
        print(f"{'Student ID':<15} {'Name':<20} {'Email':<30} {'Status':<15}")
        print("-" * 120)

        for student in students:
            status = "BANNED" if student.get_booking_ban_status() else "ACTIVE"
            print(f"{student.get_student_id():<15} {student.get_first_name() + ' ' + student.get_last_name():<20} "
                  f"{student.get_email():<30} {status:<15}")

        print("=" * 120)

    def get_student_selection(self) -> str:
        """Get student selection from user"""
        print("\n" + "-" * 80)
        print(" " * 25 + "SELECT STUDENT")
        print("-" * 80)
        return input("Enter student ID (8 digits, or enter 'CANCEL' to return): ").strip()

    def display_student_info(self, student_id: str, ban_status: bool) -> None:
        """Display student information"""
        print("\n" + "-" * 80)
        print("Student Information:")
        print(f"  Student ID: {student_id}")
        status = "BANNED" if ban_status else "ACTIVE"
        print(f"  Status: {status}")
        print("-" * 80)

    def get_ban_confirmation(self) -> bool:
        """Get ban confirmation from user"""
        confirm = input("\nAre you sure you want to ban this student? (y/n, or enter 'CANCEL' to return): ").strip().lower()
        if confirm.upper() == "CANCEL":
            return None
        return confirm in ['y', 'yes']

    def get_unban_confirmation(self) -> bool:
        """Get unban confirmation from user"""
        confirm = input("\nAre you sure you want to unban this student? (y/n, or enter 'CANCEL' to return): ").strip().lower()
        if confirm.upper() == "CANCEL":
            return None
        return confirm in ['y', 'yes']

    def display_ban_success(self) -> None:
        """Display ban success message"""
        print("\nSuccess: Student banned successfully!")

    def display_unban_success(self) -> None:
        """Display unban success message"""
        print("\nSuccess: Student unbanned successfully!")

    def display_student_not_found_message(self) -> None:
        """Display student not found message"""
        print("\nError: Student not found")

