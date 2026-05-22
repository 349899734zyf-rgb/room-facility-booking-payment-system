"""
Module: admin_controller.py
Layer: Controller
User Stories: Room 2, 9-11; Acct 14

Handles admin-only operations: promotion ideas, booking status updates
(including no-show refund logic), student ban/unban, and equipment
deposit management.
"""
from typing import List, Dict, Optional
from entities.booking import Booking
from entities.student import Student
from entities.equipment import Equipment
from entities.admin import Admin
from booking_constants import (
    BOOKING_STATUS_NO_SHOW,
    ROOM_TYPE_SMALL,
    SMALL_NO_SHOW_REFUND_RATE,
)


class AdminController:
    """Controller for admin-only management operations.

    Responsibilities:
        - Retrieve admin profile information (Acct 14)
        - Record marketing promotion ideas (Room 2)
        - Update booking status with no-show refund processing (Room 9)
        - Ban / unban student booking eligibility (Room 10)
        - Set and refund equipment deposits (Room 11)

    Collaborators:
        - Admin (entity): admin profile and promotion ideas
        - Student (entity): ban status, balance for refunds
        - Booking (entity): booking status updates
        - Equipment (entity): deposit amounts
    """

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
        """Return admin profile information for display (Acct 14)."""
        return {
            "email": admin.get_email(),
            "first_name": admin.get_first_name(),
            "last_name": admin.get_last_name(),
            "phone": admin.get_phone()
        }

    def record_promotion_idea(self, admin: Admin, idea: str) -> bool:
        """Record a marketing promotion idea (Room 2)."""
        return admin.record_promotion_idea(idea)

    def update_booking_status(self, booking_id: str, new_status: str) -> bool:
        """Update a booking's status; handles no-show refund logic (Room 9).

        Business Rules:
            - Valid statuses: 'confirmed', 'completed', 'cancelled', 'no_show'.
            - On 'no_show': partial refund (Small rooms get 20% of room price),
              equipment deposit is fully refunded, student gets a no-show record.
        """
        new_status = new_status.lower()
        if new_status not in ["confirmed", "completed", "cancelled", "no_show"]:
            return False
            
        for b in self.__all_bookings:
            if b.get_booking_id() == booking_id:
                if new_status == BOOKING_STATUS_NO_SHOW:
                    student = b.get_student()
                    room = b.get_room()
                    room_type = room.get_room_type() if hasattr(room, "get_room_type") else ROOM_TYPE_SMALL
                    
                    deposit_refund = b.get_equipment_deposit()
                    if room_type == ROOM_TYPE_SMALL:
                        room_refund = b.get_total_price() * SMALL_NO_SHOW_REFUND_RATE
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
        """Ban a student from making bookings (Room 10)."""
        if not student.get_booking_ban_status():
            student.set_booking_ban_status(True)
            return True
        return False

    def unban_student(self, student: Student) -> bool:
        """Unban a student to restore booking eligibility (Room 10)."""
        if student.get_booking_ban_status():
            student.set_booking_ban_status(False)
            return True
        return False

    def set_equipment_deposit(self, equipment: Equipment, amount: float) -> bool:
        """Set a new deposit amount for equipment (Room 11)."""
        if amount <= 0:
            return False
        equipment.set_deposit_amount(amount)
        return True

    def refund_equipment_deposit(self, equipment: Equipment, student: Student) -> bool:
        """Refund the equipment deposit to the student's balance (Room 11)."""
        refund = equipment.refund_deposit()
        student.add_funds(refund)
        return True


