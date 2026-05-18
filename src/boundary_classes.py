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
    def __init__(self, admin_controller):
        self.admin_controller = admin_controller

    def display_admin_info(self, email: str, first_name: str,
                           last_name: str, phone: str) -> None:
        """Display admin information"""
        print("\n" + "=" * 80)
        print(" " * 25 + "ADMIN INFORMATION")
        print("=" * 80)
        print(f"Email:      {email}")
        print(f"First Name: {first_name}")
        print(f"Last Name:  {last_name}")
        print(f"Phone:      {phone}")
        print("=" * 80)

    def display_admin_home(self) -> None:
        """Display admin home screen"""
        print("\n" + "=" * 80)
        print(" " * 20 + "WELCOME TO ADMIN HOME")
        print("=" * 80)
        print("1. Room Management")
        print("2. Student Management")
        print("3. System Settings")
        print("4. View Reports")
        print("5. Logout")
        print("=" * 80)

    def get_promotion_idea_input(self) -> str:
        """Get promotion idea input from admin (Story 2.2)"""
        print("\n" + "-" * 80)
        print(" " * 20 + "RECORD PROMOTION IDEA")
        print("-" * 80)

        idea = input("Enter your promotion idea: ").strip()

        if not idea:
            print("Error: Promotion idea cannot be empty")
            return ""

        return idea

    def display_promotion_recorded(self) -> None:
        """Display confirmation that promotion idea was recorded"""
        print("\nSuccess: Promotion idea recorded successfully!")






class RoomManagementUI:
    class RoomManagementUI:
        """Room Management User Interface for administrators"""

    def __init__(self, room_controller, admin_controller=None):
        """Initialize RoomManagementUI with controllers"""
        self.room_controller = room_controller
        self.admin_controller = admin_controller

    # ==================== Story 2.3: View Room Management Menu ====================

    def display_room_management_menu(self) -> None:
        """Display the room management menu"""
        print("\n" + "=" * 80)
        print(" " * 20 + "ROOM MANAGEMENT MENU")
        print("=" * 80)
        print("1.  Add a New Room (Story 2.1)")
        print("2.  Record Promotion Idea (Story 2.2)")
        print("3.  View All Rooms")
        print("4.  Delete a Room (Story 2.4)")
        print("5.  Update Room Status - Student Presence & Equipment (Story 2.5)")
        print("6.  Update Available Time Slots (Story 2.6)")
        print("7.  View Predicted Income (Story 2.7)")
        print("8.  Change Room Information (Story 2.8)")
        print("9.  Return to Main Menu")
        print("=" * 80)

    def get_management_choice(self) -> str:
        """Get the user's menu choice"""
        return input("Please select an option (1-9): ").strip()

    def display_room_list(self, rooms: list) -> None:
        """Display all rooms in a formatted table"""
        if not rooms:
            print("\nNo rooms available")
            return

        print("\n" + "=" * 150)
        print(" " * 50 + "ROOM LIST")
        print("=" * 150)
        print(f"{'Room ID':<12} {'Room Name':<20} {'Building':<15} {'Capacity':<10} "
              f"{'Price/Hour':<12} {'Hours':<20} {'Student In':<12} {'Equipment':<12}")
        print("-" * 150)

        for room in rooms:
            student_status = 'Yes' if room.is_student_in_room() else 'No'
            equipment_status = 'Yes' if room.is_equipment_rented() else 'No'
            print(f"{room.get_room_id():<12} {room.get_room_name():<20} "
                  f"{room.get_building():<15} {room.get_capacity():<10} "
                  f"${room.get_price_per_hour():<11.2f} {room.get_opening_hours():<20} "
                  f"{student_status:<12} {equipment_status:<12}")

        print("=" * 150)

    # ==================== Story 2.1: Add a New Room ====================

    def get_room_details_input(self) -> Optional[Dict[str, str]]:
        """Get new room details from user input"""
        print("\n" + "-" * 80)
        print(" " * 25 + "ADD NEW ROOM")
        print("-" * 80)

        try:
            name = input("Enter room name: ").strip()
            if not name:
                print("Error: Room name cannot be empty")
                return None

            building = input("Enter building: ").strip()
            if not building:
                print("Error: Building cannot be empty")
                return None

            capacity_str = input("Enter capacity (number of students): ").strip()
            if not capacity_str:
                print("Error: Capacity cannot be empty")
                return None

            try:
                capacity = int(capacity_str)
                if capacity <= 0:
                    print("Error: Capacity must be greater than 0")
                    return None
            except ValueError:
                print("Error: Capacity must be a valid number")
                return None

            price_str = input("Enter price per hour ($): ").strip()
            if not price_str:
                print("Error: Price cannot be empty")
                return None

            try:
                price = float(price_str)
                if price <= 0:
                    print("Error: Price must be greater than 0")
                    return None
            except ValueError:
                print("Error: Price must be a valid number")
                return None

            opening_hours = input("Enter opening hours (e.g., 09:00-17:00): ").strip()
            if not opening_hours:
                print("Error: Opening hours cannot be empty")
                return None

            return {
                'name': name,
                'building': building,
                'capacity': str(capacity),
                'price': str(price),
                'opening_hours': opening_hours
            }

        except Exception as e:
            print(f"Error: {e}")
            return None

    def display_add_room_success(self) -> None:
        """Display success message when room is added"""
        print("\nSuccess: Room added successfully!")

    def display_invalid_input_message(self) -> None:
        """Display invalid input error message"""
        print("\nError: Invalid input. Please try again.")

    # ==================== Story 2.2: Record Promotion Idea ====================

    def get_promotion_idea_input(self) -> Optional[str]:
        """Get promotion idea from user"""
        print("\n" + "-" * 80)
        print(" " * 20 + "RECORD PROMOTION IDEA")
        print("-" * 80)

        idea = input("Enter promotion idea: ").strip()
        if not idea:
            print("Error: Promotion idea cannot be empty")
            return None

        return idea

    def display_promotion_recorded(self) -> None:
        """Display success message when promotion idea is recorded"""
        print("\nSuccess: Promotion idea recorded successfully!")

    # ==================== Story 2.4: Remove a Room ====================

    def get_room_number_input(self) -> str:
        """Get room ID input from user"""
        return input("Enter room ID (e.g., RM0001): ").strip()

    def display_remove_success(self) -> None:
        """Display success message when room is deleted"""
        print("\nSuccess: Room deleted successfully!")

    def display_room_not_found_message(self) -> None:
        """Display error message when room is not found"""
        print("\nError: Room not found. Please check the room ID.")

    # ==================== Story 2.5: Record Student Presence & Equipment ====================

    def get_usage_status_input(self) -> Optional[Dict[str, bool]]:
        """Get room usage status input from user"""
        print("\n" + "-" * 80)
        print(" " * 20 + "UPDATE ROOM STATUS (STUDENT & EQUIPMENT)")
        print("-" * 80)

        try:
            student_input = input("Is there a student in the room? (y/n): ").strip().lower()
            is_student_in = student_input in ['y', 'yes', 'true', '1']

            equipment_input = input("Is equipment rented? (y/n): ").strip().lower()
            is_equipment_rented = equipment_input in ['y', 'yes', 'true', '1']

            return {
                'is_student_in': is_student_in,
                'is_equipment_rented': is_equipment_rented
            }
        except Exception:
            print("Error: Input error occurred")
            return None

    def display_room_usage_status(self, booked_slots: list, predicted_income: float) -> None:
        """Display room usage status"""
        print("\n" + "-" * 80)
        print(" " * 25 + "ROOM USAGE STATUS")
        print("-" * 80)
        print(f"Available Time Slots: {len(booked_slots)}")

        if booked_slots:
            print("Time Slots:")
            for i, slot in enumerate(booked_slots, 1):
                print(f"  {i}. {slot}")
        else:
            print("  (No time slots available)")

        print(f"\nPredicted Income: ${predicted_income:.2f}")
        print("-" * 80)

    # ==================== Story 2.6: Update Time Slots ====================

    def get_time_slots_input(self) -> Optional[List[str]]:
        """Get time slots input from user"""
        print("\n" + "-" * 80)
        print(" " * 20 + "UPDATE AVAILABLE TIME SLOTS")
        print("-" * 80)
        print("Enter time slots (format: 09:00-10:00), one per line")
        print("Enter blank line to finish")

        time_slots = []
        while True:
            slot = input("Time slot: ").strip()

            if not slot:
                break

            if '-' not in slot:
                print("Error: Format should be HH:MM-HH:MM (e.g., 09:00-10:00)")
                continue

            parts = slot.split('-')
            if len(parts) != 2:
                print("Error: Format should be HH:MM-HH:MM")
                continue

            try:
                start_time, end_time = parts[0].strip(), parts[1].strip()
                if ':' not in start_time or ':' not in end_time:
                    print("Error: Format should be HH:MM-HH:MM")
                    continue

                time_slots.append(f"{start_time}-{end_time}")
            except Exception:
                print("Error: Format should be HH:MM-HH:MM")
                continue

        if not time_slots:
            print("Error: Please enter at least one time slot")
            return None

        return time_slots

    def display_available_time_slots(self, room) -> None:
        """Display available time slots for a room"""
        slots = room.get_available_time_slots()
        print(f"\nRoom {room.get_room_id()} available time slots:")

        if not slots:
            print("  (No time slots available)")
        else:
            for i, slot in enumerate(slots, 1):
                print(f"  {i}. {slot}")

    # ==================== Story 2.7: View Predicted Income ====================

    def display_predicted_income(self, income: float) -> None:
        """Display predicted income for a room"""
        print("\n" + "-" * 80)
        print(" " * 25 + "PREDICTED INCOME")
        print("-" * 80)
        print(f"Predicted Income: ${income:.2f}")
        print("-" * 80)

    # ==================== Story 2.8: Change Room Information ====================

    def display_current_room_details(self, room) -> None:
        """Display current room information"""
        print("\n" + "-" * 80)
        print(" " * 20 + "CURRENT ROOM INFORMATION")
        print("-" * 80)
        print(f"Room ID:        {room.get_room_id()}")
        print(f"Room Name:      {room.get_room_name()}")
        print(f"Building:       {room.get_building()}")
        print(f"Capacity:       {room.get_capacity()} students")
        print(f"Price:          ${room.get_price_per_hour():.2f}/hour")
        print(f"Opening Hours:  {room.get_opening_hours()}")
        student_in = 'Yes' if room.is_student_in_room() else 'No'
        equipment = 'Yes' if room.is_equipment_rented() else 'No'
        print(f"Student In:     {student_in}")
        print(f"Equipment:      {equipment}")
        print("-" * 80)

    def get_room_update_input(self) -> Optional[Dict[str, str]]:
        """Get room update information from user"""
        print("\nEnter information to update (leave blank to skip)")
        print("-" * 80)

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
                    print("Error: Capacity must be greater than 0")
                    return None
                updates['capacity'] = capacity
            except ValueError:
                print("Error: Capacity must be an integer")
                return None

        price_str = input("New price: ").strip()
        if price_str:
            try:
                price = float(price_str)
                if price <= 0:
                    print("Error: Price must be greater than 0")
                    return None
                updates['price'] = price
            except ValueError:
                print("Error: Price must be a valid number")
                return None

        opening_hours = input("New opening hours: ").strip()
        if opening_hours:
            updates['opening_hours'] = opening_hours

        if not updates:
            print("Error: No information entered to update")
            return None

        return updates

    def display_update_success(self) -> None:
        """Display success message when room is updated"""
        print("\nSuccess: Room information updated successfully!")

    def display_update_failure(self) -> None:
        """Display failure message when room update fails"""
        print("\nError: Failed to update room information")


class BookingStatusUI:

        """Booking Status Management Interface (Room Management 9)"""

    def __init__(self, booking_controller):
        self.booking_controller = booking_controller

    def display_booking_records(self, bookings: list) -> None:
        """Display all booking records"""
        if not bookings:
            print("\nNo booking records found")
            return

        print("\n" + "=" * 150)
        print(" " * 50 + "BOOKING RECORDS")
        print("=" * 150)
        print(f"{'Booking ID':<15} {'Student ID':<15} {'Room ID':<15} {'Status':<15} {'Date':<15}")
        print("-" * 150)

        for booking in bookings:
            print(f"{booking.get_booking_id():<15} {booking.get_student_id():<15} "
                  f"{booking.get_room_id():<15} {booking.get_status():<15} "
                  f"{booking.get_date():<15}")

        print("=" * 150)

    def get_booking_selection(self) -> str:
        """Get booking selection from user"""
        print("\n" + "-" * 80)
        print(" " * 25 + "SELECT BOOKING TO UPDATE")
        print("-" * 80)
        return input("Enter booking ID: ").strip()

    def display_booking_details(self, booking) -> None:
        """Display booking details"""
        print("\n" + "-" * 80)
        print("Booking Details:")
        print(f"  Booking ID: {booking.get_booking_id()}")
        print(f"  Student ID: {booking.get_student_id()}")
        print(f"  Room ID: {booking.get_room_id()}")
        print(f"  Current Status: {booking.get_status()}")
        print(f"  Date: {booking.get_date()}")
        print("-" * 80)

    def get_new_status(self) -> str:
        """Get new booking status from user"""
        print("\nAvailable statuses:")
        print("1. Pending")
        print("2. Confirmed")
        print("3. Completed")
        print("4. Cancelled")

        choice = input("Select new status (1-4): ").strip()

        status_map = {
            '1': 'Pending',
            '2': 'Confirmed',
            '3': 'Completed',
            '4': 'Cancelled'
        }

        return status_map.get(choice, "")

    def display_status_update_success(self) -> None:
        """Display status update success message"""
        print("\nSuccess: Booking status updated successfully!")


class BanStudentUI:
        """Student Ban Management Interface (Room Management 10)"""

    def __init__(self, admin_controller):
        self.admin_controller = admin_controller

    def display_students(self, students: list) -> None:
        """Display all students"""
        if not students:
            print("\nNo students found")
            return

        print("\n" + "=" * 120)
        print(" " * 45 + "STUDENT LIST")
        print("=" * 120)
        print(f"{'Student ID':<15} {'Name':<20} {'Email':<30} {'Status':<15}")
        print("-" * 120)

        for student in students:
            status = "BANNED" if student.is_banned() else "ACTIVE"
            print(f"{student.get_student_id():<15} {student.get_name():<20} "
                  f"{student.get_email():<30} {status:<15}")

        print("=" * 120)

    def get_student_selection(self) -> str:
        """Get student selection from user"""
        print("\n" + "-" * 80)
        print(" " * 25 + "SELECT STUDENT")
        print("-" * 80)
        return input("Enter student ID: ").strip()

    def display_student_info(self, student_id: str, ban_status: bool) -> None:
        """Display student information"""
        print("\n" + "-" * 80)
        print("Student Information:")
        print(f"  Student ID: {student_id}")
        status = "BANNED" if ban_status else "ACTIVE"
        print(f"  Status: {status}")
        print("-" * 80)

    def get_ban_confirmation(self) -> bool:
        """Get ban confirmation from user"""
        confirm = input("\nAre you sure you want to ban this student? (y/n): ").strip().lower()
        return confirm in ['y', 'yes']

    def get_unban_confirmation(self) -> bool:
        """Get unban confirmation from user"""
        confirm = input("\nAre you sure you want to unban this student? (y/n): ").strip().lower()
        return confirm in ['y', 'yes']

    def display_ban_success(self) -> None:
        """Display ban success message"""
        print("\nSuccess: Student banned successfully!")

    def display_unban_success(self) -> None:
        """Display unban success message"""
        print("\nSuccess: Student unbanned successfully!")

    def display_student_not_found_message(self) -> None:
        """Display student not found message"""
        print("\nError: Student not found")



class EquipmentDepositUI:
    """Equipment Deposit User Interface - Story 2.11: Set Equipment Deposit"""
   
    def __init__(self, admin_controller):
        self.admin_controller = admin_controller

    def display_equipment_list(self, equipments: list) -> None:
        """Display all equipment"""
        if not equipments:
            print("\nNo equipment found")
            return

        print("\n" + "=" * 120)
        print(" " * 45 + "EQUIPMENT LIST")
        print("=" * 120)
        print(f"{'Equipment ID':<15} {'Name':<20} {'Current Deposit':<20} {'Category':<20}")
        print("-" * 120)

        for equipment in equipments:
            deposit = equipment.get_deposit_amount()
            print(f"{equipment.get_equipment_id():<15} {equipment.get_name():<20} "
                  f"${deposit:<19.2f} {equipment.get_category():<20}")

        print("=" * 120)

    def get_equipment_selection(self) -> str:
        """Get equipment selection from user"""
        print("\n" + "-" * 80)
        print(" " * 25 + "SELECT EQUIPMENT")
        print("-" * 80)
        return input("Enter equipment ID: ").strip()

    def display_current_deposit(self, equipment_id: str, amount: float) -> None:
        """Display current deposit information"""
        print("\n" + "-" * 80)
        print("Current Deposit Information:")
        print(f"  Equipment ID: {equipment_id}")
        print(f"  Current Deposit: ${amount:.2f}")
        print("-" * 80)

    def get_deposit_amount_input(self) -> float:
        """Get deposit amount input from user"""
        print("\n" + "-" * 80)
        print(" " * 20 + "SET EQUIPMENT DEPOSIT AMOUNT")
        print("-" * 80)

        try:
            amount_str = input("Enter deposit amount ($): ").strip()

            if not amount_str:
                print("Error: Deposit amount cannot be empty")
                return 0.0

            amount = float(amount_str)

            if amount < 0:
                print("Error: Deposit amount cannot be negative")
                return 0.0

            return amount

        except ValueError:
            print("Error: Please enter a valid number")
            return 0.0

    def get_deposit_confirmation(self) -> bool:
        """Get deposit confirmation from user"""
        confirm = input("\nConfirm setting this deposit amount? (y/n): ").strip().lower()
        return confirm in ['y', 'yes']

    def display_deposit_set_success(self, amount: float) -> None:
        """Display deposit set success message"""
        print(f"\nSuccess: Equipment deposit amount set to ${amount:.2f} successfully!")

    def display_deposit_refund_success(self, amount: float) -> None:
        """Display deposit refund success message"""
        print(f"\nSuccess: Equipment deposit of ${amount:.2f} refunded successfully!")

    def display_invalid_amount_message(self) -> None:
        """Display invalid amount message"""
        print("\nError: Invalid deposit amount. Please try again.")


