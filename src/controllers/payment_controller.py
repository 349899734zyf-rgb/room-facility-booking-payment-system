from typing import List, Optional

try:
    from src.entity_classes import (
        Student,
        PromoCode,
        DealPackage,
        Booking,
        Order
    )
except ModuleNotFoundError:
    from entity_classes import (
        Student,
        PromoCode,
        DealPackage,
        Booking,
        Order
    )

class PaymentController:
    """Checkout and Payment Controller"""

    def __init__(self) -> None:
        self.__promo_codes: List[PromoCode] = []
        self.__deal_package = DealPackage("DP001", 100.0, 12.0)
        self.__order_counter = 0

        # default promo code
        self.__promo_codes.append(
            PromoCode("SAVE20", 20.0)
        )

    # =====================================================
    # Promo Code
    # =====================================================

    def validate_promo_code(
            self,
            code: str,
            student: Student
    ) -> Optional[PromoCode]:

        for promo in self.__promo_codes:

            if promo.get_code() == code:

                if promo.is_used_by(student.get_student_id()):
                    return None

                return promo

        return None

    def apply_promo_code(
            self,
            promo: PromoCode,
            student: Student,
            order: Order
    ) -> float:

        discount = promo.get_discount_amount()

        order.set_promo_discount(discount)

        promo.mark_used(student.get_student_id())

        student.mark_promo_code_used(
            promo.get_code()
        )

        return order.get_final_price()

    # =====================================================
    # Deal Package
    # =====================================================

    def purchase_deal_package(
            self,
            student: Student
    ) -> bool:

        package_price = self.__deal_package.get_price()

        if student.deduct_balance(package_price):

            student.add_deal_package_hours(
                self.__deal_package.get_hours()
            )

            return True

        return False

    def pay_by_deal_package(
            self,
            student: Student,
            required_hours: float,
            has_equipment: bool
    ) -> bool:

        # package cannot be used with equipment
        if has_equipment:
            return False

        return student.deduct_deal_package_hours(
            required_hours
        )

    # =====================================================
    # Balance Payment
    # =====================================================

    def check_balance_sufficient(
            self,
            student: Student,
            amount: float
    ) -> bool:

        return student.get_balance() >= amount

    def pay_by_balance(
            self,
            student: Student,
            amount: float
    ) -> bool:

        return student.deduct_balance(amount)

    # =====================================================
    # Order
    # =====================================================

    def create_order(
            self,
            booking: Booking,
            payment_method: str
    ) -> Order:

        self.__order_counter += 1

        order_id = f"OD{self.__order_counter:04d}"

        return Order(
            order_id,
            booking,
            booking.get_total_price(),
            payment_method
        )

    def confirm_order(
            self,
            order: Order,
            student: Student
    ) -> bool:

        booking = order.get_booking()

        booking.set_status("confirmed")

        booking.set_payment_method(
            order.get_payment_method()
        )

        return True
