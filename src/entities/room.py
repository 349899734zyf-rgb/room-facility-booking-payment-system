"""
Module: room.py
Layer: Entity
User Stories: Room 1-8, Book 3.1

Represents a bookable study room with pricing, capacity, time-slot
availability, and automatic room type classification (Small/Medium/Large).
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
    """Entity for a bookable study room.

    Responsibilities:
        - Store room metadata: ID, name, building, capacity, price (Room 1)
        - Auto-classify room type by price (Small/Medium/Large)
        - Manage available time slots for booking (Room 5-6)
        - Track student presence and equipment rental status (Room 5)
        - Calculate predicted income from booked slots (Room 7)

    Business Rules:
        - Room type inferred from price: <= $10 = Small, <= $40 = Medium, > $40 = Large.
        - Time slots formatted as 'YYYY-MM-DD HH:MM-YYYY-MM-DD HH:MM'.
    """

    def __init__(self, room_id: str, room_name: str, building: str,
                 capacity: int, price_per_hour: float, opening_hours: str,
                 room_type: Optional[str] = None, standard_equipment: str = "") -> None:
        """Create a room with automatic type classification.

        Args:
            room_id: Unique room identifier (e.g. 'RM0001').
            room_name: Descriptive room name.
            building: Building where the room is located.
            capacity: Maximum occupancy.
            price_per_hour: Hourly booking rate.
            opening_hours: Opening hours string (e.g. '09:00-18:00').
            room_type: Explicit type override; if None, inferred from price.
            standard_equipment: Description of built-in equipment.
        """
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
        """Return the unique room identifier."""
        return self.__room_id

    def get_room_name(self) -> str:
        return self.__room_name

    def get_building(self) -> str:
        return self.__building

    def get_capacity(self) -> int:
        """Return the room's maximum occupancy."""
        return self.__capacity

    def get_price_per_hour(self) -> float:
        """Return the hourly booking rate."""
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
    # --- Business Methods ---
    def _extract_time_only(self, slot_str: str) -> str:
        """Extract HH:MM-HH:MM from YYYY-MM-DD HH:MM-YYYY-MM-DD HH:MM or HH:MM-HH:MM."""
        import re
        times = re.findall(r'\d{2}:\d{2}', slot_str)
        if len(times) == 2:
            return f"{times[0]}-{times[1]}"
        return slot_str.strip()

    def _parse_slot(self, slot_str: str):
        """Parse time slot string into (date_str, start_minutes, end_minutes).

        Returns None if format is invalid.
        """
        parts = slot_str.split('-')
        if len(parts) != 2:
            return None
        start_part, end_part = parts[0].strip(), parts[1].strip()

        def to_minutes(t_str: str) -> int:
            try:
                h, m = map(int, t_str.split(':'))
                return h * 60 + m
            except Exception:
                return -1

        # Check if there is a date prefix
        if len(start_part) >= 16 and start_part[10] == ' ':
            date_str = start_part[:10]
            start_time_str = start_part[11:]
            if len(end_part) >= 16 and end_part[10] == ' ':
                end_time_str = end_part[11:]
            else:
                end_time_str = end_part
            s_min = to_minutes(start_time_str)
            e_min = to_minutes(end_time_str)
            if s_min == -1 or e_min == -1 or s_min >= e_min:
                return None
            return date_str, s_min, e_min
        else:
            s_min = to_minutes(start_part)
            e_min = to_minutes(end_part)
            if s_min == -1 or e_min == -1 or s_min >= e_min:
                return None
            return None, s_min, e_min

    def _format_slot(self, date_str, start_mins, end_mins) -> str:
        def to_time_str(mins: int) -> str:
            h = mins // 60
            m = mins % 60
            return f"{h:02d}:{m:02d}"

        start_t = to_time_str(start_mins)
        end_t = to_time_str(end_mins)
        if date_str:
            return f"{date_str} {start_t}-{date_str} {end_t}"
        else:
            return f"{start_t}-{end_t}"

    def _merge_intervals(self, intervals):
        if not intervals:
            return []
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        for current in intervals[1:]:
            prev_start, prev_end = merged[-1]
            curr_start, curr_end = current
            if curr_start <= prev_end:
                merged[-1] = (prev_start, max(prev_end, curr_end))
            else:
                merged.append(current)
        return merged

    def is_available(self, start_time: str, end_time: str) -> bool:
        """Check if the room is available in the specified time slot (Book 3.1).

        Args:
            start_time: Start time string.
            end_time: End time string.

        Returns:
            True if the requested slot is contained within any available slot.
        """
        # First fallback to exact match check
        time_slot = f"{start_time}-{end_time}"
        if time_slot in self.__available_time_slots:
            return True

        import re
        def to_minutes(t_str: str) -> int:
            try:
                h, m = map(int, t_str.split(':'))
                return h * 60 + m
            except Exception:
                return -1

        def parse_datetime_or_time(t_str: str):
            t_str = t_str.strip()
            if len(t_str) >= 16 and t_str[10] == ' ':
                return t_str[:10], to_minutes(t_str[11:])
            elif len(t_str) == 5 and ':' in t_str:
                return None, to_minutes(t_str)
            else:
                match = re.search(r'\d{2}:\d{2}', t_str)
                if match:
                    return None, to_minutes(match.group())
                return None, -1

        req_start_date, req_start_mins = parse_datetime_or_time(start_time)
        req_end_date, req_end_mins = parse_datetime_or_time(end_time)

        if req_start_mins == -1 or req_end_mins == -1 or req_start_mins >= req_end_mins:
            return False

        req_date = req_start_date or req_end_date

        for slot in self.__available_time_slots:
            parsed = self._parse_slot(slot)
            if not parsed:
                # If slot is invalid/unparseable (e.g. mock string "s1"), check exact string equality
                if slot == time_slot:
                    return True
                # Check extract time only
                time_only_search = self._extract_time_only(time_slot)
                if ' ' not in slot and slot == time_only_search:
                    return True
                continue
            avail_date, avail_start, avail_end = parsed

            # Date compatibility check
            if avail_date is not None and req_date is not None and avail_date != req_date:
                continue

            # Containment check
            if avail_start <= req_start_mins and req_end_mins <= avail_end:
                return True
        return False

    def update_availability(self, time_slot: str, available: bool) -> None:
        """Add or remove a time slot from the available slots list (Room 5-6).

        Args:
            time_slot: Time slot string to add/remove.
            available: True to add the slot, False to remove it.
        """
        if available:
            # Merging logic
            parsed_slots = []
            unparseable_slots = []
            for s in self.__available_time_slots:
                parsed = self._parse_slot(s)
                if parsed:
                    parsed_slots.append(parsed)
                else:
                    unparseable_slots.append(s)

            new_parsed = self._parse_slot(time_slot)
            if new_parsed:
                parsed_slots.append(new_parsed)
            else:
                unparseable_slots.append(time_slot)

            by_date = {}
            for date_str, s_min, e_min in parsed_slots:
                if date_str not in by_date:
                    by_date[date_str] = []
                by_date[date_str].append((s_min, e_min))

            new_slots = list(unparseable_slots)
            for date_str, intervals in by_date.items():
                merged = self._merge_intervals(intervals)
                for s_min, e_min in merged:
                    new_slots.append(self._format_slot(date_str, s_min, e_min))

            # Maintain uniqueness of unparseable slots if added
            self.__available_time_slots = []
            for ns in new_slots:
                if ns not in self.__available_time_slots:
                    self.__available_time_slots.append(ns)
        else:
            # Splitting/removing logic
            req_parsed = self._parse_slot(time_slot)
            if not req_parsed:
                # If we cannot parse requested time_slot, fallback to exact string removal
                if time_slot in self.__available_time_slots:
                    self.__available_time_slots.remove(time_slot)
                else:
                    time_only_search = self._extract_time_only(time_slot)
                    for s in self.__available_time_slots:
                        if ' ' not in s and s == time_only_search:
                            self.__available_time_slots.remove(s)
                            break
                return

            req_date, req_start, req_end = req_parsed

            new_slots = []
            removed = False
            for slot in self.__available_time_slots:
                parsed = self._parse_slot(slot)
                if not parsed:
                    # Keep unparseable slots but check if they match requested exactly
                    if slot == time_slot:
                        removed = True
                        continue
                    time_only_search = self._extract_time_only(time_slot)
                    if ' ' not in slot and slot == time_only_search:
                        removed = True
                        continue
                    new_slots.append(slot)
                    continue

                avail_date, avail_start, avail_end = parsed

                # Date compatibility check
                date_matches = (avail_date == req_date) or (avail_date is None) or (req_date is None)
                contains = (avail_start <= req_start) and (req_end <= avail_end)

                if not removed and date_matches and contains:
                    removed = True
                    # Split the slot
                    if avail_start < req_start:
                        new_slots.append(self._format_slot(avail_date, avail_start, req_start))
                    if req_end < avail_end:
                        new_slots.append(self._format_slot(avail_date, req_end, avail_end))
                else:
                    new_slots.append(slot)

            self.__available_time_slots = new_slots

    def calculate_predicted_income(self) -> float:
        """Room 7: Income = booked_slots * price + equipment fee."""
        booked_slots = len(self.__available_time_slots)
        income = booked_slots * self.__price_per_hour
        if self.__is_equipment_rented:
            income += EQUIPMENT_RENTAL_FEE
        return income

    def get_room_type(self) -> str:
        """Return the room type classification ('Small', 'Medium', or 'Large')."""
        return self.__room_type

    def set_room_type(self, room_type: str) -> None:
        self.__room_type = room_type

    def get_standard_equipment(self) -> str:
        return self.__standard_equipment

    def set_standard_equipment(self, equipment: str) -> None:
        self.__standard_equipment = equipment

    def __str__(self) -> str:
        return f"{self.__room_id} | {self.__room_name}"

