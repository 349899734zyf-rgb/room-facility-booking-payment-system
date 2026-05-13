import sys
from file_handler import FileHandler
from controller_classes import AuthController, BookingController
from boundary_classes import LoginUI, RegistrationUI, BookingUI
from entity_classes import Student, Admin, Room

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

    #Student Test Accounts
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

    #Admin Test Account
    admin_email = "admin1@monash.edu"
    admins_in_system = [a.get_email() for a in auth_ctrl.get_admins()]
    if admin_email not in admins_in_system:
        test_admin = Admin(admin_email, "Password123456", "Admin", "User", "0461812562", "ADMIN001")
        auth_ctrl.get_admins().append(test_admin)

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
            print()
            print("=== Account Login ===")
            email = input("Enter Email: ").strip()
            password = input("Enter Password: ").strip()

            user = auth_ctrl.login(email, password)

            if user:
                role_name = user.get_role()

                print()
                if role_name == "admin":
                    print("Login Successful! Welcome to the Admin Portal!")
                    admin_menu(user)
                else:
                    print("Login Successful! Welcome to the Student Portal!")
                    student_menu(user, book_ctrl, book_ui)
            else:
                print("Error: Invalid email or password!")

        elif choice == "2":
            #Registration
            print()
            print("=== Student Registration ===")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            student_id = input("Student ID: ").strip()
            phone = input("Phone Number: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()

            new_student = auth_ctrl.register_student(
                email,
                password,
                first_name,
                last_name,
                phone,
                student_id
            )

            if new_student:
                FileHandler.save_student(student_file, new_student)
                print("Registration Successful!")
            else:
                print("Error: Registration Failed!")

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
            #Search console inputs
            building = input("Enter Building (e.g., Woodside): ").strip()
            start = input("Enter Start Time (e.g., 09:00): ").strip()
            end = input("Enter End Time (e.g., 11:00): ").strip()

            #Controller searches using input variables
            rooms = book_ctrl.search_rooms(building, start, end)

            if not rooms:
                print("No available rooms match your criteria.")
            else:
                print()
                print("Available Rooms:")
                for r in rooms:
                    print("- Room ID: {} | {} (Building: {})".format(r.get_room_id(), r.get_room_name(), r.get_building()))

        elif choice == "2":
            print()
            print("Logging Out...")
            break

def admin_menu(admin):
    while True:
        print()
        print("--- Admin Portal: {} ---".format(admin.get_first_name()))
        print("Staff ID: {}".format(admin.get_admin_id()))
        print()
        print("1. Logout")
        print()

        choice = input("Selection: ")
        if choice == "1":
            print()
            print("Logging Out Admin Portal...")
            break

#The main() function only runs if this specific file is executed
if __name__ == "__main__":
    main()