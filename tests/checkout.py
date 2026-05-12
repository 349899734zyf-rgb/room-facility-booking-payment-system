"""
MSSRB - Feature 4: Checkout
Covers: Check 1 ~ Check 11
Contains: <<Entity>> PromoCode, DealPackage, Order
          <<Controller>> PaymentController
          <<Boundary>> CheckoutUI
"""
from typing import List, Optional
from account import Student
from booking import Booking


# ================================================================
# <<Entity>> Section
# ================================================================

class PromoCode:
    """Promo code entity class.
    Each code has a fixed discount amount and tracks which
    students have used it (single-use per student).
    Referenced by: Check 4
    """

    def __init__(self, code: str, discount_amount: float) -> None:
        self.__code: str = code
        self.__discount_amount: float = discount_amount
        self.__used_by_students: List[str] = []

    # --- Accessors ---
    def get_code(self) -> str:
        return self.__code

    def get_discount_amount(self) -> float:
        return self.__discount_amount

    def get_used_by_students(self) -> List[str]:
        return self.__used_by_students

    # --- Mutators ---
    def set_code(self, code: str) -> None:
        self.__code = code

    def set_discount_amount(self, amount: float) -> None:
        self.__discount_amount = amount

    # --- Business Methods ---
    def is_valid(self) -> bool:
        """Check if the promo code string is non-empty."""
        return self.__code.strip() != ""

    def is_used_by(self, student_id: str) -> bool:
        """Check 4: Check if already used by the given student."""
        return student_id in self.__used_by_students

    def mark_used(self, student_id: str) -> None:
        """Mark this promo code as used by a student."""
        self.__used_by_students.append(student_id)

    def apply_discount(self, original_price: float) -> float:
        """Check 4: Apply discount. Final price never below $0."""
        return max(0, original_price - self.__discount_amount)


class DealPackage:
    """Deal package entity class.
    Default: $100 for 12 hours of booking time.
    Cannot be used with equipment-bundled bookings (Check 6).
    Referenced by: Check 3, 5, 6, 7
    """

    def __init__(self, package_id: str, price: float = 100.0,
                 hours: float = 12.0) -> None:
        self.__package_id: str = package_id
        self.__price: float = price
        self.__hours: float = hours

    # --- Accessors ---
    def get_package_id(self) -> str:
        return self.__package_id

    def get_price(self) -> float:
        return self.__price

    def get_hours(self) -> float:
        return self.__hours

    # --- Mutators ---
    def set_price(self, price: float) -> None:
        self.__price = price

    def set_hours(self, hours: float) -> None:
        self.__hours = hours


class Order:
    """Order entity class.
    Wraps a booking with payment details (method, promo discount).
    Check 9: Provides booking summary before confirmation.
    Check 10: Finalized when student confirms.
    """

    def __init__(self, order_id: str, booking: Booking,
                 price: float, payment_method: str) -> None:
        self.__order_id: str = order_id
        self.__booking: Booking = booking
        self.__price: float = price
        self.__promo_discount: float = 0.0
        self.__final_price: float = price
        self.__payment_method: str = payment_method

    # --- Accessors ---
    def get_order_id(self) -> str:
        return self.__order_id

    def get_booking(self) -> Booking:
        return self.__booking

    def get_price(self) -> float:
        return self.__price

    def get_promo_discount(self) -> float:
        return self.__promo_discount

    def get_final_price(self) -> float:
        return self.__final_price

    def get_payment_method(self) -> str:
        return self.__payment_method

    # --- Mutators ---
    def set_promo_discount(self, discount: float) -> None:
        """Apply promo discount and recalculate final price."""
        self.__promo_discount = discount
        self.__final_price = max(0, self.__price - discount)

    def set_payment_method(self, method: str) -> None:
        self.__payment_method = method

    # --- Business Methods ---
    def calculate_final_price(self) -> float:
        """Check 4: Return the price after promo discount."""
        return self.__final_price


# ================================================================
# <<Controller>> Section
# ================================================================

class PaymentController:
    """Payment and checkout controller.
    Handles: Check 1 (Choose Method), Check 2 (Balance Pay),
             Check 3/5/6 (Deal Package), Check 4 (Promo Code),
             Check 7 (Purchase Package), Check 9 (Order),
             Check 10 (Confirm), Check 11 (Next Step)
    """

    def __init__(self) -> None:
        self.__promo_codes: List[PromoCode] = []
        self.__deal_package: DealPackage = DealPackage("DP001", 100.0, 12.0)
        self.__order_counter: int = 0

    def get_promo_codes(self) -> List[PromoCode]:
        return self.__promo_codes

    def get_deal_package(self) -> DealPackage:
        return self.__deal_package

    def pay_by_balance(self, student: Student, amount: float) -> bool:
        """Check 2: Deduct amount from student's balance."""
        return student.deduct_balance(amount)

    def check_balance_sufficient(self, student: Student,
                                 amount: float) -> bool:
        """Check 2: Check if balance is sufficient."""
        return student.get_balance() >= amount

    def pay_by_deal_package(self, student: Student, hours: float,
                            has_equipment: bool) -> bool:
        """Check 3/5/6: Pay using deal package hours.
        Cannot use if booking includes equipment (Check 6).
        """
        if has_equipment:
            return False
        return student.deduct_deal_package_hours(hours)

    def can_use_deal_package(self, has_equipment: bool) -> bool:
        """Check 6: Returns False if equipment is bundled."""
        return not has_equipment

    def validate_promo_code(self, code: str,
                            student: Student) -> Optional[PromoCode]:
        """Check 4: Validate promo code. Returns None if invalid/used."""
        for pc in self.__promo_codes:
            if pc.get_code() == code:
                if pc.is_used_by(student.get_student_id()):
                    return None
                return pc
        return None

    def apply_promo_code(self, promo: PromoCode, student: Student,
                         order: Order) -> float:
        """Check 4: Apply promo discount and mark as used."""
        discount = promo.get_discount_amount()
        order.set_promo_discount(discount)
        promo.mark_used(student.get_student_id())
        student.mark_promo_code_used(promo.get_code())
        return order.get_final_price()

    def purchase_deal_package(self, student: Student) -> bool:
        """Check 7: Purchase deal package ($100 → 12 hours)."""
        if student.deduct_balance(self.__deal_package.get_price()):
            student.add_deal_package_hours(self.__deal_package.get_hours())
            return True
        return False

    def create_order(self, booking: Booking,
                     payment_method: str) -> Order:
        """Check 9: Create an order for the booking summary."""
        self.__order_counter += 1
        oid = f"OD{self.__order_counter:04d}"
        return Order(oid, booking, booking.get_total_price(), payment_method)

    def confirm_order(self, order: Order, student: Student) -> bool:
        """Check 10: Confirm the order and finalize booking."""
        booking = order.get_booking()
        booking.set_payment_method(order.get_payment_method())
        booking.set_status("confirmed")
        return True


# ================================================================
# <<Boundary>> Section
# ================================================================

class CheckoutUI:
    """Payment method selection and checkout UI.
    Covers: Check 1-11
    """

    @staticmethod
    def show_payment_menu(price: float, hours: float,
                          can_deal: bool) -> str:
        print(f"\n--- Payment (Check 1) — Total: ${price:.2f} ({hours:.1f}h) ---")
        print("1. Pay by Account Balance (Check 2)")
        if can_deal:
            print("2. Pay by Deal Package Hours (Check 3/5)")
        print("3. Enter Promo Code (Check 4)")
        print("0. Cancel")
        return input("Select: ").strip()

    @staticmethod
    def get_promo_code() -> str:
        return input("Enter promo code (Check 4): ").strip()

    @staticmethod
    def show_order_summary(order):
        print(f"\n--- Order Summary (Check 9) ---")
        b = order.get_booking()
        print(f"  Order ID : {order.get_order_id()}")
        print(f"  Room     : {b.get_room().get_room_name()}")
        print(f"  Time     : {b.get_start_time().strftime('%Y-%m-%d %H:%M')}"
              f" - {b.get_end_time().strftime('%H:%M')}")
        print(f"  Price    : ${order.get_price():.2f}")
        if order.get_promo_discount() > 0:
            print(f"  Discount : -${order.get_promo_discount():.2f}")
        print(f"  Final    : ${order.get_final_price():.2f}")
        print(f"  Method   : {order.get_payment_method()}")

    @staticmethod
    def confirm_order() -> bool:
        print("\n(Check 10) Confirm this booking? (y/n):")
        return input("Select: ").strip().lower() == "y"

    @staticmethod
    def show_next_step() -> str:
        print("\n--- What's next? (Check 11) ---")
        print("1. Make another booking")
        print("2. Return to main menu")
        return input("Select: ").strip()
