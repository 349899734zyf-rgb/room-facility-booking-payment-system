from typing import List, Optional, Dict


class RegistrationUI:
    """注册界面 (Account Management 1-3)"""
    def display_registration_form(self) -> None:
        print()
        print("=== Student Registration ===")

    def get_registration_input(self) -> Dict[str, str]: return {
        "first_name": input("First Name: ").strip(),
        "last_name": input("Last Name: ").strip(),
        "student_id": input("Student ID: ").strip(),
        "phone": input("Phone Number: ").strip(),
        "email": input("Email: ").strip(),
        "password": input("Password: ").strip()
    }

    def display_success_message(self) -> None:
        print("Registration Successful!")

    def display_error_message(self, message: str) -> None:
        print("Error: " + str(message))

    def display_invalid_email_message(self) -> None:
        print("Error: Invalid email domain! Must use @student.monash.edu!")

    def display_password_requirement_message(self) -> None:
        print()
        print("Password Requirement Message:")
        print("- Password must contain at least 8 characters.")
        print("- Must contain at least 1 uppercase letter.")
        print("- Must contain at least 1 number.")

    def display_incomplete_details_message(self) -> None:
        print("Error: All registration fields are required!")


class LoginUI:
    """登录界面 (Account Management 4, 15)"""
    def display_login_form(self) -> None:
        print()
        print("=== Account Login ===")

    def get_login_credentials(self) -> Dict[str, str]: return {
        "email": input("Enter Email: ").strip(),
        "password": input("Enter Password: ").strip()
    }

    def display_login_success(self, role: str) -> None:
        print()
        print("Login Successful! Welcome to the {} Portal!".format(role.capitalize()))

    def display_invalid_credentials_message(self) -> None:
        print("Error: Invalid email or password!")


class ProfileUI:
    """个人资料界面 (Account Management 5-7)"""
    def display_profile(self, first_name: str, last_name: str, student_id: str,
                        email: str, phone: str, balance: float) -> None:
        print()
        print("=== Student Profile Information ===")
        print("First Name:     {}".format(first_name))
        print("Last Name:      {}".format(last_name))
        print("Student ID:     {}".format(student_id))
        print("Email Address:  {}".format(email))
        print("Mobile Number:  {}".format(phone))
        print("Account Balance:${:.2f}".format(balance))
        print("-" * 35)
        print("1. Update Mobile Number")
        print("2. Change Password")
        print("3. Return to Main Menu")

    def get_new_mobile_number(self) -> str:
        print()
        print("=== Update Mobile Number ===")
        print("Type 'CANCEL' to return without saving.")
        print()
        return input("Enter New Mobile Number: ").strip()

    def get_confirm_mobile_number(self) -> str:
        return input("Confirm New Mobile Number: ").strip()

    def display_mobile_update_success(self) -> None:
        print("Update Result: Mobile number updated successfully!")

    def display_invalid_mobile_format_message(self) -> None:
        print("Error: Invalid format or mismatch! Follow the 04XXXXXXXX layout.")

    def get_password_change_input(self) -> Dict[str, str]:
        print()
        print("=== Change Account Password ===")
        print("Type 'CANCEL' at any prompt to exit.")
        print()
        return {
            "current": input("Enter Current Password: ").strip(),
            "new": input("Enter New Password: ").strip(),
            "confirm": input("Confirm New Password: ").strip()
        }

    def display_password_change_success(self) -> None:
        print("Password update result: Password updated successfully!")

    def display_password_requirement_message(self) -> None:
        print("Error: Passwords must match and contain 8+ characters, 1 uppercase and 1 number.")


class UsageStatusUI:
    """使用状态界面 (Account Management 8)"""
    def display_usage_status(self, bookings: list, ban_status: bool,
                             balance: float, deposit_status: str) -> None:
        print()
        print("=== Account Usage Status ===")

        bookings_count = len(bookings) if bookings else "None Active"
        print("Current Bookings:          {}".format(bookings_count))

        ban_text = "Banned" if ban_status else "Clear / Eligible to Book"
        print("Booking Restriction Status: {}".format(ban_text))
        print("Equipment Deposit Status:  {}".format(deposit_status))

        if balance > 0:
            print("Balance Status:            ${:.2f} (Sufficient for next booking slot)".format(balance))
        else:
            print("Balance Status:            ${:.2f} (Insufficient funds for upcoming slots)".format(balance))
        print("-" * 45)

    def display_return_option(self) -> None:
        input("Press Enter to return to the main portal...")


class ActivityHistoryUI:
    """活动历史界面 (Account Management 9-10)"""
    def display_activity_records(self, records: list) -> None: pass
    def display_record_type_legend(self) -> None: pass
    def get_page_navigation_input(self) -> str: return ""
    def display_page(self, page_num: int, total_pages: int) -> None: pass


class FundsUI:
    """资金管理界面 (Account Management 11-12, Checkout 8)"""
    def display_current_balance(self, balance: float) -> None: pass
    def get_top_up_amount(self) -> float: return 0.0
    def display_top_up_success(self, amount: float, new_balance: float) -> None: pass
    def display_invalid_amount_message(self) -> None: pass
    def display_top_up_options(self) -> None: pass


class BookingUI:
    """预定界面 (Booking Management 1, 4-5, 7-10, 12-13, 15)"""
    def display_booking_options(self) -> None: pass
    def get_search_criteria(self) -> Dict[str, str]: return {}
    def display_available_rooms(self, rooms: list) -> None: pass
    def display_no_rooms_message(self) -> None: pass
    def display_invalid_input_message(self) -> None: pass
    def get_room_selection(self) -> str: return ""
    def display_equipment_options(self) -> None: pass
    def get_equipment_choice(self) -> bool: return False
    def display_booking_limit_message(self) -> None: pass
    def display_booking_ban_info(self, bookings: list) -> None: pass
    def display_current_bookings(self, bookings: list) -> None: pass
    def display_eligibility_status(self, is_banned: bool, available_slots: int) -> None: pass
    def display_duration_rule_message(self) -> None: pass
    def display_deposit_requirement(self, amount: float) -> None: pass


class CancellationUI:
    """取消预定界面 (Booking Management 2-3, 6, 11, 14)"""
    def display_booking_list_for_cancel(self, bookings: list) -> None: pass
    def get_booking_selection(self) -> str: return ""
    def display_booking_details(self, booking: object, current_time: str) -> None: pass
    def display_late_cancellation_warning(self) -> None: pass
    def get_cancellation_confirmation(self) -> bool: return False
    def display_cancellation_result(self, cancel_type: str, refund: float) -> None: pass
    def display_booking_not_found_message(self) -> None: pass
    def display_negative_record_warning(self) -> None: pass


class PaymentUI:
    """支付界面 (Checkout 1-6, 9)"""
    def display_payment_options(self, price: float, duration: float) -> None: pass
    def get_payment_method_choice(self) -> str: return ""
    def display_balance_payment_info(self, price: float, balance: float) -> None: pass
    def display_insufficient_balance_message(self) -> None: pass
    def get_promo_code_input(self) -> str: return ""
    def display_promo_code_valid(self, new_price: float) -> None: pass
    def display_promo_code_invalid_message(self) -> None: pass
    def display_promo_code_used_message(self) -> None: pass
    def display_deal_package_info(self, duration: float, remaining: float) -> None: pass
    def display_insufficient_deal_hours_message(self) -> None: pass
    def display_equipment_restriction_message(self) -> None: pass
    def display_booking_summary(self, name: str, room: str, building: str,
                                time_period: str, price: float, equipment: bool) -> None: pass
    def display_booking_confirmed(self) -> None: pass
    def display_next_step_options(self) -> None: pass
    def get_next_step_choice(self) -> str: return ""


class DealPackageUI:
    """套餐购买界面 (Checkout 7)"""
    def display_deal_package_info(self, price: float, hours: float) -> None: pass
    def get_purchase_confirmation(self) -> bool: return False
    def display_purchase_success(self, hours: float) -> None: pass


class AdminUI:
    """管理员界面 (Account Management 14, Room Management 2)"""
    def display_admin_info(self, email: str, first_name: str,
                           last_name: str, phone: str) -> None: pass
    def display_admin_home(self) -> None: pass
    def get_promotion_idea_input(self) -> str: return ""
    def display_promotion_recorded(self) -> None: pass


class RoomManagementUI:
    """房间管理界面 (Room Management 1, 3-8)"""
    def display_room_list(self, rooms: list) -> None: pass
    def display_room_management_menu(self) -> None: pass
    def get_management_choice(self) -> str: return ""
    def get_room_details_input(self) -> Dict[str, str]: return {}
    def display_add_room_success(self) -> None: pass
    def get_room_number_input(self) -> str: return ""
    def display_remove_success(self) -> None: pass
    def display_room_not_found_message(self) -> None: pass
    def display_invalid_input_message(self) -> None: pass
    def display_current_room_details(self, room: object) -> None: pass
    def get_room_update_input(self) -> Dict[str, str]: return {}
    def display_update_success(self) -> None: pass
    def display_room_usage_status(self, booked_slots: list, predicted_income: float) -> None: pass
    def get_usage_status_input(self) -> Dict[str, str]: return {}
    def display_predicted_income(self, income: float) -> None: pass


class BookingStatusUI:
    """预定状态管理界面 (Room Management 9)"""
    def display_booking_records(self, bookings: list) -> None: pass
    def get_booking_selection(self) -> str: return ""
    def get_new_status(self) -> str: return ""
    def display_status_update_success(self) -> None: pass


class BanStudentUI:
    """学生封禁管理界面 (Room Management 10)"""
    def display_student_info(self, student_id: str, ban_status: bool) -> None: pass
    def get_student_selection(self) -> str: return ""
    def get_ban_confirmation(self) -> bool: return False
    def display_ban_success(self) -> None: pass
    def display_unban_success(self) -> None: pass
    def display_student_not_found_message(self) -> None: pass


class EquipmentDepositUI:
    """设备押金管理界面 (Room Management 11)"""
    def display_current_deposit(self, equipment_id: str, amount: float) -> None: pass
    def get_deposit_amount_input(self) -> float: return 0.0
    def get_deposit_confirmation(self) -> bool: return False
    def display_deposit_set_success(self, amount: float) -> None: pass
    def display_deposit_refund_success(self, amount: float) -> None: pass
    def display_invalid_amount_message(self) -> None: pass
