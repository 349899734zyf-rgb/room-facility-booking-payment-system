"""
Main Account UI Flow - Login, Registration, and Menu navigation.
Originally from Amanda's main.py, refactored to use AccountUI boundary class.
No new content added.
"""
import sys
from file_handler import FileHandler
from controller_classes import AuthController, BookingController
from boundary.account_ui import AccountUI
from entity_classes import Student, Admin, Room


def main():
    student_file = "students.csv"

    # Initialise Layers
    auth_ctrl = AuthController()
    book_ctrl = BookingController()
    ui = AccountUI()

    # Load existing students from CSV into the system
    existing_students = FileHandler.load_students(student_file)
    auth_ctrl.get_students().extend(existing_students)

    # Student Test Accounts
    test_users = [
        ("student1@student.monash.edu", "Password123", "Student A", "One", "0461812001", "00000001"),
        ("student2@student.monash.edu", "Password123", "Student B", "Two", "0461812002", "00000002")
    ]

    emails_in_system = [s.get_email() for s in auth_ctrl.get_students()]

    for email, password, firstName, lastName, phone, sID in test_users:
        if email not in emails_in_system:
            new_s = Student(email, password, firstName, lastName, phone, sID)
            auth_ctrl.get_students().append(new_s)
            FileHandler.save_student(student_file, new_s)

    # Admin Test Account
    admin_email = "admin1@monash.edu"
    admins_in_system = [a.get_email() for a in auth_ctrl.get_admins()]
    if admin_email not in admins_in_system:
        test_admin = Admin(admin_email, "Password123456", "Admin", "User", "0461812562", "ADMIN001")
        auth_ctrl.get_admins().append(test_admin)

    # Main Menu Loop
    while True:
        ui.display_main_menu()
        choice = ui.get_menu_choice()

        if choice == "1":
            # Login
            ui.display_login_header()
            email, password = ui.get_login_credentials()

            user = auth_ctrl.login(email, password)

            if user:
                role_name = user.get_role()
                ui.display_login_success(role_name)

                if role_name == "admin":
                    admin_menu(user, ui)
                else:
                    student_menu(user, book_ctrl, ui)
            else:
                ui.display_login_error()

        elif choice == "2":
            # Registration
            ui.display_registration_header()
            first_name, last_name, student_id, phone, email, password = ui.get_registration_info()

            new_student = auth_ctrl.register_student(
                email, password, first_name, last_name, phone, student_id
            )

            if new_student:
                FileHandler.save_student(student_file, new_student)
                ui.display_registration_success()
            else:
                ui.display_registration_error()

        elif choice == "3":
            ui.display_exit_message()
            sys.exit()


def student_menu(student, book_ctrl, ui):
    while True:
        ui.display_student_menu(student)
        choice = ui.get_student_menu_choice()

        if choice == "1":
            building, start, end = ui.get_search_input()
            rooms = book_ctrl.search_rooms(building, start, end)
            ui.display_search_results(rooms)

        elif choice == "2":
            ui.display_logout_message()
            break


def admin_menu(admin, ui):
    while True:
        ui.display_admin_menu(admin)
        choice = ui.get_admin_menu_choice()

        if choice == "1":
            ui.display_admin_logout_message()
            break


# The main() function only runs if this specific file is executed
if __name__ == "__main__":
    main()