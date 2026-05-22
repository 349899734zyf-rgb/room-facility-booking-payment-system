"""
Module: deal_package.py
Layer: Entity
User Stories: Checkout 6-7

Represents a pre-paid deal package that students can purchase to
pay for Small room bookings using bundled hours instead of balance.
"""


class DealPackage:
    """Entity for the pre-paid booking deal package.

    Responsibilities:
        - Store package metadata: ID, price, and included hours (Checkout 6)
        - Provide data for deal-package purchase and payment flows (Checkout 7)
    """

    def __init__(
            self,
            package_id: str,
            price: float,
            hours: float
    ) -> None:
        """Create a deal package.

        Args:
            package_id: Unique identifier for this package.
            price: Purchase price in dollars.
            hours: Number of booking hours included.
        """

        self.__package_id = package_id
        self.__price = price
        self.__hours = hours

    def get_package_id(self) -> str:
        return self.__package_id

    def get_price(self) -> float:
        return self.__price

    def get_hours(self) -> float:
        return self.__hours

    def set_package_id(self, package_id: str) -> None:
        self.__package_id = package_id

    def set_price(self, price: float) -> None:
        self.__price = price

    def set_hours(self, hours: float) -> None:
        self.__hours = hours
