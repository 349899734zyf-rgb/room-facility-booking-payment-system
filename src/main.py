import sys
from file_handler import FileHandler
from controller_classes import AuthController, BookingController
from boundary_classes import LoginUI, RegistrationUI, BookingUI
from entity_classes import Student, Room

def main():
    student_file = "students.csv"

    #Initialise Layers
    auth_ctrl = AuthController()
    book_ctrl = BookingController()

    login_ui = LoginUI()
    reg_ui = RegistrationUI()
    book_ui = BookingUI()

    #Load existing students from CSV into the system
    existing_students = FileHandler.load_students(student_file)
    auth_ctrl.get_students().extend(existing_students)

    #Test Accounts
    test_users = [
        ("Student", "One", "00000001", "0461812001", "student1@student.monash.edu", "123456"),
        ("Student", "Two", "00000002", "0461812002", "student2@student.monash.edu", "123456")
    ]

    emails_in_system = [s.get_email() for s in auth_ctrl.get_students()]

    for firstName, lastName, sID, phone, email, password in test_users:
        if email not in emails_in_system:
            new_s = Student(firstName, lastName, sID, phone, email, password)
            auth_ctrl.get_students().append(new_s)
            FileHandler.save_student(student_file, new_s)

    #Main Menu Loop
    while True:
        print()
        print("=== Monash Smart Study Room Booking System (MSSRB) ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        print()
        choice = input("Selection: ")

        if choice == "1":
            #Login
            creds = login_ui.get_login_credentials()
            user = auth_ctrl.login(creds['email'], creds['password'])

            if user:
                login_ui.display_login_success(user.get_role())
                if isinstance(user, Student):
                    student_menu(user, book_ctrl, book_ui)
                else:
                    print("Staff/Admin portal not yet implemented.")
            else:
                login_ui.display_invalid_credentials_message()

        elif choice == "2":
            #Registration
            data = reg_ui.get_registration_input()
            new_student = auth_ctrl.register_student(data['firstName'], data['lastName'], data['sID'], data['phone'], data['email'], data['password'])

            if new_student:
                FileHandler.save_student(student_file, new_student)
                reg_ui.display_success_message()
            else:
                reg_ui.display_error_message("Registration Failed!")

        elif choice == "3":
            print()
            print("Thank you for using MSSRB!")
            sys.exit()

def student_menu(student, book_ctrl, book_ui):
    while True:
        print()
        print("--- Welcome, {} ---".format(student.get_first_name()))
        print("Student ID: {}".format(student.get_student_id()))
        print("Balance: ${}".format(student.get_balance()))
        print()
        print("1. Search & Filter Rooms")
        print("2. Logout")

        print()
        choice = input("Selection: ")

        if choice == "1":
            #Search Logic
            criteria = book_ui.get_search_criteria()
            # Controller finds the rooms based on UI input
            rooms = book_ctrl.search_rooms(
                criteria['building'],
                criteria['start'],
                criteria['end']
            )
            # UI displays the list of room objects
            book_ui.display_available_rooms(rooms)

        elif choice == "2":
            print()
            print("Logging Out...")
            break

#The main() function only runs if this specific file is executed
if __name__ == "__main__":
    main()