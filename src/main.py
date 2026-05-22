"""
Module: main.py
Layer: Application entry point
User Stories: All

Main entry point for the Monash Smart Study Room Booking System (MSSRB).
Initialises all controllers and boundary UIs, pre-loads demonstration data,
and runs the main event loop dispatching to student and admin portals.
"""
import sys
import os
import datetime
from pathlib import Path

# Ensure the 'src' directory is in sys.path
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from file_handler import FileHandler
from controllers.auth_controller import AuthController
from controllers.booking_controller import BookingController
from controllers.account_controller import AccountController
from controllers.admin_controller import AdminController
from controllers.payment_controller import PaymentController
from controllers.room_controller import RoomController
from boundary.account_ui import AccountUI
from boundary.login_ui import LoginUI
from boundary.registration_ui import RegistrationUI
from boundary.profile_ui import ProfileUI
from boundary.usage_status_ui import UsageStatusUI
from boundary.funds_ui import FundsUI
from boundary.activity_history_ui import ActivityHistoryUI
from boundary.booking_ui import BookingUI
from boundary.payment_ui import PaymentUI
from boundary.deal_package_ui import DealPackageUI
from boundary.main_admin_ui import main_admin_menu
from entities.student import Student
from entities.admin import Admin
from entities.room import Room
from entities.equipment import Equipment
from booking_constants import REASON_INVALID_INPUT, REASON_NO_ROOMS


def run_student_booking(student, book_ctrl, booking_ui, acct_ctrl=None, funds_ui=None, auth_ctrl=None, student_file=None, payment_ctrl=None, payment_ui=None, deal_package_ui=None):
    """Integrates Booking System flow for the logged-in student.

    After successfully creating a booking, automatically transitions into
    the Checkout & Payment flow so the student can choose payment method,
    enter promo codes, and confirm payment in one continuous process.
    """
    print("\n=== Booking System ===")
    
    # Check eligibility
    eligibility = book_ctrl.check_eligibility(student)
    booking_ui.display_eligibility_status(
        eligibility['is_banned'],
        3 - len(student.get_active_bookings())
    )

    if not eligibility['can_make_booking']:
        if eligibility['is_banned']:
            booking_ui.display_booking_ban_info(student.get_active_bookings())
        elif eligibility['has_reached_limit']:
            booking_ui.display_booking_limit_message()
        return

    # Filter rooms by criteria
    criteria = booking_ui.get_search_criteria()
    if criteria['building'].upper() == "CANCEL":
        print("Booking process cancelled.")
        return

    # Parse and validate capacity input
    try:
        capacity = int(criteria['capacity'])
        if capacity <= 0:
            raise ValueError
    except (ValueError, TypeError):
        booking_ui.display_invalid_input_message()
        return

    result = book_ctrl.search_rooms(
        criteria['building'],
        criteria['start_time'],
        criteria['end_time'],
        capacity
    )

    if result['reason'] == REASON_INVALID_INPUT:
        booking_ui.display_invalid_input_message()
        return
    if result['reason'] == REASON_NO_ROOMS:
        booking_ui.display_no_rooms_message()
        return

    # View current bookings before decision
    booking_ui.display_current_bookings(student.get_active_bookings())

    # Display available rooms
    available_rooms = result['rooms']
    booking_ui.display_available_rooms(available_rooms)

    # Select an available room
    room_id = booking_ui.get_room_selection()
    if room_id.upper() == "CANCEL":
        print("Booking process cancelled.")
        return
        
    selected_room = book_ctrl.select_room(available_rooms, room_id)
    if selected_room is None:
        booking_ui.display_room_selection_error()
        return

    # Duration rules
    try:
        start_time = datetime.datetime.strptime(criteria['start_time'], "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(criteria['end_time'], "%Y-%m-%d %H:%M")
    except ValueError:
        booking_ui.display_invalid_input_message()
        return

    if not book_ctrl.validate_duration(start_time, end_time):
        booking_ui.display_duration_rule_message()
        return

    # Equipment bundle choice
    booking_ui.display_equipment_options()
    try:
        equipment = booking_ui.get_equipment_choice()
    except ValueError as e:
        if str(e) == "CANCEL":
            print("Booking process cancelled.")
            return
        equipment = False

    if equipment:
        booking_ui.display_deposit_requirement(book_ctrl.get_equipment_deposit())

    # Make booking
    booking_result = book_ctrl.create_booking(
        student,
        selected_room,
        start_time,
        end_time,
        equipment
    )

    if booking_result['success']:
        booking = booking_result['booking']
        print("\nRoom reserved! Proceeding to checkout...")
        # Automatically enter checkout & payment flow
        if payment_ctrl and payment_ui and deal_package_ui:
            run_student_payment(student, payment_ctrl, payment_ui, deal_package_ui, auth_ctrl, student_file, booking=booking)
        else:
            booking_ui.display_booking_confirmation(booking)
    else:
        booking_ui.display_booking_failure_message(booking_result['reason'])


def run_student_payment(student, payment_ctrl, payment_ui, deal_package_ui, auth_ctrl, student_file, booking=None):
    """Integrates Checkout & Payment System flow for the logged-in student."""
    print("\n=== Checkout & Payment System ===")
    
    if booking is None:
        active_bookings = student.get_active_bookings()
        if not active_bookings:
            print("\nNo current bookings found for checkout.")
            print("Please book a room first using Option 1 (Search & Book Rooms).")
            return
        else:
            print("\nYour current bookings:")
            for i, bk in enumerate(active_bookings, 1):
                print(f"{i}. Booking ID: {bk.get_booking_id()} | Room: {bk.get_room().get_room_name()} | Price: ${bk.get_total_price()}")
            print(f"{len(active_bookings) + 1}. Cancel and return")
            
            choice = input("Select a booking to checkout: ").strip()
            if choice.upper() == "CANCEL":
                return
            if not choice.isdigit():
                print("Invalid selection.")
                return
            idx = int(choice) - 1
            if idx == len(active_bookings):
                return
            if idx < 0 or idx >= len(active_bookings):
                print("Invalid selection.")
                return
            booking = active_bookings[idx]

    duration = booking.calculate_duration_hours()
    time_period = f"{booking.get_start_time()} to {booking.get_end_time()}"

    payment_ui.display_booking_summary(
        name=f"{student.get_first_name()} {student.get_last_name()}",
        room=booking.get_room().get_room_name(),
        building=booking.get_room().get_building(),
        time_period=time_period,
        price=booking.get_total_price(),
        equipment=booking.get_equipment_rental()
    )

    payment_ui.display_payment_options(
        price=booking.get_total_price(),
        duration=duration
    )

    choice = payment_ui.get_payment_method_choice()
    if choice.upper() == "CANCEL" or choice not in ["1", "2"]:
        print("Payment cancelled.")
        return

    payment_method = "deal_package" if choice == "2" else "balance"
    order = payment_ctrl.create_order(booking, payment_method)

    promo_input = payment_ui.get_promo_code_input().strip()
    if promo_input.upper() == "CANCEL":
        print("Payment cancelled.")
        return

    if promo_input and payment_method == "deal_package":
        payment_ui.display_promo_deal_package_restriction_message()
    elif promo_input:
        promo = payment_ctrl.validate_promo_code(promo_input, student)
        if promo is None:
            if student.has_used_promo_code(promo_input):
                payment_ui.display_promo_code_used_message()
            else:
                payment_ui.display_promo_code_invalid_message()
        else:
            final_price = payment_ctrl.apply_promo_code(promo, student, order)
            payment_ui.display_promo_code_valid(final_price)

    if payment_method == "balance":
        payable_amount = payment_ctrl.get_order_payable_amount(order)
        payment_ui.display_balance_payment_info(
            price=payable_amount,
            balance=student.get_balance()
        )
        success = payment_ctrl.check_balance_sufficient(student, payable_amount)
    else:
        if not payment_ctrl.can_use_deal_package(booking.get_equipment_rental(), booking.get_room().get_room_type()):
            payment_ui.display_equipment_restriction_message()
            return

        payment_ui.display_deal_package_info(
            duration=duration,
            remaining=student.get_deal_package_hours()
        )
        success = student.get_deal_package_hours() >= duration

        if not success and student.get_deal_package_hours() < duration:
            payment_ui.display_insufficient_deal_hours_message()
            package = payment_ctrl.get_deal_package()
            deal_package_ui.display_deal_package_info(
                package.get_price(),
                package.get_hours()
            )
            purchase_confirm = deal_package_ui.get_purchase_confirmation()
            if purchase_confirm is None:
                print("Payment cancelled.")
                return
            elif not purchase_confirm:
                payment_ui.display_booking_not_confirmed()
                return

            if not payment_ctrl.purchase_deal_package(student):
                payment_ui.display_insufficient_balance_message()
                payment_ui.display_top_up_option()
                top_up_choice = payment_ui.get_top_up_choice()
                if top_up_choice.upper() == "CANCEL":
                    print("Payment cancelled.")
                    return
                elif top_up_choice != "1":
                    payment_ui.display_checkout_finished()
                    return

                top_up_amount_val = payment_ui.get_top_up_amount()
                if top_up_amount_val.upper() == "CANCEL":
                    print("Payment cancelled.")
                    return
                try:
                    top_up_amount = float(top_up_amount_val)
                except ValueError:
                    payment_ui.display_invalid_payment_option_message()
                    return

                if not payment_ctrl.top_up_account(student, top_up_amount):
                    payment_ui.display_invalid_payment_option_message()
                    return

                payment_ui.display_top_up_success(student.get_balance())
                if not payment_ctrl.purchase_deal_package(student):
                    payment_ui.display_insufficient_balance_message()
                    print("\nWould you like to add more funds?")
                    print("1. Add Funds (Top-Up)")
                    print("2. Return to Main Menu")
                    retry_choice = input("\nSelection: ").strip()
                    if retry_choice != "1":
                        return
                    continue_top_up = True
                    while continue_top_up:
                        extra_val = payment_ui.get_top_up_amount()
                        if extra_val.upper() == "CANCEL":
                            return
                        try:
                            extra_amt = float(extra_val)
                        except ValueError:
                            payment_ui.display_invalid_payment_option_message()
                            return
                        if not payment_ctrl.top_up_account(student, extra_amt):
                            payment_ui.display_invalid_payment_option_message()
                            return
                        payment_ui.display_top_up_success(student.get_balance())
                        if payment_ctrl.purchase_deal_package(student):
                            continue_top_up = False
                        else:
                            payment_ui.display_insufficient_balance_message()
                            print("\nWould you like to add more funds?")
                            print("1. Add Funds (Top-Up)")
                            print("2. Return to Main Menu")
                            again = input("\nSelection: ").strip()
                            if again != "1":
                                return

            deal_package_ui.display_purchase_success(package.get_hours())
            payment_ui.display_deal_package_info(
                duration=duration,
                remaining=student.get_deal_package_hours()
            )
            success = student.get_deal_package_hours() >= duration

    if success:
        # CQ Original Flow: Confirmation before payment
        payment_ui.display_proceed_confirmation_prompt()
        proceed_choice = payment_ui.get_proceed_confirmation_choice()
        if proceed_choice.upper() == "CANCEL":
            print("Payment cancelled.")
            return
        elif proceed_choice != "1":
            payment_ui.display_booking_not_confirmed()
            return

        if payment_method == "balance":
            payment_ctrl.pay_by_balance(student, payable_amount)
        else:
            payment_ctrl.pay_by_deal_package(student, duration, booking.get_equipment_rental(), booking.get_room().get_room_type())
            payment_ui.display_deal_package_info(
                duration=duration,
                remaining=student.get_deal_package_hours()
            )

        payment_ctrl.confirm_order(order, student)
        payment_ui.display_booking_confirmed()

        # CQ Original Flow: Display order details
        summary = payment_ctrl.get_booking_summary(order)
        payment_ui.display_order_detail(
            order_id=order.get_order_id(),
            name=summary["name"],
            room=summary["room"],
            building=summary["building"],
            time_period=summary["time_period"],
            price=summary["price"],
            equipment=summary["equipment"],
            payment_method=order.get_payment_method()
        )

        payment_ui.display_next_step_options()
        next_step_choice = payment_ui.get_next_step_choice()
        if next_step_choice.upper() == "CANCEL":
            payment_ui.display_checkout_finished()
            if os.path.exists(student_file):
                os.remove(student_file)
            for s in auth_ctrl.get_students():
                FileHandler.save_student(student_file, s)
            return
        next_step = payment_ctrl.choose_next_step(next_step_choice)

        # Save state changes
        if os.path.exists(student_file):
            os.remove(student_file)
        for s in auth_ctrl.get_students():
            FileHandler.save_student(student_file, s)

    elif payment_method == "balance":
        # ===== CQ Original Flow: Insufficient balance -> redirect to top-up =====
        payment_ui.display_insufficient_balance_message()
        payment_ui.display_top_up_option()
        top_up_choice = payment_ui.get_top_up_choice()
        if top_up_choice.upper() == "CANCEL":
            print("Payment cancelled.")
            return
        elif top_up_choice != "1":
            payment_ui.display_checkout_finished()
            return

        top_up_amount_val = payment_ui.get_top_up_amount()
        if top_up_amount_val.upper() == "CANCEL":
            print("Payment cancelled.")
            return
        try:
            top_up_amount = float(top_up_amount_val)
        except ValueError:
            payment_ui.display_invalid_payment_option_message()
            return

        if not payment_ctrl.top_up_account(student, top_up_amount):
            payment_ui.display_invalid_payment_option_message()
            return

        payment_ui.display_top_up_success(student.get_balance())

        while not payment_ctrl.check_balance_sufficient(student, payable_amount):
            payment_ui.display_insufficient_balance_message()
            print("\nWould you like to add more funds?")
            print("1. Add Funds (Top-Up)")
            print("2. Return to Main Menu")
            retry_choice = input("\nSelection: ").strip()
            if retry_choice != "1":
                return
            extra_val = payment_ui.get_top_up_amount()
            if extra_val.upper() == "CANCEL":
                return
            try:
                extra_amt = float(extra_val)
            except ValueError:
                payment_ui.display_invalid_payment_option_message()
                return
            if not payment_ctrl.top_up_account(student, extra_amt):
                payment_ui.display_invalid_payment_option_message()
                return
            payment_ui.display_top_up_success(student.get_balance())

        # Confirm payment after top-up
        payment_ui.display_proceed_confirmation_prompt()
        proceed_choice = payment_ui.get_proceed_confirmation_choice()
        if proceed_choice.upper() == "CANCEL":
            print("Payment cancelled.")
            return
        elif proceed_choice != "1":
            payment_ui.display_booking_not_confirmed()
            return

        payment_ctrl.pay_by_balance(student, payable_amount)
        payment_ctrl.confirm_order(order, student)
        payment_ui.display_booking_confirmed()

        summary = payment_ctrl.get_booking_summary(order)
        payment_ui.display_order_detail(
            order_id=order.get_order_id(),
            name=summary["name"],
            room=summary["room"],
            building=summary["building"],
            time_period=summary["time_period"],
            price=summary["price"],
            equipment=summary["equipment"],
            payment_method=order.get_payment_method()
        )

        # Save state changes
        if os.path.exists(student_file):
            os.remove(student_file)
        for s in auth_ctrl.get_students():
            FileHandler.save_student(student_file, s)



def student_menu(student, book_ctrl, auth_ctrl, acct_ctrl, payment_ctrl, ui, profile_ui, usage_ui, funds_ui, history_ui, booking_ui, payment_ui, deal_package_ui, student_file):
    """Display student menu options and handle choices."""
    while True:
        ui.display_student_menu(student)
        choice = ui.get_student_menu_choice()

        if choice == "1":
            # Search & Book Rooms
            run_student_booking(student, book_ctrl, booking_ui, acct_ctrl, funds_ui, auth_ctrl, student_file, payment_ctrl, payment_ui, deal_package_ui)
            # Save student state changes that may result from booking costs
            if os.path.exists(student_file):
                os.remove(student_file)
            for s in auth_ctrl.get_students():
                FileHandler.save_student(student_file, s)

        elif choice == "2":
            # Checkout & Payment
            run_student_payment(student, payment_ctrl, payment_ui, deal_package_ui, auth_ctrl, student_file)

        elif choice == "3":
            # View Profile & Settings
            while True:
                prof = acct_ctrl.get_profile_info(student)
                profile_ui.display_profile(
                    prof["first_name"], prof["last_name"], prof["student_id"],
                    prof["email"], prof["phone"], prof["balance"]
                )
                sub_choice = profile_ui.get_profile_choice()

                if sub_choice == "1":
                    # Update Mobile Number
                    new_m = profile_ui.get_new_mobile_number()
                    if new_m.upper() == "CANCEL":
                        continue
                    conf_m = profile_ui.get_confirm_mobile_number()
                    if conf_m.upper() == "CANCEL":
                        continue

                    if auth_ctrl.update_mobile(student, new_m, conf_m):
                        if os.path.exists(student_file):
                            os.remove(student_file)
                        for s in auth_ctrl.get_students():
                            FileHandler.save_student(student_file, s)
                        profile_ui.display_mobile_update_success()
                    else:
                        profile_ui.display_invalid_mobile_format_message()

                elif sub_choice == "2":
                    # Change Password
                    pwd_data = profile_ui.get_password_change_input()
                    if pwd_data["current"].upper() == "CANCEL":
                        continue

                    if auth_ctrl.change_password(student, pwd_data["current"], pwd_data["new"], pwd_data["confirm"]):
                        if os.path.exists(student_file):
                            os.remove(student_file)
                        for s in auth_ctrl.get_students():
                            FileHandler.save_student(student_file, s)
                        profile_ui.display_password_change_success()
                    else:
                        profile_ui.display_password_requirement_message()

                elif sub_choice == "3":
                    break

        elif choice == "4":
            # View Usage Status
            status = acct_ctrl.get_usage_status(student)
            is_eligible = "Eligible" if status["balance"] >= 10.0 else "Ineligible (Low Funds)"
            status_msg = "Status: {} | No Outstanding Equipment Deposits".format(is_eligible)
            usage_ui.display_usage_status(status["current_bookings"], status["ban_status"], status["balance"], status_msg)
            usage_ui.display_return_option()

        elif choice == "5":
            # Funds Management
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
                        if os.path.exists(student_file):
                            os.remove(student_file)
                        for s in auth_ctrl.get_students():
                            FileHandler.save_student(student_file, s)
                        funds_ui.display_top_up_success(amount, student.get_balance())
                    else:
                        funds_ui.display_payment_cancelled()
                elif fund_choice == "2":
                    break

        elif choice == "6":
            # View Activity History
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
                if hist_choice.upper() == "CANCEL":
                    print("\nReturning to main menu.")
                    break
                elif hist_choice == "1":
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
                    if target_page == -2:
                        print("\nReturning to navigation.")
                        continue
                    if target_page != -1:
                        page = target_page
                elif hist_choice == "4":
                    break

        elif choice == "7":
            ui.display_student_logout_message()
            break


def main():
    student_file = "students.csv"

    # Initialise Core Controllers
    auth_ctrl = AuthController()
    book_ctrl = BookingController()
    room_ctrl = RoomController()
    # Link rooms list in memory to ensure synchronization between room and booking management
    room_ctrl._RoomController__rooms = book_ctrl.get_rooms()
    acct_ctrl = AccountController()
    admin_ctrl = AdminController()
    admin_ctrl.set_all_bookings(book_ctrl.get_all_bookings())
    admin_ctrl.get_equipments().append(Equipment("EQ001", 50.0))
    admin_ctrl.get_equipments().append(Equipment("EQ002", 100.0))
    payment_ctrl = PaymentController()
    payment_ctrl.set_booking_controller(book_ctrl)

    # Initialise Boundary UI components
    ui = AccountUI()
    login_ui = LoginUI()
    reg_ui = RegistrationUI()
    profile_ui = ProfileUI()
    usage_ui = UsageStatusUI()
    funds_ui = FundsUI()
    history_ui = ActivityHistoryUI()
    booking_ui = BookingUI()
    payment_ui = PaymentUI()
    deal_package_ui = DealPackageUI()

    # Load existing students from CSV into the system
    existing_students = FileHandler.load_students(student_file)
    auth_ctrl.get_students().extend(existing_students)

    # Prepopulate Test Student Accounts if not present
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

    # Prepopulate Test Admin Account if not present
    admin_email = "admin1@monash.edu"
    admins_in_system = [a.get_email() for a in auth_ctrl.get_admins()]
    if admin_email not in admins_in_system:
        test_admin = Admin(admin_email, "Password123456", "Admin", "User", "0461812562", "ADMIN001")
        auth_ctrl.get_admins().append(test_admin)

    # Prepopulate one test room inside Clayton with slot for booking demo
    if not book_ctrl.get_rooms():
        room = Room("R001", "Study Room 1", "Building A", 4, 10.0, "09:00-18:00")
        room.set_available_time_slots([
            "2026-05-06 10:00-2026-05-06 12:00"
        ])
        book_ctrl.get_rooms().append(room)

    # Unified Entry point: Authenticate first
    while True:
        ui.display_main_menu()
        choice = ui.get_menu_choice().strip()

        if choice == "1":
            # Login Flow
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
                        # Direct to complete Admin Dashboard flow
                        main_admin_menu(user, admin_ctrl, auth_ctrl, room_ctrl, book_ctrl, student_file)
                    elif role_name == "student" and isinstance(user, Student):
                        # Direct to complete Student Portal flow
                        student_menu(
                            user, book_ctrl, auth_ctrl, acct_ctrl, payment_ctrl,
                            ui, profile_ui, usage_ui, funds_ui, history_ui,
                            booking_ui, payment_ui, deal_package_ui, student_file
                        )
                    else:
                        login_ui.display_login_error()
                    break
                else:
                    login_ui.display_login_error()

        elif choice == "2":
            # Registration Flow
            while True:
                reg_ui.display_registration_header()
                first_name, last_name, student_id, phone, email, password = reg_ui.get_registration_info()

                fields = [first_name, last_name, student_id, phone, email, password]
                if any(v.upper() == "CANCEL" for v in fields):
                    print("Registration cancelled! Returning to main menu.")
                    break

                if not all(fields):
                    print("Error: All registration fields are required!")
                    continue

                if not auth_ctrl.validate_email(email):
                    print("Error: Invalid email domain! Must use @student.monash.edu!")
                    continue

                if not auth_ctrl.validate_password(password):
                    print("\nPassword Requirement Message:")
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
            sys.exit(0)
        else:
            print("Error: Invalid choice! Please select 1-3.")



if __name__ == "__main__":
    main()
