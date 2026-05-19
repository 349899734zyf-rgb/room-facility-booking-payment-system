"""
Equipment entity.
Covers: Room 11
"""


class Equipment:
    """设备实体类 (Booking Management 4, Room Management 5, 11)"""

    def __init__(self, equipment_id: str, deposit_amount: float) -> None:
        self.__equipment_id: str = equipment_id
        self.__deposit_amount: float = deposit_amount
        self.__is_available: bool = True

    # --- Accessors ---
    def get_equipment_id(self) -> str:
        return self.__equipment_id

    def get_deposit_amount(self) -> float:
        return self.__deposit_amount

    def get_is_available(self) -> bool:
        return self.__is_available

    # --- Mutators ---
    def set_equipment_id(self, eid: str) -> None:
        self.__equipment_id = eid

    def set_deposit_amount(self, amount: float) -> None:
        self.__deposit_amount = amount

    def set_is_available(self, available: bool) -> None:
        self.__is_available = available

    # --- Business Methods ---
    def refund_deposit(self) -> float:
        """退还押金 (Room Management 11)"""
        return self.__deposit_amount

