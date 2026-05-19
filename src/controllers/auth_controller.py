"""
AuthController.
Covers: Acct 1-4, 6-7, 13, 15
"""
from typing import Dict, List, Optional
from entities.student import Student
from entities.admin import Admin
from entities.user import User


class AuthController:
    """Auth Controller (Account Management 1-4, 6-7, 13-15)"""

    def __init__(self) -> None:
        self.__students: List[Student] = []
        self.__admins: List[Admin] = []

    def get_students(self) -> List[Student]:
        return self.__students

    def get_admins(self) -> List[Admin]:
        return self.__admins

    def validate_email(self, email: str) -> bool:
        return email.endswith("@student.monash.edu")

    def validate_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_upper and has_digit

    def validate_mobile(self, mobile: str) -> bool:
        return len(mobile) == 10 and mobile.startswith("04") and mobile.isdigit()

    def register_student(self, email: str, password: str, first_name: str,
                          last_name: str, phone: str, student_id: str) -> Optional[Student]:
        if not all([email, password, first_name, last_name, phone, student_id]):
            return None
        if not self.validate_email(email):
            return None
        if not self.validate_password(password):
            return None
        student = Student(email, password, first_name, last_name, phone, student_id)
        self.__students.append(student)
        return student

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
        """Change password (Acct 7)"""
        if not user.verify_password(current_pwd):
            return False
        if new_pwd != confirm_pwd:
            return False
        if not self.validate_password(new_pwd):
            return False
        user.set_password(new_pwd)
        return True

    def update_mobile(self, user: User, new_mobile: str, confirm_mobile: str) -> bool:
        """Update mobile number (Acct 6)"""
        if new_mobile != confirm_mobile:
            return False
        if not self.validate_mobile(new_mobile):
            return False
        user.set_phone(new_mobile)
        return True

