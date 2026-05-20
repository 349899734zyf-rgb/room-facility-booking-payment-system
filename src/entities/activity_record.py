"""
ActivityRecord entity.
Covers: Acct 9-10
"""
from datetime import datetime


class ActivityRecord:
    """Activity record entity (Account Management 9-10)"""

    def __init__(self, date: datetime, record_type: str, details: str, amount: float) -> None:
        self.__date: datetime = date
        self.__record_type: str = record_type  # booking/recharge/late_cancellation/no_show
        self.__details: str = details
        self.__amount: float = amount

    # --- Accessors ---
    def get_date(self) -> datetime:
        return self.__date

    def get_record_type(self) -> str:
        return self.__record_type

    def get_details(self) -> str:
        return self.__details

    def get_amount(self) -> float:
        return self.__amount

    # --- Mutators ---
    def set_date(self, date: datetime) -> None:
        self.__date = date

    def set_record_type(self, record_type: str) -> None:
        self.__record_type = record_type

    def set_details(self, details: str) -> None:
        self.__details = details

    def set_amount(self, amount: float) -> None:
        self.__amount = amount

    def __str__(self) -> str:
        return f"[{self.__date}] {self.__record_type}: {self.__details} (${self.__amount})"

