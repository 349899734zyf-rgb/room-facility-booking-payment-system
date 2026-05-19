"""
AccountController.
Covers: Acct 5, 8-12
"""
from typing import Dict, List, Optional
from entities.student import Student


class AccountController:
    """账户控制器 (Account Management 5, 8-12)"""

    def __init__(self) -> None:
        pass

    def get_profile_info(self, student: Student) -> Dict[str, object]:
        """获取个人资料 (Acct 5)"""
        return {
            "first_name": student.get_first_name(),
            "last_name": student.get_last_name(),
            "student_id": student.get_student_id(),
            "email": student.get_email(),
            "phone": student.get_phone(),
            "balance": student.get_balance()
        }

    def get_usage_status(self, student: Student) -> Dict[str, object]:
        """获取使用状态 (Acct 8)"""
        return {
            "current_bookings": student.get_active_bookings(),
            "ban_status": student.get_booking_ban_status(),
            "balance": student.get_balance(),
            "deal_package_hours": student.get_deal_package_hours()
        }

    def get_activity_history(self, student: Student, page: int) -> List:
        """获取活动历史 (Acct 9-1.10)"""
        return student.get_activity_history_page(page)

    def get_funds_summary(self, student: Student) -> Dict[str, float]:
        """获取资金摘要 (Acct 11)"""
        return {"balance": student.get_balance()}

    def add_funds(self, student: Student, amount: float) -> bool:
        """充值 (Acct 12)"""
        return student.add_funds(amount)

