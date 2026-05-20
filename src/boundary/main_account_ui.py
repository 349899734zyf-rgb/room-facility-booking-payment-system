"""
Main Account UI Flow - Login, Registration, and Menu navigation.
Originally from Amanda's main.py, refactored to use AccountUI boundary class.
No new content added.
"""
import sys
import os
from file_handler import FileHandler
from controllers.auth_controller import AuthController
from controllers.booking_controller import BookingController
from controllers.account_controller import AccountController
from controllers.admin_controller import AdminController
from boundary.account_ui import AccountUI
from boundary.login_ui import LoginUI
from boundary.registration_ui import RegistrationUI
from boundary.profile_ui import ProfileUI
from boundary.usage_status_ui import UsageStatusUI
from boundary.funds_ui import FundsUI
from boundary.activity_history_ui import ActivityHistoryUI
from entities.student import Student
from entities.admin import Admin
from entities.room import Room


def main():
    student_file = "students.csv"

    # Initialise Layers
    auth_ctrl = AuthController()
    book_ctrl = BookingController()
    acct_ctrl = AccountController()
    admin_ctrl = AdminController()

    ui = AccountUI()
    login_ui = LoginUI()
    reg_ui = RegistrationUI()
    profile_ui = ProfileUI()
    usage_ui = UsageStatusUI()
    funds_ui = FundsUI()
    history_ui = ActivityHistoryUI()

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
            new_s.deposit_funds(50.0)
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
            while True:
                login_ui.display_login_header()
                email, password = login_ui.get_login_credentials()

                if email.upper() == "CANCEL" or password.upper() == "CANCEL":
                    print("Login cancelled! Returning to main menu.")
                    break

                user = auth_ctrl.login(email, password)

                if user:
                    role_name = user.get_role()
                    login_ui.display_login_success(role_name)

                    if role_name == "admin" and isinstance(user, Admin):
                        admin_menu(user, admin_ctrl, ui)
                    elif role_name == "student" and isinstance(user, Student):
                        student_menu(user, book_ctrl, auth_ctrl, acct_ctrl, ui, profile_ui, usage_ui, funds_ui, history_ui)
                    else:
                        login_ui.display_login_error()
                    break
                else:
                    login_ui.display_login_error()

        elif choice == "2":
            # Registration
            while True:
                reg_ui.display_registration_header()
                first_name, last_name, student_id, phone, email, password = reg_ui.get_registration_info()

                fields = [first_name, last_name, student_id, phone, email, password]
                if any(v.upper() == "CANCEL" for v in fields):
                    print("Registration cancelled! Returning to main menu!")
                    break

                if not all(fields):
                    print("Error: All registration fields are required!")
                    continue

                # Acct 2: Email Pattern Check
                if not auth_ctrl.validate_email(email):
                    print("Error: Invalid email domain! Must use @student.monash.edu!")
                    continue

                # Acct 3: Password Rule Assertion Check
                if not auth_ctrl.validate_password(password):
                    print()
                    print("Password Requirement Message:")
                    print("- Password must contain at least 8 characters.")
                    print("- Must contain at least 1 uppercase letter.")
                    print("- Must contain at least 1 number.")
                    continue

                new_student = auth_ctrl.register_student(
                    email, password, first_name, last_name, phone, student_id
                )

                if new_student:
                    FileHandler.save_student(student_file, new_student)
                    reg_ui.display_registration_success()
                    input("Select any key to 'Go to Login'... ")
                    break
                else:
                    reg_ui.display_registration_error()

        elif choice == "3":
            ui.display_exit_message()
            sys.exit()


def student_menu(student, book_ctrl, auth_ctrl, acct_ctrl, ui, profile_ui, usage_ui, funds_ui, history_ui):
    while True:
        ui.display_student_menu(student)
        choice = ui.get_student_menu_choice()

        if choice == "1":
            # Search & Filter Rooms
            building, start, end = ui.get_search_input()
            rooms = book_ctrl.search_rooms(building, start, end)
            ui.display_search_results(rooms)

        elif choice == "2":
            # View Profile & Settings (Acct 5-7)
            while True:
                prof = acct_ctrl.get_profile_info(student)
                profile_ui.display_profile(
                    prof["first_name"], prof["last_name"], prof["student_id"],
                    prof["email"], prof["phone"], prof["balance"]
                )
                sub_choice = profile_ui.get_profile_choice()

                if sub_choice == "1":
                    # Update Mobile Number (Acct 6)
                    new_m = profile_ui.get_new_mobile_number()
                    if new_m.upper() == "CANCEL":
                        continue
                    conf_m = profile_ui.get_confirm_mobile_number()
                    if conf_m.upper() == "CANCEL":
                        continue

                    if auth_ctrl.update_mobile(student, new_m, conf_m):
                        if os.path.exists("students.csv"):
                            os.remove("students.csv")
                        for s in auth_ctrl.get_students():
                            FileHandler.save_student("students.csv", s)
                        profile_ui.display_mobile_update_success()
                    else:
                        profile_ui.display_invalid_mobile_format_message()

                elif sub_choice == "2":
                    # Change Password (Acct 7)
                    pwd_data = profile_ui.get_password_change_input()
                    if pwd_data["current"].upper() == "CANCEL":
                        continue

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
            # View Usage Status (Acct 8)
            status = acct_ctrl.get_usage_status(student)
            is_eligible = "Eligible" if status["balance"] >= 10.0 else "Ineligible (Low Funds)"
            status_msg = "Status: {} | No Outstanding Equipment Deposits".format(is_eligible)
            usage_ui.display_usage_status(status["current_bookings"], status["ban_status"], status["balance"], status_msg)
            usage_ui.display_return_option()

        elif choice == "4":
            # Funds Management (Acct 11-12)
            while True:
                funds_ui.display_current_balance(student.get_balance())
                funds_ui.display_top_up_options()
                fund_choice = funds_ui.get_menu_choice()

                if fund_choice == "1":
                    amount = funds_ui.get_top_up_amount()
                    if amount is None:
                        continue
                    if amount <= 0:
                        continue

                    funds_ui.display_payment_confirmation(amount)
                    if funds_ui.get_payment_confirmation():
                        acct_ctrl.add_funds(student, amount)
                        if os.path.exists("students.csv"):
                            os.remove("students.csv")
                        for s in auth_ctrl.get_students():
                            FileHandler.save_student("students.csv", s)
                        funds_ui.display_top_up_success(amount, student.get_balance())
                    else:
                        funds_ui.display_payment_cancelled()
                elif fund_choice == "2":
                    break

        elif choice == "5":
            # View Activity History (Acct 9-10)
            records = student.get_activity_history()
            page = 1
            per_page = 2
            total_pages = (len(records) + per_page - 1) // per_page
            if total_pages == 0:
                total_pages = 1

            while True:
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page
                records_slice = records[start_idx:end_idx]

                history_ui.display_page(page, total_pages)
                history_ui.display_activity_records(records_slice, start_idx)
                history_ui.display_record_type_legend()
                history_ui.display_navigation_menu()

                hist_choice = history_ui.get_page_navigation_input()
                if hist_choice == "1":
                    if page < total_pages:
                        page += 1
                    else:
                        history_ui.display_oldest_page_warning()
                elif hist_choice == "2":
                    if page > 1:
                        page -= 1
                    else:
                        history_ui.display_newest_page_warning()
                elif hist_choice == "3":
                    target_page = history_ui.get_direct_page_input(total_pages)
                    if target_page != -1:
                        page = target_page
                elif hist_choice == "4":
                    break

        elif choice == "6":
            ui.display_student_logout_message()
            break


def admin_menu(admin, admin_ctrl, ui):
    while True:
        adm_prof = admin_ctrl.get_admin_info(admin)
        ui.display_admin_menu(admin, adm_prof)
        choice = ui.get_admin_menu_choice()

        if choice == "1":
            ui.display_admin_logout_message()
            break


# The main() function only runs if this specific file is executed
if __name__ == "__main__":
    main()