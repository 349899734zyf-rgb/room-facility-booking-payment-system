"""
Module: account_controller.py
Layer: Controller
User Stories: Acct 5, 8-12

Provides student account operations: profile retrieval, usage status,
activity history pagination, funds summary, and balance top-up.
"""
from typing import Dict, List, Optional
from entities.student import Student


class AccountController:
    """Controller for student account management.

    Responsibilities:
        - Return student profile information (Acct 5)
        - Return booking and ban usage status (Acct 8)
        - Return paginated activity history (Acct 9-10)
        - Return account funds summary (Acct 11)
        - Process balance top-ups (Acct 12)
    """

    def __init__(self) -> None:
        pass

    def get_profile_info(self, student: Student) -> Dict[str, object]:
        """Get profile info (Acct 5)"""
        return {
            "first_name": student.get_first_name(),
            "last_name": student.get_last_name(),
            "student_id": student.get_student_id(),
            "email": student.get_email(),
            "phone": student.get_phone(),
            "balance": student.get_balance()
        }

    def get_usage_status(self, student: Student) -> Dict[str, object]:
        """Return booking status, ban status, balance, and deal hours (Acct 8)."""
        return {
            "current_bookings": student.get_active_bookings(),
            "ban_status": student.get_booking_ban_status(),
            "balance": student.get_balance(),
            "deal_package_hours": student.get_deal_package_hours()
        }

    def get_activity_history(self, student: Student, page: int) -> List:
        """Return a page of activity history records (Acct 9-10)."""
        return student.get_activity_history_page(page)

    def get_funds_summary(self, student: Student) -> Dict[str, float]:
        """Return account balance summary (Acct 11)."""
        return {"balance": student.get_balance()}

    def add_funds(self, student: Student, amount: float) -> bool:
        """Top up the student's balance (Acct 12)."""
        return student.add_funds(amount)

