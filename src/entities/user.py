"""
Module: user.py
Layer: Entity
User Stories: Acct 1-15

Abstract base class for all system users (Student and Admin).
Provides shared attributes (email, password, name, phone) and
authentication behaviour used across the Account Management feature.
"""
from abc import ABC, abstractmethod


class User(ABC):
    """Abstract base entity for system users.

    Responsibilities:
        - Store common user credentials and profile data (Acct 1-4)
        - Provide password verification for login (Acct 15)
        - Define abstract role identification (Acct 13)

    Subclasses:
        - Student: student-specific booking and account features
        - Admin: administrative room/booking management features
    """

    def __init__(self, email: str, password: str, first_name: str, last_name: str, phone: str) -> None:
        """Initialise a user with credentials and profile information."""
        self.__email: str = email
        self.__password: str = password
        self.__first_name: str = first_name
        self.__last_name: str = last_name
        self.__phone: str = phone

    # --- Accessors ---
    def get_email(self) -> str:
        """Return the user's email address."""
        return self.__email

    def get_password(self) -> str:
        """Return the user's password."""
        return self.__password

    def get_first_name(self) -> str:
        """Return the user's first name."""
        return self.__first_name

    def get_last_name(self) -> str:
        """Return the user's last name."""
        return self.__last_name

    def get_phone(self) -> str:
        """Return the user's phone number."""
        return self.__phone

    # --- Mutators ---
    def set_email(self, email: str) -> None:
        """Update the user's email address."""
        self.__email = email

    def set_password(self, password: str) -> None:
        """Update the user's password (Acct 7)."""
        self.__password = password

    def set_first_name(self, first_name: str) -> None:
        """Update the user's first name."""
        self.__first_name = first_name

    def set_last_name(self, last_name: str) -> None:
        """Update the user's last name."""
        self.__last_name = last_name

    def set_phone(self, phone: str) -> None:
        """Update the user's phone number (Acct 6)."""
        self.__phone = phone

    # --- Business Methods ---
    @abstractmethod
    def get_role(self) -> str:
        """Return the user's role string ('student' or 'admin') (Acct 13)."""
        pass

    def verify_password(self, input_password: str) -> bool:
        """Verify a password attempt against the stored password (Acct 15)."""
        return self.__password == input_password

    def __str__(self) -> str:
        """Return a human-readable representation of the user."""
        return f"User({self.__email}, {self.__first_name} {self.__last_name})"

