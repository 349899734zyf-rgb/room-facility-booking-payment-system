"""
Module: promo_code.py
Layer: Entity
User Stories: Checkout 4-5

Represents a promotional discount code that can be applied once per
student to reduce the booking price by a percentage.
"""
from typing import List


class PromoCode:
    """Entity for a promotional discount code.

    Responsibilities:
        - Store code string and discount percentage (Checkout 4)
        - Track which students have used this code (Checkout 5)
        - Calculate discounted price from original price (Checkout 4)

    Business Rules:
        - Each student can use a given promo code only once.
        - Discount is applied as a percentage of the original price.
    """

    def __init__(
            self,
            code: str,
            discount_amount: float
    ) -> None:
        """Create a promo code.

        Args:
            code: The promotional code string (e.g. 'NEWBEE20').
            discount_amount: Discount percentage (e.g. 20.0 for 20%).
        """

        self.__code = code
        self.__discount_amount = discount_amount
        self.__used_students: List[str] = []

    def get_code(self) -> str:
        return self.__code

    def get_discount_amount(self) -> float:
        return self.__discount_amount

    def get_used_by_students(self) -> List[str]:
        return self.__used_students

    def set_code(self, code: str) -> None:
        self.__code = code

    def set_discount_amount(self, amount: float) -> None:
        self.__discount_amount = amount

    def is_valid(self) -> bool:
        """Return True if the code string is non-empty."""
        return self.__code.strip() != ""

    def is_used_by(self, student_id: str) -> bool:
        """Check whether a student has already redeemed this code (Checkout 5)."""
        return student_id in self.__used_students

    def mark_used(self, student_id: str) -> None:
        """Record that a student has used this code (Checkout 5)."""
        if not self.is_used_by(student_id):
            self.__used_students.append(student_id)

    def apply_discount(
            self,
            original_price: float
    ) -> float:
        """Calculate the discounted price (Checkout 4).

        Args:
            original_price: The original price before discount.

        Returns:
            The price after applying the percentage discount (minimum 0).
        """
        discount = original_price * (self.__discount_amount / 100)

        return max(
            0,
            original_price - discount
        )

