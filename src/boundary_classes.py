from typing import List, Optional, Dict


class RegistrationUI:
    """注册界面 (Account Management 1-3)"""
    def display_registration_form(self) -> None: pass
    def get_registration_input(self) -> Dict[str, str]: return {}
    def display_success_message(self) -> None: pass
    def display_error_message(self, message: str) -> None: pass
    def display_invalid_email_message(self) -> None: pass
    def display_password_requirement_message(self) -> None: pass
    def display_incomplete_details_message(self) -> None: pass


class LoginUI:
    """登录界面 (Account Management 4, 15)"""
    def display_login_form(self) -> None: pass
    def get_login_credentials(self) -> Dict[str, str]: return {}
    def display_login_success(self, role: str) -> None: pass
    def display_invalid_credentials_message(self) -> None: pass


class ProfileUI:
    """个人资料界面 (Account Management 5-7)"""
    def display_profile(self, first_name: str, last_name: str, student_id: str,
                        email: str, phone: str, balance: float) -> None: pass
    def get_new_mobile_number(self) -> str: return ""
    def get_confirm_mobile_number(self) -> str: return ""
    def display_mobile_update_success(self) -> None: pass
    def display_invalid_mobile_format_message(self) -> None: pass
    def get_password_change_input(self) -> Dict[str, str]: return {}
    def display_password_change_success(self) -> None: pass
    def display_password_requirement_message(self) -> None: pass


class UsageStatusUI:
    """使用状态界面 (Account Management 8)"""
    def display_usage_status(self, bookings: list, ban_status: bool,
                             balance: float, deposit_status: str) -> None: pass
    def display_return_option(self) -> None: pass


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
    """Room Management UI (Room Management 1, 3-8)"""

    def __init__(self, room_controller: 'RoomController') -> None:
        """Initialize UI with room controller"""
        self.room_controller = room_controller

    def display_room_list(self, rooms: list) -> None:
        """Display all rooms in a table format"""
        if not rooms:
            print("\n❌ No rooms available")
            return

        print("\n" + "="*120)
        print("                                             Room List")
        print("="*120)
        print(f"{'Room ID':<12} {'Room Name':<15} {'Building':<12} {'Capacity':<10} {'Price':<12} {'Hours':<15}")
        print("-"*120)

        for room in rooms:
            print(f"{room.get_room_id():<12} {room.get_room_name():<15} "
                  f"{room.get_building():<12} {room.get_capacity():<10} "
                  f"${room.get_price_per_hour():<11.2f} {room.get_opening_hours():<15}")

        print("="*120)

    def display_room_management_menu(self) -> None:
        """Display room management menu"""
        print("\n" + "="*60)
        print("                    Room Management Menu")
        print("="*60)
        print("1. Add New Room")
        print("2. View All Rooms")
        print("3. Delete Room")
        print("4. Update Room Information")
        print("5. Update Room Status (Student/Equipment)")
        print("6. Update Available Time Slots")
        print("7. View Room Predicted Income")
        print("8. Return to Main Menu")
        print("="*60)

    def get_management_choice(self) -> str:
        """Get user menu choice"""
        return input("Please select an option (1-8): ").strip()

    def get_room_details_input(self) -> Dict[str, str]:
        """Get room details input for adding new room"""
        print("\n" + "="*60)
        print("                    Add New Room")
        print("="*60)

        try:
            room_name = input("Room Name (e.g., Study Room A): ").strip()
            if not room_name:
                print("❌ Room name cannot be empty")
                return {}

            building = input("Building (e.g., Building A): ").strip()
            if not building:
                print("❌ Building cannot be empty")
                return {}

            capacity_str = input("Capacity (number of students): ").strip()
            try:
                capacity = int(capacity_str)
                if capacity <= 0:
                    print("❌ Capacity must be greater than 0")
                    return {}
            except ValueError:
                print("❌ Capacity must be an integer")
                return {}

            price_str = input("Price per hour (e.g., 25.0): ").strip()
            try:
                price = float(price_str)
                if price <= 0:
                    print("❌ Price must be greater than 0")
                    return {}
            except ValueError:
                print("❌ Price must be a number")
                return {}

            opening_hours = input("Opening Hours (e.g., 9:00-18:00): ").strip()
            if not opening_hours:
                print("❌ Opening hours cannot be empty")
                return {}

            return {
                'name': room_name,
                'building': building,
                'capacity': str(capacity),
                'price': str(price),
                'opening_hours': opening_hours
            }

        except Exception as e:
            print(f"❌ Input error: {str(e)}")
            return {}

    def display_add_room_success(self) -> None:
        """Display room added successfully message"""
        print("\n✅ Room added successfully!")

    def get_room_number_input(self) -> str:
        """Get room ID input"""
        return input("\nEnter room ID (e.g., RM0001): ").strip()

    def display_remove_success(self) -> None:
        """Display room deleted successfully message"""
        print("\n✅ Room deleted successfully")

    def display_room_not_found_message(self) -> None:
        """Display room not found message"""
        print("\n❌ Room not found")

    def display_invalid_input_message(self) -> None:
        """Display invalid input message"""
        print("\n❌ Invalid input")

    def display_current_room_details(self, room: object) -> None:
        """Display current room information"""
        print("\n" + "-"*60)
        print("                  Current Room Information")
        print("-"*60)
        print(f"Room ID:        {room.get_room_id()}")
        print(f"Room Name:      {room.get_room_name()}")
        print(f"Building:       {room.get_building()}")
        print(f"Capacity:       {room.get_capacity()} students")
        print(f"Price:          ${room.get_price_per_hour():.2f}/hour")
        print(f"Opening Hours:  {room.get_opening_hours()}")
        print("-"*60)

    def get_room_update_input(self) -> Dict[str, str]:
        """Get room information to update"""
        print("\nEnter information to update (leave blank to skip)")

        updates = {}

        room_name = input("New room name: ").strip()
        if room_name:
            updates['name'] = room_name

        building = input("New building: ").strip()
        if building:
            updates['building'] = building

        capacity_str = input("New capacity: ").strip()
        if capacity_str:
            try:
                capacity = int(capacity_str)
                if capacity <= 0:
                    print("❌ Capacity must be greater than 0")
                    return {}
                updates['capacity'] = str(capacity)
            except ValueError:
                print("❌ Capacity must be an integer")
                return {}

        price_str = input("New price: ").strip()
        if price_str:
            try:
                price = float(price_str)
                if price <= 0:
                    print("❌ Price must be greater than 0")
                    return {}
                updates['price'] = str(price)
            except ValueError:
                print("❌ Price must be a number")
                return {}

        opening_hours = input("New opening hours: ").strip()
        if opening_hours:
            updates['opening_hours'] = opening_hours

        if not updates:
            print("❌ No information entered to update")
            return {}

        return updates

    def display_update_success(self) -> None:
        """Display room updated successfully message"""
        print("\n✅ Room information updated successfully")

    def display_room_usage_status(self, booked_slots: list, predicted_income: float) -> None:
        """Display room usage status with booked slots and predicted income"""
        print("\n" + "-"*60)
        print("                  Room Usage Status")
        print("-"*60)
        print(f"Available Time Slots: {len(booked_slots)}")

        if booked_slots:
            print("Time Slots:")
            for i, slot in enumerate(booked_slots, 1):
                print(f"  {i}. {slot}")
        else:
            print("  (No time slots available)")

        print(f"Predicted Income: ${predicted_income:.2f}")
        print("-"*60)

    def get_usage_status_input(self) -> Dict[str, str]:
        """Get room usage status input"""
        print("\n" + "-"*60)
        print("                  Update Room Status")
        print("-"*60)

        try:
            student_input = input("Is there a student in the room? (y/n): ").strip().lower()
            is_student_in = 'y' if student_input in ['y', 'yes'] else 'n'

            equipment_input = input("Is equipment rented? (y/n): ").strip().lower()
            is_equipment_rented = 'y' if equipment_input in ['y', 'yes'] else 'n'

            return {
                'is_student_in': is_student_in,
                'is_equipment_rented': is_equipment_rented
            }
        except Exception:
            print("❌ Input error")
            return {}

    def display_predicted_income(self, income: float) -> None:
        """Display room predicted income"""
        print("\n" + "-"*60)
        print("                  Predicted Income")
        print("-"*60)
        print(f"Predicted Income: ${income:.2f}")
        print("-"*60)

    def pause(self) -> None:
        """Pause and wait for user to press Enter"""
        input("\nPress Enter to continue...")



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
