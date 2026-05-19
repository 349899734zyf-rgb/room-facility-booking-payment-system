"""
AdminController.
Covers: Room 2, 9-11; Acct 14
"""
from typing import List, Dict, Optional
from entities.booking import Booking
from entities.student import Student
from entities.equipment import Equipment
from entities.admin import Admin


class AdminController:
    """管理员控制器 (Room Management 2, 9-11)"""

    def __init__(self) -> None:
        self.__all_bookings: List[Booking] = []
        self.__equipments: List[Equipment] = []

    def get_all_bookings(self) -> List[Booking]:
        return self.__all_bookings

    def set_all_bookings(self, bookings: List[Booking]) -> None:
        self.__all_bookings = bookings

    def get_equipments(self) -> List[Equipment]:
        return self.__equipments

    def get_admin_info(self, admin: Admin) -> Dict[str, str]:
        """获取管理员信息 (Account Management 14)"""
        return {
            "email": admin.get_email(),
            "first_name": admin.get_first_name(),
            "last_name": admin.get_last_name(),
            "phone": admin.get_phone()
        }

    def record_promotion_idea(self, admin: Admin, idea: str) -> bool:
        """记录推广创意 (Room Management 2)"""
        return admin.record_promotion_idea(idea)

    def update_booking_status(self, booking_id: str, new_status: str) -> bool:
        """更新预定状态 (Room Management 9)"""
        for b in self.__all_bookings:
            if b.get_booking_id() == booking_id:
                b.set_status(new_status)
                return True
        return False

    def ban_student(self, student: Student) -> bool:
        """封禁学生预定资格 (Room Management 10)"""
        if not student.get_booking_ban_status():
            student.set_booking_ban_status(True)
            return True
        return False

    def unban_student(self, student: Student) -> bool:
        """解除学生封禁 (Room Management 10)"""
        if student.get_booking_ban_status():
            student.set_booking_ban_status(False)
            return True
        return False

    def set_equipment_deposit(self, equipment: Equipment, amount: float) -> bool:
        """设置设备押金金额 (Room Management 11)"""
        if amount <= 0:
            return False
        equipment.set_deposit_amount(amount)
        return True

    def refund_equipment_deposit(self, equipment: Equipment, student: Student) -> bool:
        """退还设备押金 (Room Management 11)"""
        refund = equipment.refund_deposit()
        student.add_funds(refund)
        return True

