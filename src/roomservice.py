from typing import Dict, Any

class RoomService:
    def __init__(self, room_repository):
        self.room_repository = room_repository

    def add_room(self, room_data: Dict[str, Any]) -> None:
        """添加新房间"""
        new_room = Room(**room_data)
        self.room_repository.save(new_room)
