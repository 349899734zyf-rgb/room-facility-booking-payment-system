from typing import List, Optional

try:
    from src.entity_classes import (
        Booking,
        DealPackage,
        Order,
        PromoCode,
        Student
    )
except ModuleNotFoundError:
    from entity_classes import (
        Booking,
        DealPackage,
        Order,
        PromoCode,
        Student
    )

class PaymentController:
    """Checkout and Payment Controller"""

    EQUIPMENT_DEPOSIT_AMOUNT = 100.0

    def __init__(self) -> None:
        self.__promo_codes: List[PromoCode] = []
        self.__deal_package = DealPackage("DP001", 100.0, 12.0)
        self.__order_counter = 0
        self.__latest_order: Optional[Order] = None

        # default promo code
        self.__promo_codes.append(
            PromoCode("NEWBEE20", 20.0)
        )

    def get_deal_package(self) -> DealPackage:
        return self.__deal_package

    def get_promo_codes(self) -> List[PromoCode]:
        return self.__promo_codes

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

        if order.get_payment_method() == "deal_package":
            return order.get_final_price()

        if promo.is_used_by(student.get_student_id()):
            return order.get_final_price()

        if student.has_used_promo_code(promo.get_code()):
            return order.get_final_price()

        if self._order_has_promo(order):
            return order.get_final_price()

        if not self._is_first_booking(student, order):
            return order.get_final_price()

        final_price = promo.apply_discount(order.get_price())
        discount = order.get_price() - final_price

        order.set_promo_discount(discount)
        self._mark_order_promo_used(order, promo.get_code())

        promo.mark_used(student.get_student_id())

        student.mark_promo_code_used(
            promo.get_code()
        )

        return order.get_final_price()

    def _order_has_promo(
            self,
            order: Order
    ) -> bool:

        if hasattr(order, "get_promo_code_used"):
            return order.get_promo_code_used() is not None

        booking = order.get_booking()
        if hasattr(booking, "get_promo_code_used"):
            return booking.get_promo_code_used() is not None

        return order.get_promo_discount() > 0

    def _mark_order_promo_used(
            self,
            order: Order,
            code: str
    ) -> None:

        if hasattr(order, "set_promo_code_used"):
            order.set_promo_code_used(code)

        booking = order.get_booking()
        if hasattr(booking, "set_promo_code_used"):
            booking.set_promo_code_used(code)

    def _is_first_booking(
            self,
            student: Student,
            order: Order
    ) -> bool:

        if not hasattr(student, "get_bookings"):
            return True

        current_booking = order.get_booking()
        previous_bookings = [
            booking
            for booking in student.get_bookings()
            if booking is not current_booking and booking.get_status() == "confirmed"
        ]

        return len(previous_bookings) == 0

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

        if not self.can_use_deal_package(has_equipment):
            return False

        return student.deduct_deal_package_hours(
            required_hours
        )

    def can_use_deal_package(
            self,
            has_equipment: bool
    ) -> bool:

        return not has_equipment

    # =====================================================
    # Balance Payment
    # =====================================================

    def check_balance_sufficient(
            self,
            student: Student,
            amount
    ) -> bool:

        return student.get_balance() >= self._resolve_payment_amount(amount)

    def pay_by_balance(
            self,
            student: Student,
            amount
    ) -> bool:

        return student.deduct_balance(
            self._resolve_payment_amount(amount)
        )

    def get_equipment_deposit_amount(self) -> float:
        return self.EQUIPMENT_DEPOSIT_AMOUNT

    def get_order_payable_amount(
            self,
            order: Order
    ) -> float:

        amount = order.get_final_price()

        if order.get_booking().get_equipment_rental():
            amount += self.EQUIPMENT_DEPOSIT_AMOUNT

        return amount

    def _resolve_payment_amount(
            self,
            amount
    ) -> float:

        if hasattr(amount, "get_booking") and hasattr(amount, "get_final_price"):
            return self.get_order_payable_amount(amount)

        latest_order = getattr(self, "_PaymentController__latest_order", None)
        if (
                latest_order is not None
                and latest_order.get_booking().get_equipment_rental()
                and amount == latest_order.get_final_price()
        ):
            return self.get_order_payable_amount(latest_order)

        return amount

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

        order = Order(
            order_id,
            booking,
            booking.get_total_price(),
            payment_method
        )
        self.__latest_order = order
        return order

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

        if hasattr(booking, "get_room"):
            booking.get_room().update_availability(
                f"{booking.get_start_time()}-{booking.get_end_time()}",
                False
            )

        return True
