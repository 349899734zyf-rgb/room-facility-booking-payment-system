"""
RoomController.
Covers: Room 1, 3-8
"""
from typing import List, Dict, Optional


class RoomController:
    """房间控制器 (Room Management 1, 3-8)"""

    def __init__(self) -> None:
        self.__rooms: List[Room] = []
        self.__room_counter: int = 0

    def get_rooms(self) -> List[Room]:
        return self.__rooms

    def add_room(self, name: str, building: str, capacity: int,
                 price: float, opening_hours: str) -> Optional[Room]:
        """添加房间 (Room 1)"""
        if not all([name, building, opening_hours]) or capacity <= 0 or price <= 0:
            return None
        self.__room_counter += 1
        rid = f"RM{self.__room_counter:04d}"
        room = Room(rid, name, building, capacity, price, opening_hours)
        self.__rooms.append(room)
        return room

    def remove_room(self, room_id: str) -> bool:
        """移除房间 (Room 4)"""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                self.__rooms.remove(room)
                return True
        return False

    def find_room(self, room_id: str) -> Optional[Room]:
        """查找房间"""
        for room in self.__rooms:
            if room.get_room_id() == room_id:
                return room
        return None

    def update_room_info(self, room_id: str, updates: Dict[str, object]) -> bool:
        """更新房间信息 (Room 8)"""
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
        return True

    def update_room_usage_status(self, room_id: str, is_student_in: bool,
                                 is_equipment_rented: bool) -> bool:
        """更新房间学生/设备在场状态 (Room Management 5)"""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.set_is_student_in_room(is_student_in)
        room.set_is_equipment_rented(is_equipment_rented)
        return True

    def update_room_time_slots(self, room_id: str, available_slots: List[str]) -> bool:
        """更新房间可用时段 (Room Management 6)"""
        room = self.find_room(room_id)
        if room is None:
            return False
        room.set_available_time_slots(available_slots)
        return True

    def get_predicted_income(self, room_id: str) -> float:
        """获取房间预测收入 (Room 7)"""
        room = self.find_room(room_id)
        if room is None:
            return 0.0
        return room.calculate_predicted_income()

