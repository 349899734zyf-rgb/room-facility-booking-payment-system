"""
Module: admin.py
Layer: Entity
User Stories: Acct 13-15, Room 1-11

Represents an administrator who can manage rooms, bookings,
equipment, and student accounts.
"""
from typing import List


from entities.user import User


class Admin(User):
    """Administrator entity extending User.

    Responsibilities:
        - Identify as 'admin' role for access control (Acct 13)
        - Store promotion ideas for room marketing (Room 2)

    Collaborators:
        - AdminController: delegates admin business operations
    """

    def __init__(self, email: str, password: str, first_name: str, last_name: str,
                 phone: str, admin_id: str) -> None:
        """Initialise an admin with profile data and a unique admin ID."""
        super().__init__(email, password, first_name, last_name, phone)
        self.__admin_id: str = admin_id
        self.__promotion_ideas: List[str] = []

    # --- Accessors ---
    def get_admin_id(self) -> str:
        """Return the unique administrator identifier."""
        return self.__admin_id

    def get_promotion_ideas(self) -> List[str]:
        """Return the list of recorded promotion ideas (Room 2)."""
        return self.__promotion_ideas

    # --- Mutators ---
    def set_admin_id(self, admin_id: str) -> None:
        """Update the administrator identifier."""
        self.__admin_id = admin_id

    # --- Business Methods ---
    def get_role(self) -> str:
        """Return 'admin' as the user role (Acct 13)."""
        return "admin"

    def record_promotion_idea(self, idea: str) -> bool:
        """Record promotion idea (Room 2)"""
        if idea.strip():
            self.__promotion_ideas.append(idea)
            return True
        return False

