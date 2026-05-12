"""
MSSRB - Feature 1: Customer Registration, Login, and Account Management
Covers: Acct 1 ~ Acct 15
Contains: <<Entity>> User, Student, Admin, ActivityRecord
          <<Controller>> AuthController, AccountController
          <<Boundary>> AuthUI, StudentMenuUI
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict


# ================================================================
# <<Entity>> Section
# ================================================================

class User(ABC):
    """Abstract base class representing a system user.
    Provides shared attributes (email, password, name, phone)
    and authentication support for both Student and Admin roles.
    Referenced by: Acct 1-15
    """

    def __init__(self, email: str, password: str, first_name: str,
                 last_name: str, phone: str) -> None:
        self.__email: str = email
        self.__password: str = password
        self.__first_name: str = first_name
        self.__last_name: str = last_name
        self.__phone: str = phone

    # --- Accessors ---
    def get_email(self) -> str:
        return self.__email

    def get_password(self) -> str:
        return self.__password

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def get_phone(self) -> str:
        return self.__phone

    # --- Mutators ---
    def set_email(self, email: str) -> None:
        self.__email = email

    def set_password(self, password: str) -> None:
        self.__password = password

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = first_name

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = last_name

    def set_phone(self, phone: str) -> None:
        self.__phone = phone

    # --- Business Methods ---
    @abstractmethod
    def get_role(self) -> str:
        """Return the role string ('student' or 'admin').
        Acct 13: Used for role-based menu access.
        """
        pass

    def verify_password(self, input_password: str) -> bool:
        """Verify the given password against the stored password.
        Acct 4 / Acct 15: Used during login authentication.
        """
        return self.__password == input_password

    def __str__(self) -> str:
        return f"User({self.__email}, {self.__first_name} {self.__last_name})"


class ActivityRecord:
    """Activity record entity class.
    Records date, type, details, and amount for student activity history.
    Types: booking, recharge, late_cancellation, no_show, cancellation.
    Referenced by: Acct 9, Acct 10
    """

    def __init__(self, date: datetime, record_type: str,
                 details: str, amount: float) -> None:
        self.__date: datetime = date
        self.__record_type: str = record_type
        self.__details: str = details
        self.__amount: float = amount

    # --- Accessors ---
    def get_date(self) -> datetime:
        return self.__date

    def get_record_type(self) -> str:
        return self.__record_type

    def get_details(self) -> str:
        return self.__details

    def get_amount(self) -> float:
        return self.__amount

    def __str__(self) -> str:
        return (f"[{self.__date.strftime('%Y-%m-%d %H:%M')}] "
                f"{self.__record_type.upper():20s} | "
                f"{self.__details} | ${self.__amount:.2f}")


class Student(User):
    """Student entity class.
    Stores account balance, booking list, activity history,
    ban status, deal package hours, and promo code usage.
    Referenced by: Acct 1-13, Book 1-15, Check 1-11
    """

    def __init__(self, email: str, password: str, first_name: str,
                 last_name: str, phone: str, student_id: str) -> None:
        super().__init__(email, password, first_name, last_name, phone)
        self.__student_id: str = student_id
        self.__balance: float = 0.0
        self.__booking_ban_status: bool = False
        self.__late_cancellation_count: int = 0
        self.__no_show_count: int = 0
        self.__deal_package_hours: float = 0.0
        self.__bookings: List = []
        self.__activity_history: List[ActivityRecord] = []
        self.__used_promo_codes: List[str] = []

    # --- Accessors ---
    def get_student_id(self) -> str:
        return self.__student_id

    def get_balance(self) -> float:
        return self.__balance

    def get_booking_ban_status(self) -> bool:
        return self.__booking_ban_status

    def get_late_cancellation_count(self) -> int:
        return self.__late_cancellation_count

    def get_no_show_count(self) -> int:
        return self.__no_show_count

    def get_deal_package_hours(self) -> float:
        return self.__deal_package_hours

    def get_bookings(self) -> List:
        return self.__bookings

    def get_activity_history(self) -> List[ActivityRecord]:
        return self.__activity_history

    def get_used_promo_codes(self) -> List[str]:
        return self.__used_promo_codes

    # --- Mutators ---
    def set_student_id(self, student_id: str) -> None:
        self.__student_id = student_id

    def set_balance(self, balance: float) -> None:
        self.__balance = balance

    def set_booking_ban_status(self, status: bool) -> None:
        self.__booking_ban_status = status

    def set_late_cancellation_count(self, count: int) -> None:
        self.__late_cancellation_count = count

    def set_no_show_count(self, count: int) -> None:
        self.__no_show_count = count

    def set_deal_package_hours(self, hours: float) -> None:
        self.__deal_package_hours = hours

    # --- Business Methods ---
    def get_role(self) -> str:
        """Return 'student'. Acct 13: Role Recognition."""
        return "student"

    def add_funds(self, amount: float) -> bool:
        """Add funds to the student's account balance.
        Acct 12: Amount must be positive; records a 'recharge' activity.
        """
        if amount <= 0:
            return False
        self.__balance += amount
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "recharge",
                           f"Added ${amount:.2f}", amount))
        return True

    def deduct_balance(self, amount: float) -> bool:
        """Deduct the specified amount from account balance.
        Check 2: Returns True if sufficient balance.
        """
        if self.__balance >= amount:
            self.__balance -= amount
            return True
        return False

    def is_eligible_to_book(self) -> bool:
        """Check if the student is eligible to make a booking.
        Book 7: Returns False if currently banned.
        """
        return not self.__booking_ban_status

    def has_reached_booking_limit(self) -> bool:
        """Check if the student has reached max booking limit.
        Book 10: Maximum 3 active (confirmed) bookings allowed.
        """
        active = [b for b in self.__bookings if b.get_status() == "confirmed"]
        return len(active) >= 3

    def add_booking(self, booking) -> None:
        """Add a booking to the student's list.
        Book 5/15: Also records a 'booking' activity in history.
        """
        self.__bookings.append(booking)
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "booking",
                           f"Booked {booking.get_room().get_room_name()}",
                           booking.get_total_price()))

    def remove_booking(self, booking) -> None:
        """Remove a booking after cancellation. Book 2/6."""
        if booking in self.__bookings:
            self.__bookings.remove(booking)

    def record_late_cancellation(self) -> None:
        """Record a late cancellation and check ban threshold.
        Book 3: If total (late + no-show) >= 3, student is banned.
        """
        self.__late_cancellation_count += 1
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "late_cancellation",
                           "Late cancellation recorded", 0.0))
        self._check_ban_threshold()

    def record_no_show(self) -> None:
        """Record a no-show event and check ban threshold."""
        self.__no_show_count += 1
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "no_show",
                           "No-show recorded", 0.0))
        self._check_ban_threshold()

    def _check_ban_threshold(self) -> None:
        """Automatically ban if late_cancel + no_show >= 3.
        Book 3 / Room 10.
        """
        if (self.__late_cancellation_count + self.__no_show_count) >= 3:
            self.__booking_ban_status = True

    def add_deal_package_hours(self, hours: float) -> None:
        """Add deal package hours. Check 7: $100 → 12 hours."""
        self.__deal_package_hours += hours

    def deduct_deal_package_hours(self, hours: float) -> bool:
        """Deduct hours from deal package. Check 5."""
        if self.__deal_package_hours >= hours:
            self.__deal_package_hours -= hours
            return True
        return False

    def has_used_promo_code(self, code: str) -> bool:
        """Check 4: Each promo code single-use per student."""
        return code in self.__used_promo_codes

    def mark_promo_code_used(self, code: str) -> None:
        """Check 4: Mark promo code as used."""
        self.__used_promo_codes.append(code)

    def get_active_bookings(self) -> List:
        """Return confirmed bookings. Book 11-13."""
        return [b for b in self.__bookings if b.get_status() == "confirmed"]

    def get_activity_history_page(self, page: int,
                                  page_size: int = 10) -> List[ActivityRecord]:
        """Return a single page of activity history.
        Acct 10: Pagination support (default 10 per page).
        """
        start = (page - 1) * page_size
        end = start + page_size
        return self.__activity_history[start:end]

    def get_total_history_pages(self, page_size: int = 10) -> int:
        """Calculate total number of history pages."""
        total = len(self.__activity_history)
        return max(1, (total + page_size - 1) // page_size)


class Admin(User):
    """Administrator entity class.
    Has permissions for room management, booking status updates,
    student banning, and equipment deposit management.
    Referenced by: Acct 14-15, Room 1-11
    """

    def __init__(self, email: str, password: str, first_name: str,
                 last_name: str, phone: str, admin_id: str) -> None:
        super().__init__(email, password, first_name, last_name, phone)
        self.__admin_id: str = admin_id
        self.__promotion_ideas: List[str] = []

    # --- Accessors ---
    def get_admin_id(self) -> str:
        return self.__admin_id

    def get_promotion_ideas(self) -> List[str]:
        return self.__promotion_ideas

    # --- Mutators ---
    def set_admin_id(self, admin_id: str) -> None:
        self.__admin_id = admin_id

    # --- Business Methods ---
    def get_role(self) -> str:
        """Return 'admin'. Acct 13: Role Recognition."""
        return "admin"

    def record_promotion_idea(self, idea: str) -> bool:
        """Record a promotion idea. Room 2: Must be non-empty."""
        if idea.strip():
            self.__promotion_ideas.append(idea.strip())
            return True
        return False


# ================================================================
# <<Controller>> Section
# ================================================================

class AuthController:
    """Authentication and registration controller.
    Handles: Acct 1 (Register), Acct 2 (Email), Acct 3 (Password),
             Acct 4 (Login), Acct 6 (Mobile), Acct 7 (Change Pwd),
             Acct 13 (Role), Acct 15 (Admin Login)
    """

    def __init__(self) -> None:
        self.__students: List[Student] = []
        self.__admins: List[Admin] = []

    def get_students(self) -> List[Student]:
        return self.__students

    def get_admins(self) -> List[Admin]:
        return self.__admins

    def validate_email(self, email: str) -> bool:
        """Acct 2: Email must end with '@student.monash.edu'."""
        return email.endswith("@student.monash.edu")

    def validate_password(self, password: str) -> bool:
        """Acct 3: >= 8 chars, at least one uppercase and one digit."""
        if len(password) < 8:
            return False
        return any(c.isupper() for c in password) and any(c.isdigit() for c in password)

    def validate_mobile(self, mobile: str) -> bool:
        """Acct 6: Exactly 10 digits starting with '04'."""
        return len(mobile) == 10 and mobile.startswith("04") and mobile.isdigit()

    def register_student(self, email: str, password: str, first_name: str,
                         last_name: str, phone: str,
                         student_id: str) -> Optional[Student]:
        """Acct 1: Register a new student account.
        All fields non-empty, valid email, valid password, valid mobile.
        """
        if not all([email.strip(), password.strip(), first_name.strip(),
                    last_name.strip(), phone.strip(), student_id.strip()]):
            return None
        if not self.validate_email(email):
            return None
        if not self.validate_password(password):
            return None
        if not self.validate_mobile(phone):
            return None
        for s in self.__students:
            if s.get_email() == email:
                return None
        student = Student(email, password, first_name, last_name, phone, student_id)
        self.__students.append(student)
        return student

    def login(self, email: str, password: str) -> Optional[User]:
        """Acct 4 / Acct 15: Authenticate by email and password."""
        for s in self.__students:
            if s.get_email() == email and s.verify_password(password):
                return s
        for a in self.__admins:
            if a.get_email() == email and a.verify_password(password):
                return a
        return None

    def identify_role(self, user: User) -> str:
        """Acct 13: Return 'student' or 'admin'."""
        return user.get_role()

    def change_password(self, user: User, current_pwd: str,
                        new_pwd: str, confirm_pwd: str) -> bool:
        """Acct 7: Change password with validation."""
        if not user.verify_password(current_pwd):
            return False
        if new_pwd != confirm_pwd:
            return False
        if not self.validate_password(new_pwd):
            return False
        user.set_password(new_pwd)
        return True

    def update_mobile(self, user: User, new_mobile: str,
                      confirm_mobile: str) -> bool:
        """Acct 6: Update mobile; both entries must match."""
        if new_mobile != confirm_mobile:
            return False
        if not self.validate_mobile(new_mobile):
            return False
        user.set_phone(new_mobile)
        return True

    def find_student_by_id(self, student_id: str) -> Optional[Student]:
        """Helper: Find a student by their student ID."""
        for s in self.__students:
            if s.get_student_id() == student_id:
                return s
        return None


class AccountController:
    """Account management controller.
    Handles: Acct 5 (Profile), Acct 8 (Usage Status),
             Acct 9-10 (Activity History), Acct 11-12 (Funds)
    """

    def __init__(self) -> None:
        pass

    def get_profile_info(self, student: Student) -> Dict[str, object]:
        """Acct 5: Return student profile fields."""
        return {
            "first_name": student.get_first_name(),
            "last_name": student.get_last_name(),
            "student_id": student.get_student_id(),
            "email": student.get_email(),
            "phone": student.get_phone(),
            "balance": student.get_balance()
        }

    def get_usage_status(self, student: Student) -> Dict[str, object]:
        """Acct 8: Return usage status."""
        return {
            "current_bookings": student.get_active_bookings(),
            "ban_status": student.get_booking_ban_status(),
            "balance": student.get_balance(),
            "deal_package_hours": student.get_deal_package_hours()
        }

    def get_activity_history(self, student: Student, page: int) -> List:
        """Acct 9/10: Return a page of activity history."""
        return student.get_activity_history_page(page)

    def get_total_history_pages(self, student: Student) -> int:
        """Acct 10: Get total number of history pages."""
        return student.get_total_history_pages()

    def get_funds_summary(self, student: Student) -> Dict[str, float]:
        """Acct 11: Return balance and deal package hours."""
        return {
            "balance": student.get_balance(),
            "deal_package_hours": student.get_deal_package_hours()
        }

    def add_funds(self, student: Student, amount: float) -> bool:
        """Acct 12: Add funds; amount must be positive."""
        return student.add_funds(amount)


# ================================================================
# <<Boundary>> Section
# ================================================================

class AuthUI:
    """Login, registration, and credential management UI.
    Covers: Acct 1-4, 6-7, 13, 15
    """

    @staticmethod
    def show_welcome():
        print("\n" + "=" * 60)
        print("  MSSRB - Monash Smart Study Room Booking System")
        print("=" * 60)

    @staticmethod
    def show_login_menu() -> str:
        print("\n--- Welcome ---")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        return input("Select: ").strip()

    @staticmethod
    def get_login_credentials() -> tuple:
        print("\n--- Login (Acct 4 / Acct 15) ---")
        email = input("Email: ").strip()
        pwd = input("Password: ").strip()
        return email, pwd

    @staticmethod
    def get_registration_details() -> dict:
        print("\n--- Register New Account (Acct 1) ---")
        return {
            "email": input("Email (@student.monash.edu): ").strip(),
            "password": input("Password (>=8 chars, uppercase+digit): ").strip(),
            "first_name": input("First Name: ").strip(),
            "last_name": input("Last Name: ").strip(),
            "phone": input("Mobile (04XXXXXXXX): ").strip(),
            "student_id": input("Student ID: ").strip()
        }

    @staticmethod
    def get_new_mobile() -> tuple:
        print("\n--- Update Mobile (Acct 6) ---")
        return input("New mobile: ").strip(), input("Confirm mobile: ").strip()

    @staticmethod
    def get_password_change() -> tuple:
        print("\n--- Change Password (Acct 7) ---")
        return (input("Current password: ").strip(),
                input("New password: ").strip(),
                input("Confirm new password: ").strip())

    @staticmethod
    def show_message(msg: str):
        print(f"\n  >> {msg}")

    @staticmethod
    def show_error(msg: str):
        print(f"\n  [ERROR] {msg}")

    @staticmethod
    def show_success(msg: str):
        print(f"\n  [OK] {msg}")


class StudentMenuUI:
    """Student main menu and sub-menus.
    Covers: Acct 5, 8-12, navigation to Booking/Checkout
    """

    @staticmethod
    def show_main_menu(name: str) -> str:
        print(f"\n{'=' * 50}")
        print(f"  Student Menu — Welcome, {name}")
        print(f"{'=' * 50}")
        print("1. View Profile (Acct 5)")
        print("2. Update Mobile (Acct 6)")
        print("3. Change Password (Acct 7)")
        print("4. View Usage Status (Acct 8)")
        print("5. View Activity History (Acct 9/10)")
        print("6. Funds Management (Acct 11/12)")
        print("7. Search & Book a Room (Book 1-15, Check 1-11)")
        print("8. View / Cancel Bookings (Book 2/3/6/11-14)")
        print("0. Logout")
        return input("Select: ").strip()

    @staticmethod
    def show_profile(info: dict):
        print("\n--- Your Profile (Acct 5) ---")
        print(f"  Name     : {info['first_name']} {info['last_name']}")
        print(f"  Email    : {info['email']}")
        print(f"  Student ID: {info['student_id']}")
        print(f"  Phone    : {info['phone']}")
        print(f"  Balance  : ${info['balance']:.2f}")

    @staticmethod
    def show_usage_status(status: dict):
        print("\n--- Usage Status (Acct 8) ---")
        ban = "BANNED" if status["ban_status"] else "Active"
        print(f"  Account Status   : {ban}")
        print(f"  Balance          : ${status['balance']:.2f}")
        print(f"  Deal Pkg Hours   : {status['deal_package_hours']:.1f}h")
        print(f"  Active Bookings  : {len(status['current_bookings'])}")
        for b in status["current_bookings"]:
            print(f"    - {b}")

    @staticmethod
    def show_activity_history(records: list, page: int, total_pages: int):
        print(f"\n--- Activity History (Acct 9) — Page {page}/{total_pages} ---")
        if not records:
            print("  (No records)")
        for r in records:
            print(f"  {r}")

    @staticmethod
    def get_history_navigation(page: int, total: int) -> str:
        print(f"\n(Acct 10) Page {page}/{total} — [N]ext [P]rev [G]o to page [B]ack")
        return input("Select: ").strip().upper()

    @staticmethod
    def get_page_number() -> int:
        try:
            return int(input("Enter page number: ").strip())
        except ValueError:
            return 1

    @staticmethod
    def show_funds_summary(info: dict):
        print("\n--- Funds Summary (Acct 11) ---")
        print(f"  Balance        : ${info['balance']:.2f}")
        print(f"  Deal Pkg Hours : {info.get('deal_package_hours', 0):.1f}h")

    @staticmethod
    def get_funds_menu() -> str:
        print("\n1. Add Funds (Acct 12)")
        print("2. Purchase Deal Package (Check 7)")
        print("0. Back")
        return input("Select: ").strip()

    @staticmethod
    def get_topup_amount() -> float:
        try:
            return float(input("Enter amount to add ($): ").strip())
        except ValueError:
            return -1.0
