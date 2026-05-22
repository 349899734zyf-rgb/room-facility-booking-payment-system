"""
Module: equipment.py
Layer: Entity
User Stories: Room 5, Room 11, Book 3.4

Represents a piece of rental equipment (e.g. AV gear) that students
can optionally rent alongside a room booking, subject to a deposit.
"""
from booking_constants import EQUIPMENT_RENTAL_FEE


class Equipment:
    """Entity for rental equipment.

    Responsibilities:
        - Store equipment metadata: ID, name, category, deposit (Room 5)
        - Track availability status for room usage updates (Room 5)
        - Provide deposit refund amount on return (Room 11)
    """

    def __init__(self, equipment_id: str, *args, **kwargs) -> None:
        """Create an equipment item.

        Args:
            equipment_id: Unique equipment identifier.
            *args: Positional args parsed as (name), (name, deposit),
                or (name, category, deposit).
            **kwargs: Optional keyword args: name, category, deposit_amount,
                deposit, rental_fee.
        """
        self.__equipment_id: str = equipment_id
        self.__is_available: bool = True
        self.__rental_fee: float = float(kwargs.get("rental_fee", EQUIPMENT_RENTAL_FEE))

        name = "Unknown"
        category = "AV"
        deposit_amount = 0.0

        if "name" in kwargs:
            name = kwargs["name"]
        if "category" in kwargs:
            category = kwargs["category"]
        if "deposit_amount" in kwargs:
            deposit_amount = kwargs["deposit_amount"]
        elif "deposit" in kwargs:
            deposit_amount = kwargs["deposit"]

        # Parse positional arguments
        if len(args) == 1:
            val = args[0]
            if isinstance(val, (int, float)):
                deposit_amount = float(val)
                name = "Equipment"
            else:
                name = str(val)
        elif len(args) == 2:
            name = str(args[0])
            val = args[1]
            if isinstance(val, (int, float)):
                deposit_amount = float(val)
            else:
                category = str(val)
        elif len(args) >= 3:
            name = str(args[0])
            category = str(args[1])
            deposit_amount = float(args[2])

        self.__name: str = name
        self.__category: str = category
        self.__deposit_amount: float = deposit_amount

    # --- Accessors ---
    def get_equipment_id(self) -> str:
        return self.__equipment_id

    def get_name(self) -> str:
        return self.__name

    def get_category(self) -> str:
        return self.__category

    def get_deposit_amount(self) -> float:
        return self.__deposit_amount

    def get_is_available(self) -> bool:
        return self.__is_available

    def get_rental_fee(self) -> float:
        return self.__rental_fee

    # --- Mutators ---
    def set_equipment_id(self, eid: str) -> None:
        self.__equipment_id = eid

    def set_deposit_amount(self, amount: float) -> None:
        self.__deposit_amount = amount

    def set_is_available(self, available: bool) -> None:
        self.__is_available = available

    # --- Business Methods ---
    def refund_deposit(self) -> float:
        """Return the deposit amount for refund processing (Room 11)."""
        return self.__deposit_amount

    def __str__(self) -> str:
        status = "Available" if self.__is_available else "In Use"
        return f"{self.__equipment_id} | {self.__name} | {status}"
