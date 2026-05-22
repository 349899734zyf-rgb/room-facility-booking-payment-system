"""
Module: order.py
Layer: Entity
User Stories: Checkout 1-5

Represents a payment order linking a booking to a payment method,
with optional promotional discount applied.
"""


class Order:
    """Entity for a payment order in the checkout flow.

    Responsibilities:
        - Link a booking to its payment method and pricing (Checkout 1)
        - Track promotional discount application (Checkout 4-5)
        - Calculate the final payable price after discounts (Checkout 3)
    """

    def __init__(
            self,
            order_id,
            booking,
            price,
            payment_method
    ):
        """Create an order for a booking.

        Args:
            order_id: Unique order identifier.
            booking: The Booking entity this order pays for.
            price: Original price before any discount.
            payment_method: 'balance' or 'deal_package'.
        """

        self.__order_id = order_id
        self.__booking = booking
        self.__price = price
        self.__promo_discount = 0
        self.__final_price = price
        self.__payment_method = payment_method
        self.__promo_code_used = None

    def get_booking(self):
        return self.__booking

    def get_order_id(self):
        return self.__order_id

    def get_price(self):
        return self.__price

    def get_promo_discount(self):
        return self.__promo_discount

    def get_payment_method(self):
        return self.__payment_method

    def get_final_price(self):
        return self.__final_price

    def get_promo_code_used(self):
        return self.__promo_code_used

    def set_promo_discount(self, discount):
        """Apply a promotional discount and recalculate the final price (Checkout 4)."""

        self.__promo_discount = discount

        self.__final_price = max(
            0,
            self.__price - discount
        )

    def set_payment_method(self, method):

        self.__payment_method = method

    def set_promo_code_used(self, code):

        self.__promo_code_used = code

    def calculate_final_price(self):
        """Recalculate and return the final price after promo discount (Checkout 3)."""

        self.__final_price = max(
            0,
            self.__price - self.__promo_discount
        )

        return self.__final_price
