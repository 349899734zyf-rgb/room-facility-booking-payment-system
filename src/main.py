import os
from typing import cast
from file_handler import FileHandler
from controller_classes import AuthController, BookingController, AccountController
from boundary_classes import LoginUI, RegistrationUI, ProfileUI, UsageStatusUI
from entity_classes import Student, Admin, User

def main():
    student_file = "students.csv"

    #Initialise Layers
    auth_ctrl = AuthController()
    book_ctrl = BookingController()
    acct_ctrl = AccountController()

    login_ui = LoginUI()
    reg_ui = RegistrationUI()
    profile_ui = ProfileUI()
    usage_ui = UsageStatusUI()

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
            new_s.deposit_funds(50.0)
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
        choice = input("Selection: ").strip()

        if choice == "1":
            #Acct 1, Acct 4 & Acct 15: Login Verification Setup
            login_ui.display_login_form()
            creds = login_ui.get_login_credentials()
            user = auth_ctrl.login(creds["email"], creds["password"])

            if user:
                role_name = user.get_role()
                login_ui.display_login_success(role_name)

                if role_name == "admin" and isinstance(user, Admin):
                    #Acct 13 & 15: Route to Admin Workspace Portal
                    admin_menu(user, acct_ctrl)
                elif role_name == "student" and isinstance(user, Student):
                    #Acct 13: Route to Student Workspace Portal
                    student_menu(user, book_ctrl, auth_ctrl, acct_ctrl, profile_ui, usage_ui)
                else:
                    login_ui.display_invalid_credentials_message()

        elif choice == "2":
            #Acct 1: Registration
            # Acct 1: Registration Pipeline Console Implementation
            reg_ui.display_registration_form()
            data = reg_ui.get_registration_input()

            #Input validation checklist (blank fields, cancel options)
            if any(v.upper() == "CANCEL" for v in data.values()):
                print("Registration cancelled! Returning to main menu!")
                continue

            if not all(data.values()):
                reg_ui.display_incomplete_details_message()
                continue

            #Acct 2: Email Pattern Check
            if not auth_ctrl.validate_email(data["email"]):
                reg_ui.display_invalid_email_message()
                continue

            #Acct 3: Password Rule Assertion Check
            if not auth_ctrl.validate_password(data["password"]):
                reg_ui.display_password_requirement_message()
                continue

            new_student = auth_ctrl.register_student(data["email"], data["password"], data["first_name"], data["last_name"], data["phone"], data["student_id"])

            if new_student:
                FileHandler.save_student(student_file, new_student)
                reg_ui.display_success_message()
                input("Select any key to 'Go to Login'... ")
            else:
                reg_ui.display_error_message("Registration pipeline exception!")

        elif choice == "3":
            print()
            print("Thank you for using MSSRB!")
            break

def student_menu(student, book_ctrl, auth_ctrl, acct_ctrl, profile_ui, usage_ui):
    while True:
        print()
        print("=== Monash Student Portal ===")
        print("Welcome, {}! (Role: Student)".format(student.get_first_name()))
        print("1. Search & Filter Rooms")
        print("2. View Profile & Settings")
        print("3. View Usage Status")
        print("4. Funds Management")
        print("5. View Activity History")
        print("6. Logout")
        print()

        choice = input("Selection: ").strip()

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
            #Acct 5: View Profile (Must show all listed fields including Balance)
            while True:
                prof = acct_ctrl.get_profile_info(student)
                profile_ui.display_profile(prof["first_name"], prof["last_name"], prof["student_id"], prof["email"], prof["phone"], prof["balance"])

                sub_choice = input("Selection: ").strip()
                if sub_choice == "1":
                    #Acct 6: Edit Mobile Number
                    new_m = profile_ui.get_new_mobile_number()
                    if new_m.upper() == "CANCEL": continue
                    conf_m = profile_ui.get_confirm_mobile_number()
                    if conf_m.upper() == "CANCEL": continue

                    if auth_ctrl.update_mobile(student, new_m, conf_m):
                        if os.path.exists("students.csv"):
                            os.remove("students.csv")
                        for s in auth_ctrl.get_students():
                            FileHandler.save_student("students.csv", s)
                        profile_ui.display_mobile_update_success()
                    else:
                        profile_ui.display_invalid_mobile_format_message()

                elif sub_choice == "2":
                    #Acct 7: Change Password
                    pwd_data = profile_ui.get_password_change_input()
                    if pwd_data["current"].upper() == "CANCEL": continue

                    if auth_ctrl.change_password(student, pwd_data["current"], pwd_data["new"], pwd_data["confirm"]):
                        if os.path.exists("students.csv"):
                            os.remove("students.csv")
                        for s in auth_ctrl.get_students():
                            FileHandler.save_student("students.csv", s)
                        profile_ui.display_password_change_success()
                    else:
                        profile_ui.display_password_requirement_message()

                elif sub_choice == "3":
                    break

        elif choice == "3":
            #Acct 8: View Real-time Usage Analytics Dashboard
            status = acct_ctrl.get_usage_status(student)
            is_eligible = "Eligible" if status["balance"] >= 10.0 else "Ineligible (Low Funds)"
            status_msg = "Status: {} | No Outstanding Equipment Deposits".format(is_eligible)
            usage_ui.display_usage_status(status["current_bookings"], status["ban_status"], status["balance"], status_msg)
            usage_ui.display_return_option()

        elif choice == "4":
            #Acct 11 & 12: View Funds Summary & Add Funds
            while True:
                print()
                print("--- Wallet & Funds Management ---")
                print("Current Available Balance: ${:.2f}".format(student.get_balance()))
                print("-" * 35)
                print("1. Add Funds (Top-Up)")
                print("2. Return to Main Menu")
                print()
                fund_choice = input("Selection: ").strip()

                if fund_choice == "1":
                    amount_str = input("Enter top-up amount ($): ").strip()
                    if amount_str.upper() == "CANCEL":
                        continue
                    try:
                        amount = float(amount_str)
                        if amount <= 0:
                            print("[ERROR] Invalid amount message: Values must be strictly positive.")
                            continue

                        #Payment confirmation processing check step
                        print()
                        print("Payment Confirmation: Add ${:.2f} to account?".format(amount))
                        conf = input("Type 'CONFIRM' to authorise simulated banking payment or 'CANCEL': ").strip().upper()

                        if conf == "CONFIRM":
                            student.deposit_funds(amount)
                            if os.path.exists("students.csv"):
                                os.remove("students.csv")
                            for s in auth_ctrl.get_students():
                                FileHandler.save_student("students.csv", s)
                            print("[SUCCESS] Payment success message displayed!")
                            print("Updated Balance: ${:.2f} (Added Amount: ${:.2f})".format(student.get_balance(), amount))
                        else:
                            print("Payment cancelled. Original balance maintained unchanged.")
                    except ValueError:
                        print("[ERROR] Please enter a valid numerical dollar currency digit.")
                elif fund_choice == "2":
                    break

        elif choice == "5":
            #Acct 9 & 10: View Activity History & Navigate History Pages
            records = [
                {"date": "2026-05-18", "type": "Recharge", "details": "Simulated Cash Top-up Entry", "amount": "+$20.00"},
                {"date": "2026-05-19", "type": "Booking", "details": "Woodside Room 4.02 Reservation", "amount": "-$10.00"},
                {"date": "2026-05-20", "type": "Late Cancellation", "details": "SGL Room 2.11 Penalty Fee", "amount": "-$5.00"},
                {"date": "2026-05-20", "type": "No Show", "details": "LT3 Absence Forfeiture Charge", "amount": "-$10.00"}
            ]
            page = 1
            per_page = 2
            total_pages = (len(records) + per_page - 1) // per_page

            while True:
                print()
                print("--- Student Activity Ledger History (Page {} of {}) ---".format(page, total_pages))
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page

                for idx, rec in enumerate(records[start_idx:end_idx], start=start_idx + 1):
                    print("{}. [{}] Type: {} | {} | Amount: {}".format(idx, rec["date"], rec["type"], rec["details"], rec["amount"]))

                print("-" * 60)
                print("Legend Types Reference Guide: Booking | Recharge | Late Cancellation | No Show")
                print("-" * 60)
                print("1. Next Page")
                print("2. Previous Page")
                print("3. Enter Direct Page Number Target")
                print("4. Return to Main Menu")
                print()

                hist_choice = input("Selection: ").strip()
                if hist_choice == "1":
                    if page < total_pages:
                        page += 1
                    else:
                        print("You are already displaying the oldest transaction records page.")
                elif hist_choice == "2":
                    if page > 1:
                        page -= 1
                    else:
                        print("You are already displaying the newest transaction records page.")
                elif hist_choice == "3":
                    target_str = input("Enter target page index number (1-{}): ".format(total_pages)).strip()
                    if target_str.isdigit() and 1 <= int(target_str) <= total_pages:
                        page = int(target_str)
                    else:
                        print("[ERROR] Out of range tracking index targets.")
                elif hist_choice == "4":
                    break

        elif choice == "6":
            print()
            print("Logging Out Student Portal...")
            break

def admin_menu(admin: Admin, acct_ctrl: AccountController):
    while True:
        print()
        print("=== Admin Control Center Home Dashboard ===")
        print("Status: Logged In Authenticated Dashboard View")

        user_view = cast(User, admin)
        student_view = cast(Student, user_view)
        adm_prof = acct_ctrl.get_profile_info(student_view)

        #Acct 14: Admin View Info
        print("-" * 45)
        print("Admin Profile Details:")
        print("- Staff Name:    {} {}".format(adm_prof["first_name"], adm_prof["last_name"]))
        print("- Staff Email:   {}".format(adm_prof["email"]))
        print("- Staff Phone:   {}".format(adm_prof["phone"]))
        print("- Security ID:   {}".format(admin.get_admin_id()))
        print("-" * 45)
        print("Administrative Control Options:")
        print("1. Logout Profile Operations")
        print()

        choice = input("Selection: ").strip()
        if choice == "1":
            print()
            print("Logging Out Admin Portal Workspace Dashboard...")
            break

#The main() function only runs if this specific file is executed
if __name__ == "__main__":
    main()