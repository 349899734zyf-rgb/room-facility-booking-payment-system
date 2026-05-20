import csv
import os
from entities.student import Student

class FileHandler:
    Fields = ['firstName', 'lastName', 'sID', 'phone', 'email', 'password', 'balance']

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
                'balance': student.get_balance()
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
                students.append(s)
        return students