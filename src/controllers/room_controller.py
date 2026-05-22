"""
Module: room_controller.py
Layer: Controller
User Stories: Room 1, 3-8

Manages room CRUD operations, room type validation, usage status
tracking, time slot management, and predicted income calculations.
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
    """Controller for the Room Management feature.

    Responsibilities:
        - Add new rooms with auto-generated IDs (Room 1)
        - Validate room type / price / capacity consistency (Room 1)
        - View room listings (Room 3)
        - Remove rooms (Room 4)
        - Update room usage status (Room 5)
        - Update available time slots (Room 6)
        - Calculate predicted income (Room 7)
        - Change room information (Room 8)

    Collaborators:
        - Room (entity): room data and availability logic
    """

    def __init__(self) -> None:
        self.__rooms: List[Room] = []
        self.__room_counter: int = 0

    def get_rooms(self) -> List[Room]:
        """Return all rooms managed by this controller (Room 3)."""
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
        """Create and add a new room with an auto-generated ID (Room 1).

        Args:
            name: Descriptive room name.
            building: Building where the room is located.
            capacity: Maximum occupancy.
            price: Hourly booking rate.
            opening_hours: Opening hours string.
            room_type: Explicit type; if None, inferred from price.

        Returns:
            The new Room on success, or None if inputs are invalid.
        """
        if not all([name, building, opening_hours]) or capacity <= 0 or price <= 0:
            return None
        self.__room_counter += 1
        rid = f"{ROOM_ID_PREFIX}{self.__room_counter:0{ROOM_ID_DIGITS}d}"
        room = Room(rid, name, building, capacity, price, opening_hours, room_type=room_type)
        self.__rooms.append(room)
        return room


    def remove_room(self, room_id: str) -> bool:
        """Remove a room by its ID (Room 4)."""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                self.__rooms.remove(room)
                return True
        return False

    def find_room(self, room_id: str) -> Optional[Room]:
        """Find and return a room by its ID, or None if not found."""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                return room
        return None

    def update_room_info(self, room_id: str, updates: Dict[str, object]) -> bool:
        """Update room attributes from a dictionary of changes (Room 8).

        Args:
            room_id: The ID of the room to update.
            updates: Dict of field names to new values (e.g. {'name': '...', 'price': 15.0}).

        Returns:
            True if the room was found and updated, False otherwise.
        """
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
        """Update student presence and equipment rental flags (Room 5)."""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.set_is_student_in_room(is_student_in)
        room.set_is_equipment_rented(is_equipment_rented)
        return True

    def update_room_time_slots(self, room_id: str, available_slots: List[str]) -> bool:
        """Replace the room's available time slots list (Room 6)."""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.set_available_time_slots(available_slots)
        return True

    def register_room_time_slot(self, room_id: str, time_slot: str, available: bool) -> bool:
        """Add or remove an individual time slot, merging/splitting as necessary (Room 6)."""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.update_availability(time_slot, available)
        return True

    def get_predicted_income(self, room_id: str) -> float:
        """Return predicted income for a room based on booked slots (Room 7)."""
        room = self.find_room(room_id)
        if room is None:
            return 0.0
        return room.calculate_predicted_income()

