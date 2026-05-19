"""
Admin entity.
Covers: Acct 13-15
"""
from typing import List


class Admin(User):
    """管理员实体类 (Account Management 14-15, Room Management 1-11)"""

    def __init__(self, email: str, password: str, first_name: str, last_name: str,
                 phone: str, admin_id: str) -> None:
        super().__init__(email, password, first_name, last_name, phone)
        self.__admin_id: str = admin_id
        self.__promotion_ideas: List[str] = []

    # --- Accessors ---
    def get_admin_id(self) -> str:
        return self.__admin_id

    def get_promotion_ideas(self) -> List[str]:
        return self.__promotion_ideas

    # --- Mutators ---
    def set_admin_id(self, admin_id: str) -> None:
        self.__admin_id = admin_id

    # --- Business Methods ---
    def get_role(self) -> str:
        return "admin"

    def record_promotion_idea(self, idea: str) -> bool:
        """记录推广创意 (Room 2)"""
        if idea.strip():
            self.__promotion_ideas.append(idea)
            return True
        return False

