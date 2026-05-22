"""
RoomController.
Covers: Room 1, 3-8
"""
from typing import List, Dict, Optional
from entities.room import Room
from booking_constants import (
    ROOM_TYPE_SMALL,
    ROOM_TYPE_MEDIUM,
    ROOM_TYPE_LARGE,
    SMALL_ROOM_MAX_PRICE,
    MEDIUM_ROOM_MAX_PRICE,
    SMALL_ROOM_MAX_CAPACITY,
    MEDIUM_ROOM_MAX_CAPACITY,
    LARGE_ROOM_MAX_CAPACITY,
    ROOM_ID_PREFIX,
    ROOM_ID_DIGITS,
)


class RoomController:
    """Room Controller (Room Management 1, 3-8)"""

    def __init__(self) -> None:
        self.__rooms: List[Room] = []
        self.__room_counter: int = 0

    def get_rooms(self) -> List[Room]:
        return self.__rooms

    @staticmethod
    def validate_room_rules(price: float, capacity: int,
                            room_type: Optional[str] = None) -> Optional[str]:
        """Validate price-capacity consistency for a room type.

        If *room_type* is ``None`` the type is inferred from *price*.
        Returns the validated room-type string on success, or ``None``
        when the combination violates business rules.
        """
        if room_type is None:
            if price <= SMALL_ROOM_MAX_PRICE:
                room_type = ROOM_TYPE_SMALL
            elif price <= MEDIUM_ROOM_MAX_PRICE:
                room_type = ROOM_TYPE_MEDIUM
            else:
                room_type = ROOM_TYPE_LARGE

        if room_type == ROOM_TYPE_SMALL:
            if price > SMALL_ROOM_MAX_PRICE or capacity > SMALL_ROOM_MAX_CAPACITY:
                return None
        elif room_type == ROOM_TYPE_MEDIUM:
            if (price <= SMALL_ROOM_MAX_PRICE
                    or price > MEDIUM_ROOM_MAX_PRICE
                    or capacity > MEDIUM_ROOM_MAX_CAPACITY):
                return None
        elif room_type == ROOM_TYPE_LARGE:
            if price <= MEDIUM_ROOM_MAX_PRICE or capacity > LARGE_ROOM_MAX_CAPACITY:
                return None
        else:
            return None
        return room_type

    def add_room(self, name: str, building: str, capacity: int,
                 price: float, opening_hours: str, room_type: Optional[str] = None) -> Optional[Room]:
        """Add room (Room 1)"""
        if not all([name, building, opening_hours]) or capacity <= 0 or price <= 0:
            return None
        self.__room_counter += 1
        rid = f"{ROOM_ID_PREFIX}{self.__room_counter:0{ROOM_ID_DIGITS}d}"
        room = Room(rid, name, building, capacity, price, opening_hours, room_type=room_type)
        self.__rooms.append(room)
        return room


    def remove_room(self, room_id: str) -> bool:
        """Remove room (Room 4)"""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                self.__rooms.remove(room)
                return True
        return False

    def find_room(self, room_id: str) -> Optional[Room]:
        """Find room"""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                return room
        return None

    def update_room_info(self, room_id: str, updates: Dict[str, object]) -> bool:
        """Update room info (Room 8)"""
        room = self.find_room(room_id)
        if room is None:
            return False
        if "name" in updates:
            room.set_room_name(str(updates["name"]))
        if "building" in updates:
            room.set_building(str(updates["building"]))
        if "capacity" in updates:
            room.set_capacity(int(updates["capacity"]))
        if "price" in updates:
            room.set_price_per_hour(float(updates["price"]))
        if "opening_hours" in updates:
            room.set_opening_hours(str(updates["opening_hours"]))
        if "standard_equipment" in updates:
            room.set_standard_equipment(str(updates["standard_equipment"]))
        if "room_type" in updates:
            room.set_room_type(str(updates["room_type"]))
        return True

    def update_room_usage_status(self, room_id: str, is_student_in: bool,
                                 is_equipment_rented: bool) -> bool:
        """Update room usage status (Room Management 5)"""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.set_is_student_in_room(is_student_in)
        room.set_is_equipment_rented(is_equipment_rented)
        return True

    def update_room_time_slots(self, room_id: str, available_slots: List[str]) -> bool:
        """Update room time slots (Room Management 6)"""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.set_available_time_slots(available_slots)
        return True

    def get_predicted_income(self, room_id: str) -> float:
        """Get predicted income (Room 7)"""
        room = self.find_room(room_id)
        if room is None:
            return 0.0
        return room.calculate_predicted_income()

