from typing import List, Optional
from entities.promo_code import PromoCode
from entities.deal_package import DealPackage
from entities.order import Order
from entities.student import Student
from entities.booking import Booking

class PaymentController:
    """Checkout and Payment Controller"""

    EQUIPMENT_DEPOSIT_AMOUNT = 100.0

    # Constants imported from Branch_CQ
    PAYMENT_METHOD_CHOICES = {
        "1": "balance",
        "2": "deal_package",
        "balance": "balance",
        "deal_package": "deal_package",
    }
    NEXT_STEP_CHOICES = {
        "1": "continue_booking",
        "2": "finish",
        "continue_booking": "continue_booking",
        "finish": "finish",
    }

    def __init__(self) -> None:
        self.__promo_codes: List[PromoCode] = []
        self.__deal_package = DealPackage("DP001", 100.0, 12.0)
        self.__order_counter = 0
        self.__latest_order: Optional[Order] = None

        # default promo code
        self.__promo_codes.append(PromoCode("NEWBEE20", 20.0))

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
            student: Student,
            booking: Optional[Booking] = None
    ) -> Optional[PromoCode]:

        target_code = code.strip().upper()
        search_code = "NEWBEE20" if target_code == "NEWBIE20" else target_code

        for promo in self.__promo_codes:

            if promo.get_code().upper() == search_code:

                if promo.is_used_by(student.get_student_id()):
                    return None

                if search_code == "NEWBEE20":
                    room_type = "Small"
                    if booking and hasattr(booking, "get_room"):
                        room = booking.get_room()
                        if room and hasattr(room, "get_room_type"):
                            room_type = room.get_room_type()
                    if room_type != "Small":
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
            has_equipment: bool,
            room_type: str = "Small"
    ) -> bool:

        if not self.can_use_deal_package(has_equipment, room_type):
            return False

        return student.deduct_deal_package_hours(
            required_hours
        )

    def can_use_deal_package(
            self,
            has_equipment: bool,
            room_type: str = "Small"
    ) -> bool:

        return (not has_equipment) and (room_type == "Small")

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

    # Methods imported from Branch_CQ

    def select_payment_method(self, choice: str) -> Optional[str]:
        """Validate payment method input (Checkout 1)."""
        return self.PAYMENT_METHOD_CHOICES.get(choice.strip().lower())

    def top_up_account(self, student: Student, amount: float) -> bool:
        """Top up account balance from the insufficient-balance flow."""
        return student.add_funds(amount)

    def complete_balance_payment(self, student: Student, order: Order) -> bool:
        """Deduct the payable amount and confirm the booking if successful."""
        if not self.pay_by_balance(student, order):
            return False
        return self.confirm_order(order, student)

    def complete_deal_package_payment(self, student: Student, order: Order) -> bool:
        """Pay with package hours and confirm the booking if successful."""
        booking = order.get_booking()
        duration = booking.calculate_duration_hours()
        room = booking.get_room()
        room_type = room.get_room_type() if hasattr(room, "get_room_type") else "Small"
        if not self.pay_by_deal_package(student, duration, booking.get_equipment_rental(), room_type):
            return False
        return self.confirm_order(order, student)

    def get_booking_summary(self, order: Order) -> dict:
        """Return the details needed before final confirmation."""
        booking = order.get_booking()
        student = booking.get_student()
        room = booking.get_room()
        return {
            "name": f"{student.get_first_name()} {student.get_last_name()}",
            "room": room.get_room_name(),
            "building": room.get_building(),
            "time_period": f"{booking.get_start_time()} to {booking.get_end_time()}",
            "price": order.get_final_price(),
            "equipment": booking.get_equipment_rental(),
        }

    def choose_next_step(self, choice: str) -> Optional[str]:
        """Validate post-confirmation navigation input (Checkout 11)."""
        return self.NEXT_STEP_CHOICES.get(choice.strip().lower())
