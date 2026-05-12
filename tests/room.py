"""
MSSRB - Feature 2: Room Management
Covers: Room 1 ~ Room 11
Contains: <<Entity>> Room, Equipment
          <<Controller>> RoomController, AdminController
          <<Boundary>> AdminMenuUI
"""
from typing import List, Optional, Dict
from account import Student, Admin


# ================================================================
# <<Entity>> Section
# ================================================================

class Room:
    """Room entity class.
    Stores room details (name, building, capacity, price, opening hours),
    available time slots, and occupancy/equipment status.
    Referenced by: Room 1, 3-8, Book 1, 5, 9, 15
    """

    def __init__(self, room_id: str, room_name: str, building: str,
                 capacity: int, price_per_hour: float,
                 opening_hours: str) -> None:
        self.__room_id: str = room_id
        self.__room_name: str = room_name
        self.__building: str = building
        self.__capacity: int = capacity
        self.__price_per_hour: float = price_per_hour
        self.__opening_hours: str = opening_hours
        self.__available_time_slots: List[str] = []
        self.__is_equipment_rented: bool = False
        self.__is_student_in_room: bool = False

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
    def is_available(self, time_slot: str) -> bool:
        """Book 1: Check if the room is available for the given slot."""
        return time_slot in self.__available_time_slots

    def calculate_predicted_income(self) -> float:
        """Room 7: Income = booked_slots × price + equipment fee ($10)."""
        booked_slots = len(self.__available_time_slots)
        income = booked_slots * self.__price_per_hour
        if self.__is_equipment_rented:
            income += 10.0
        return income

    def update_availability(self, time_slot: str, available: bool) -> None:
        """Room 5/6: Add or remove a time slot."""
        if available and time_slot not in self.__available_time_slots:
            self.__available_time_slots.append(time_slot)
        elif not available and time_slot in self.__available_time_slots:
            self.__available_time_slots.remove(time_slot)

    def __str__(self) -> str:
        return (f"[{self.__room_id}] {self.__room_name} | "
                f"{self.__building} | Cap: {self.__capacity} | "
                f"${self.__price_per_hour:.2f}/hr | {self.__opening_hours}")


class Equipment:
    """Equipment entity class.
    Tracks deposit amount and availability status.
    Referenced by: Book 4, Room 5, Room 11
    """

    def __init__(self, equipment_id: str, name: str,
                 deposit_amount: float, rental_fee: float = 10.0) -> None:
        self.__equipment_id: str = equipment_id
        self.__name: str = name
        self.__deposit_amount: float = deposit_amount
        self.__rental_fee: float = rental_fee
        self.__is_available: bool = True

    # --- Accessors ---
    def get_equipment_id(self) -> str:
        return self.__equipment_id

    def get_name(self) -> str:
        return self.__name

    def get_deposit_amount(self) -> float:
        return self.__deposit_amount

    def get_rental_fee(self) -> float:
        return self.__rental_fee

    def get_is_available(self) -> bool:
        return self.__is_available

    # --- Mutators ---
    def set_deposit_amount(self, amount: float) -> None:
        self.__deposit_amount = amount

    def set_is_available(self, available: bool) -> None:
        self.__is_available = available

    # --- Business Methods ---
    def refund_deposit(self) -> float:
        """Room 11: Return the deposit amount for refund."""
        return self.__deposit_amount

    def __str__(self) -> str:
        status = "Available" if self.__is_available else "In Use"
        return (f"[{self.__equipment_id}] {self.__name} | "
                f"Deposit: ${self.__deposit_amount:.2f} | "
                f"Fee: ${self.__rental_fee:.2f} | {status}")


# ================================================================
# <<Controller>> Section
# ================================================================

class RoomController:
    """Room management controller.
    Handles: Room 1 (Add), Room 3 (View), Room 4 (Remove),
             Room 5 (Status), Room 6 (Time Slots), Room 7 (Income),
             Room 8 (Update Info)
    """

    def __init__(self) -> None:
        self.__rooms: List[Room] = []
        self.__room_counter: int = 0

    def get_rooms(self) -> List[Room]:
        return self.__rooms

    def add_room(self, name: str, building: str, capacity: int,
                 price: float, opening_hours: str) -> Optional[Room]:
        """Room 1: Add a new room. All text fields non-empty, capacity > 0, price > 0."""
        if not all([name.strip(), building.strip(), opening_hours.strip()]):
            return None
        if capacity <= 0 or price <= 0:
            return None
        self.__room_counter += 1
        rid = f"RM{self.__room_counter:04d}"
        room = Room(rid, name, building, capacity, price, opening_hours)
        self.__rooms.append(room)
        return room

    def remove_room(self, room_id: str) -> bool:
        """Room 4: Remove a room by ID."""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                self.__rooms.remove(room)
                return True
        return False

    def find_room(self, room_id: str) -> Optional[Room]:
        """Helper: Find a room by ID."""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                return room
        return None

    def update_room_info(self, room_id: str,
                         updates: Dict[str, object]) -> bool:
        """Room 8: Update one or more fields of a room."""
        room = self.find_room(room_id)
        if room is None:
            return False
        if "name" in updates and str(updates["name"]).strip():
            room.set_room_name(str(updates["name"]))
        if "building" in updates and str(updates["building"]).strip():
            room.set_building(str(updates["building"]))
        if "capacity" in updates:
            cap = int(updates["capacity"])
            if cap > 0:
                room.set_capacity(cap)
        if "price" in updates:
            p = float(updates["price"])
            if p > 0:
                room.set_price_per_hour(p)
        if "opening_hours" in updates and str(updates["opening_hours"]).strip():
            room.set_opening_hours(str(updates["opening_hours"]))
        return True

    def update_room_usage_status(self, room_id: str, is_student_in: bool,
                                 is_equipment_rented: bool) -> bool:
        """Room 5: Update student presence and equipment status."""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.set_is_student_in_room(is_student_in)
        room.set_is_equipment_rented(is_equipment_rented)
        return True

    def update_room_time_slots(self, room_id: str,
                               available_slots: List[str]) -> bool:
        """Room 6: Replace available time slots list."""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.set_available_time_slots(available_slots)
        return True

    def get_predicted_income(self, room_id: str) -> float:
        """Room 7: Calculate predicted income for a room."""
        room = self.find_room(room_id)
        if room is None:
            return 0.0
        return room.calculate_predicted_income()


class AdminController:
    """Administrator management controller.
    Handles: Acct 14 (Admin Info), Room 2 (Promotion),
             Room 9 (Booking Status), Room 10 (Ban Student),
             Room 11 (Equipment Deposit)
    """

    def __init__(self) -> None:
        self.__equipments: List[Equipment] = []

    def get_equipments(self) -> List[Equipment]:
        return self.__equipments

    def get_admin_info(self, admin: Admin) -> Dict[str, str]:
        """Acct 14: Return admin profile fields."""
        return {
            "email": admin.get_email(),
            "first_name": admin.get_first_name(),
            "last_name": admin.get_last_name(),
            "phone": admin.get_phone(),
            "admin_id": admin.get_admin_id()
        }

    def record_promotion_idea(self, admin: Admin, idea: str) -> bool:
        """Room 2: Record a promotion idea."""
        return admin.record_promotion_idea(idea)

    def update_booking_status(self, booking, new_status: str) -> bool:
        """Room 9: Update a booking's status. Valid: confirmed/completed/cancelled."""
        valid_statuses = ["confirmed", "completed", "cancelled"]
        if new_status.lower() not in valid_statuses:
            return False
        booking.set_status(new_status.lower())
        return True

    def ban_student(self, student: Student) -> bool:
        """Room 10: Ban a student. Returns False if already banned."""
        if not student.get_booking_ban_status():
            student.set_booking_ban_status(True)
            return True
        return False

    def unban_student(self, student: Student) -> bool:
        """Room 10: Remove ban. Returns False if not banned."""
        if student.get_booking_ban_status():
            student.set_booking_ban_status(False)
            return True
        return False

    def set_equipment_deposit(self, equipment: Equipment,
                              amount: float) -> bool:
        """Room 11: Set deposit amount; must be positive."""
        if amount <= 0:
            return False
        equipment.set_deposit_amount(amount)
        return True

    def refund_equipment_deposit(self, equipment: Equipment,
                                 student: Student) -> float:
        """Room 11: Refund the deposit to a student."""
        refund = equipment.refund_deposit()
        student.add_funds(refund)
        return refund


# ================================================================
# <<Boundary>> Section
# ================================================================

class AdminMenuUI:
    """Admin main menu and sub-menus.
    Covers: Acct 14, Room 1-11
    """

    @staticmethod
    def show_main_menu(name: str) -> str:
        print(f"\n{'=' * 50}")
        print(f"  Admin Menu — Welcome, {name}")
        print(f"{'=' * 50}")
        print("1.  View Admin Info (Acct 14)")
        print("2.  View All Rooms (Room 3)")
        print("3.  Add a Room (Room 1)")
        print("4.  Remove a Room (Room 4)")
        print("5.  Update Room Info (Room 8)")
        print("6.  Update Room Time Slots (Room 6)")
        print("7.  Update Room Usage Status (Room 5)")
        print("8.  View Predicted Income (Room 7)")
        print("9.  Record Promotion Idea (Room 2)")
        print("10. Update Booking Status (Room 9)")
        print("11. Ban / Unban Student (Room 10)")
        print("12. Equipment Deposit Mgmt (Room 11)")
        print("0.  Logout")
        return input("Select: ").strip()

    @staticmethod
    def show_admin_info(info: dict):
        print("\n--- Admin Info (Acct 14) ---")
        for k, v in info.items():
            print(f"  {k.replace('_', ' ').title()}: {v}")

    @staticmethod
    def get_room_details() -> dict:
        print("\n--- Add Room (Room 1) ---")
        return {
            "name": input("Room name: ").strip(),
            "building": input("Building: ").strip(),
            "capacity": input("Capacity: ").strip(),
            "price": input("Price per hour ($): ").strip(),
            "opening_hours": input("Opening hours (e.g. 09:00-21:00): ").strip()
        }

    @staticmethod
    def get_room_id() -> str:
        return input("Enter Room ID: ").strip()

    @staticmethod
    def get_room_updates() -> dict:
        print("\n--- Update Room (Room 8) — Leave blank to skip ---")
        updates = {}
        n = input("New name: ").strip()
        if n: updates["name"] = n
        b = input("New building: ").strip()
        if b: updates["building"] = b
        c = input("New capacity: ").strip()
        if c: updates["capacity"] = c
        p = input("New price: ").strip()
        if p: updates["price"] = p
        h = input("New opening hours: ").strip()
        if h: updates["opening_hours"] = h
        return updates

    @staticmethod
    def get_time_slots() -> list:
        print("Enter time slots (HH:MM-HH:MM), one per line. Blank to finish:")
        slots = []
        while True:
            s = input("  Slot: ").strip()
            if not s:
                break
            slots.append(s)
        return slots

    @staticmethod
    def get_usage_status() -> tuple:
        sin = input("Student in room? (y/n): ").strip().lower() == "y"
        eq = input("Equipment rented? (y/n): ").strip().lower() == "y"
        return sin, eq

    @staticmethod
    def show_predicted_income(room_id: str, income: float):
        print(f"\n--- Predicted Income (Room 7) ---")
        print(f"  Room {room_id}: ${income:.2f}")

    @staticmethod
    def get_promotion_idea() -> str:
        return input("Enter promotion idea (Room 2): ").strip()

    @staticmethod
    def get_booking_id() -> str:
        return input("Enter Booking ID: ").strip()

    @staticmethod
    def get_new_status() -> str:
        print("New status: [confirmed / completed / cancelled]")
        return input("Status: ").strip()

    @staticmethod
    def get_student_id() -> str:
        return input("Enter Student ID: ").strip()

    @staticmethod
    def get_ban_action() -> str:
        print("1. Ban student")
        print("2. Unban student")
        return input("Select: ").strip()

    @staticmethod
    def get_equipment_menu() -> str:
        print("\n--- Equipment Deposit (Room 11) ---")
        print("1. Set deposit amount")
        print("2. Refund deposit to student")
        print("0. Back")
        return input("Select: ").strip()

    @staticmethod
    def get_deposit_amount() -> float:
        try:
            return float(input("Deposit amount ($): ").strip())
        except ValueError:
            return -1.0

    @staticmethod
    def show_room_list(rooms: list):
        print(f"\n--- Room List ({len(rooms)}) (Room 3) ---")
        if not rooms:
            print("  No rooms in system.")
        for r in rooms:
            print(f"  {r}")
