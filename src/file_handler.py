"""
Module: file_handler.py
Layer: Utility (cross-cutting)
User Stories: Acct 4 (persist registration), Acct 15 (load for login)

Handles CSV-based persistence of student data: saving new registrations
and loading existing student records with full attribute restoration.
"""
import csv
import os
from entities.student import Student

class FileHandler:
    """Utility class for CSV-based student data persistence.

    Responsibilities:
        - Save a student's full state to a CSV file (Acct 4)
        - Load all students from CSV with backward-compatible field parsing (Acct 15)
    """
    Fields = [
        'firstName', 'lastName', 'sID', 'phone', 'email', 'password', 'balance',
        'booking_ban_status', 'late_cancellation_count', 'no_show_count', 'deal_package_hours', 'used_promo_codes'
    ]

    @staticmethod
    def save_student(file_path, student):
        file_exists = os.path.exists(file_path)
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FileHandler.Fields)
            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'firstName': student.get_first_name(),
                'lastName': student.get_last_name(),
                'sID': student.get_student_id(),
                'phone': student.get_phone(),
                'email': student.get_email(),
                'password': student.get_password(),
                'balance': student.get_balance(),
                'booking_ban_status': str(student.get_booking_ban_status()),
                'late_cancellation_count': student.get_late_cancellation_count(),
                'no_show_count': student.get_no_show_count(),
                'deal_package_hours': student.get_deal_package_hours(),
                'used_promo_codes': ';'.join(student.get_used_promo_codes())
            })

    @staticmethod
    def load_students(file_path):
        students = []
        if not os.path.exists(file_path):
            return students

        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                s = Student(
                    row['email'],
                    row['password'],
                    row['firstName'],
                    row['lastName'],
                    row['phone'],
                    row['sID']
                )
                s.set_balance(float(row['balance']))
                
                # Check optional fields with defaults to maintain backward-compatibility
                ban_status = row.get('booking_ban_status', 'False')
                s.set_booking_ban_status(ban_status == 'True')
                
                s.set_late_cancellation_count(int(row.get('late_cancellation_count', 0)))
                s.set_no_show_count(int(row.get('no_show_count', 0)))
                s.set_deal_package_hours(float(row.get('deal_package_hours', 0.0)))
                
                used_promos = row.get('used_promo_codes', '')
                if used_promos:
                    for code in used_promos.split(';'):
                        if code:
                            s.mark_promo_code_used(code)
                
                students.append(s)
        return students