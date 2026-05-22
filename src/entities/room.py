"""
Room entity.
Covers: Room 1-8
"""
from typing import List, Optional
from booking_constants import (
    ROOM_TYPE_SMALL,
    ROOM_TYPE_MEDIUM,
    ROOM_TYPE_LARGE,
    SMALL_ROOM_MAX_PRICE,
    MEDIUM_ROOM_MAX_PRICE,
    EQUIPMENT_RENTAL_FEE,
)


class Room:
    """Room entity (Room Management 1, 4-8, Booking Management 1)"""

    def __init__(self, room_id: str, room_name: str, building: str,
                 capacity: int, price_per_hour: float, opening_hours: str,
                 room_type: Optional[str] = None, standard_equipment: str = "") -> None:
        self.__room_id: str = room_id
        self.__room_name: str = room_name
        self.__building: str = building
        self.__capacity: int = capacity
        self.__price_per_hour: float = price_per_hour
        self.__opening_hours: str = opening_hours
        self.__available_time_slots: List[str] = []
        self.__is_equipment_rented: bool = False
        self.__is_student_in_room: bool = False

        if room_type is None:
            if price_per_hour <= SMALL_ROOM_MAX_PRICE:
                self.__room_type = ROOM_TYPE_SMALL
            elif price_per_hour <= MEDIUM_ROOM_MAX_PRICE:
                self.__room_type = ROOM_TYPE_MEDIUM
            else:
                self.__room_type = ROOM_TYPE_LARGE
        else:
            self.__room_type = room_type

        self.__standard_equipment = standard_equipment

    # --- Accessors ---
    def get_room_id(self) -> str:
        return self.__room_id

    def get_room_name(self) -> str:
        return self.__room_name

    def get_building(self) -> str:
        return self.__building

    def get_capacity(self) -> int:
        return self.__capacity

    def get_price_per_hour(self) -> float:
        return self.__price_per_hour

    def get_opening_hours(self) -> str:
        return self.__opening_hours

    def get_available_time_slots(self) -> List[str]:
        return self.__available_time_slots

    def get_is_equipment_rented(self) -> bool:
        return self.__is_equipment_rented

    def get_is_student_in_room(self) -> bool:
        return self.__is_student_in_room

    # --- Mutators ---
    def set_room_id(self, room_id: str) -> None:
        self.__room_id = room_id

    def set_room_name(self, room_name: str) -> None:
        self.__room_name = room_name

    def set_building(self, building: str) -> None:
        self.__building = building

    def set_capacity(self, capacity: int) -> None:
        self.__capacity = capacity

    def set_price_per_hour(self, price: float) -> None:
        self.__price_per_hour = price

    def set_opening_hours(self, hours: str) -> None:
        self.__opening_hours = hours

    def set_available_time_slots(self, slots: List[str]) -> None:
        self.__available_time_slots = slots

    def set_is_equipment_rented(self, status: bool) -> None:
        self.__is_equipment_rented = status

    def set_is_student_in_room(self, status: bool) -> None:
        self.__is_student_in_room = status

    # --- Business Methods ---
    def is_available(self, start_time: str, end_time: str) -> bool:
        """Check if the room is available in specified time slot (Book 1)"""
        time_slot = f"{start_time}-{end_time}"
        return time_slot in self.__available_time_slots

    def calculate_predicted_income(self) -> float:
        """Calculate predicted income (Room 7)"""
        booked_slots = len(self.__available_time_slots)
        income = booked_slots * self.__price_per_hour
        if self.__is_equipment_rented:
            income += EQUIPMENT_RENTAL_FEE
        return income

    def update_availability(self, time_slot: str, available: bool) -> None:
        """Update availability time slot (Room 5/6)"""
        if available and time_slot not in self.__available_time_slots:
            self.__available_time_slots.append(time_slot)
        elif not available and time_slot in self.__available_time_slots:
            self.__available_time_slots.remove(time_slot)

    def get_room_type(self) -> str:
        return self.__room_type

    def set_room_type(self, room_type: str) -> None:
        self.__room_type = room_type

    def get_standard_equipment(self) -> str:
        return self.__standard_equipment

    def set_standard_equipment(self, equipment: str) -> None:
        self.__standard_equipment = equipment

    def __str__(self) -> str:
        return f"{self.__room_id} | {self.__room_name}"

