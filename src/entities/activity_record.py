"""
Module: activity_record.py
Layer: Entity
User Stories: Acct 9-10

Records a single activity event (booking, recharge, late cancellation,
or no-show) in a student's activity history.
"""
from datetime import datetime


class ActivityRecord:
    """Entity representing one entry in a student's activity history.

    Responsibilities:
        - Store a timestamped record of a student activity (Acct 9)
        - Provide data for paginated activity history display (Acct 10)

    Record types: 'booking', 'recharge', 'late_cancellation', 'no_show'.
    """

    def __init__(self, date: datetime, record_type: str, details: str, amount: float) -> None:
        """Create an activity record.

        Args:
            date: Timestamp when the activity occurred.
            record_type: Category of activity ('booking', 'recharge',
                'late_cancellation', or 'no_show').
            details: Human-readable description of the activity.
            amount: Monetary amount associated with the activity.
        """
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
        return f"[{self.__date}] {self.__record_type.upper()}: {self.__details} (${self.__amount:.2f})"

