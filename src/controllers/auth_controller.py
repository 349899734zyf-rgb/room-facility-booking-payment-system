"""
Module: auth_controller.py
Layer: Controller
User Stories: Acct 1-4, 6-7, 13, 15

Handles authentication, registration, validation of credentials
(email, password, mobile), login, role identification, and
profile update operations (password change, mobile update).
"""
from typing import Dict, List, Optional
from entities.student import Student
from entities.admin import Admin
from entities.user import User


class AuthController:
    """Controller for authentication and registration.

    Responsibilities:
        - Validate email, password, and mobile formats (Acct 1-3)
        - Register new students with duplicate checking (Acct 4)
        - Authenticate users (students and admins) via login (Acct 15)
        - Identify user role for access control (Acct 13)
        - Change password with current-password verification (Acct 7)
        - Update mobile number with confirmation matching (Acct 6)
    """

    def __init__(self) -> None:
        self.__students: List[Student] = []
        self.__admins: List[Admin] = []

    def get_students(self) -> List[Student]:
        """Return all registered students."""
        return self.__students

    def get_admins(self) -> List[Admin]:
        """Return all registered admins."""
        return self.__admins

    def validate_email(self, email: str) -> bool:
        """Check that email ends with '@student.monash.edu' (Acct 1)."""
        return email.endswith("@student.monash.edu")

    def validate_password(self, password: str) -> bool:
        """Validate password: min 8 chars, at least 1 uppercase and 1 digit (Acct 2)."""
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_upper and has_digit

    def validate_mobile(self, mobile: str) -> bool:
        """Validate mobile: 10 digits starting with '04' (Acct 3)."""
        return len(mobile) == 10 and mobile.startswith("04") and mobile.isdigit()

    def register_student(self, email: str, password: str, first_name: str,
                          last_name: str, phone: str, student_id: str) -> Optional[Student]:
        """Register a new student after validating all inputs (Acct 4).

        Returns:
            The new Student on success, or None if validation fails
            or email/ID already exists.
        """
        if not all([email, password, first_name, last_name, phone, student_id]):
            return None
        if not self.validate_email(email):
            return None
        if not self.validate_password(password):
            return None
        if not self.validate_mobile(phone):
            return None
        for s in self.__students:
            if s.get_email() == email or s.get_student_id() == student_id:
                return None
        student = Student(email, password, first_name, last_name, phone, student_id)
        self.__students.append(student)
        return student

    def find_student_by_id(self, student_id: str) -> Optional[Student]:
        """Find a student by their student ID."""
        for s in self.__students:
            if s.get_student_id() == student_id:
                return s
        return None

    def login(self, email: str, password: str) -> Optional[User]:
        """login"""
        for s in self.__students:
            if s.get_email() == email and s.verify_password(password):
                return s
        for a in self.__admins:
            if a.get_email() == email and a.verify_password(password):
                return a
        return None

    def identify_role(self, user: User) -> str:
        """Identify role (Acct 13)"""
        return user.get_role()

    def change_password(self, user: User, current_pwd: str, new_pwd: str, confirm_pwd: str) -> bool:
        """Change password after verifying current password and validating the new one (Acct 7).

        Returns:
            True if password was changed, False on verification or validation failure.
        """
        if not user.verify_password(current_pwd):
            return False
        if new_pwd != confirm_pwd:
            return False
        if not self.validate_password(new_pwd):
            return False
        user.set_password(new_pwd)
        return True

    def update_mobile(self, user: User, new_mobile: str, confirm_mobile: str) -> bool:
        """Update mobile number after matching confirmation (Acct 6).

        Returns:
            True if mobile was updated, False on mismatch or invalid format.
        """
        if new_mobile != confirm_mobile:
            return False
        if not self.validate_mobile(new_mobile):
            return False
        user.set_phone(new_mobile)
        return True

