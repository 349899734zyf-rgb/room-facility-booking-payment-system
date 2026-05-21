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
    """Admin Controller (Room Management 2, 9-11)"""

    def __init__(self) -> None:
        self.__all_bookings: List[Booking] = []
        self.__equipments: List[Equipment] = []
        self.__students: List[Student] = []

    def get_all_bookings(self) -> List[Booking]:
        return self.__all_bookings

    def set_all_bookings(self, bookings: List[Booking]) -> None:
        self.__all_bookings = bookings

    def get_equipments(self) -> List[Equipment]:
        return self.__equipments

    # Methods imported from QIuerying original code

    def get_all_students(self) -> List[Student]:
        return self.__students

    def set_all_students(self, students: List[Student]) -> None:
        self.__students = students

    def add_student(self, student: Student) -> None:
        self.__students.append(student)

    def find_student(self, student_id: str) -> Optional[Student]:
        for student in self.__students:
            if student.get_student_id() == student_id:
                return student
        return None

    def get_all_equipment(self) -> List[Equipment]:
        return self.__equipments

    def find_equipment(self, equipment_id: str) -> Optional[Equipment]:
        for equipment in self.__equipments:
            if equipment.get_equipment_id() == equipment_id:
                return equipment
        return None

    # Original methods

    def get_admin_info(self, admin: Admin) -> Dict[str, str]:
        """Get admin info (Account Management 14)"""
        return {
            "email": admin.get_email(),
            "first_name": admin.get_first_name(),
            "last_name": admin.get_last_name(),
            "phone": admin.get_phone()
        }

    def record_promotion_idea(self, admin: Admin, idea: str) -> bool:
        """Record promotion idea (Room Management 2)"""
        return admin.record_promotion_idea(idea)

    def update_booking_status(self, booking_id: str, new_status: str) -> bool:
        """Update booking status (Room Management 9)"""
        new_status = new_status.lower()
        if new_status not in ["confirmed", "completed", "cancelled", "no_show"]:
            return False
            
        for b in self.__all_bookings:
            if b.get_booking_id() == booking_id:
                if new_status == "no_show":
                    student = b.get_student()
                    room = b.get_room()
                    room_type = room.get_room_type() if hasattr(room, "get_room_type") else "Small"
                    
                    deposit_refund = b.get_equipment_deposit()
                    if room_type == "Small":
                        room_refund = b.get_total_price() * 0.2
                    else:
                        room_refund = 0.0
                    refund = room_refund + deposit_refund
                    if refund > 0:
                        student.add_funds(refund)
                        
                    student.record_no_show()
                    student.remove_booking(b)
                    
                    start_text = b.get_start_time().strftime("%Y-%m-%d %H:%M")
                    end_text = b.get_end_time().strftime("%Y-%m-%d %H:%M")
                    room.update_availability(f"{start_text}-{end_text}", True)
                
                b.set_status(new_status)
                return True
        return False

    def ban_student(self, student: Student) -> bool:
        """Ban student booking eligibility (Room Management 10)"""
        if not student.get_booking_ban_status():
            student.set_booking_ban_status(True)
            return True
        return False

    def unban_student(self, student: Student) -> bool:
        """Unban student (Room Management 10)"""
        if student.get_booking_ban_status():
            student.set_booking_ban_status(False)
            return True
        return False

    def set_equipment_deposit(self, equipment: Equipment, amount: float) -> bool:
        """Set equipment deposit amount (Room Management 11)"""
        if amount <= 0:
            return False
        equipment.set_deposit_amount(amount)
        return True

    def refund_equipment_deposit(self, equipment: Equipment, student: Student) -> bool:
        """Refund equipment deposit (Room Management 11)"""
        refund = equipment.refund_deposit()
        student.add_funds(refund)
        return True


