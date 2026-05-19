"""
User - Abstract base class.
Covers: Acct 1-15
"""
from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, email: str, password: str, first_name: str, last_name: str, phone: str) -> None:
        self.__email: str = email
        self.__password: str = password
        self.__first_name: str = first_name
        self.__last_name: str = last_name
        self.__phone: str = phone

    # --- Accessors ---
    def get_email(self) -> str:
        return self.__email

    def get_password(self) -> str:
        return self.__password

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def get_phone(self) -> str:
        return self.__phone

    # --- Mutators ---
    def set_email(self, email: str) -> None:
        self.__email = email

    def set_password(self, password: str) -> None:
        self.__password = password

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = first_name

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = last_name

    def set_phone(self, phone: str) -> None:
        self.__phone = phone

    # --- Business Methods ---
    @abstractmethod
    def get_role(self) -> str:
        pass

    def verify_password(self, input_password: str) -> bool:
        return self.__password == input_password

    def __str__(self) -> str:
        return f"User({self.__email}, {self.__first_name} {self.__last_name})"

