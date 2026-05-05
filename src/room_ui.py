from typing import Dict, Any
from .base_ui import BaseUI
from .room_service import RoomService

class RoomUI(BaseUI):
    def __init__(self, room_service: RoomService):
        self.room_service = room_service

    def display_add_room_form(self) -> None:
        """显示添加房间的表单"""
        form_fields = ["number", "building", "capacity", "hourly_rate", "has_equipment"]
        initial_values = {
            "number": "",
            "building": "",
            "capacity": 0,
            "hourly_rate": 0.0,
            "has_equipment": False
        }
        self.display_form(form_fields, initial_values)

    def get_new_room_data(self) -> Dict[str, Any]:
        """获取用户在表单中输入的新房间数据"""
        return self.get_form_data()

    def confirm_add_room(self, room_data: Dict[str, Any]) -> bool:
        """确认添加新房间"""
        message = (
            f"房间号: {room_data['number']}\n"
            f"楼栋: {room_data['building']}\n"
            f"容量: {room_data['capacity']}人\n"
            f"价格: {room_data['hourly_rate']}元/小时\n"
            f"有设备: {room_data['has_equipment']}\n"
            "确认添加吗?"
        )
        return self.get_confirmation(message)

    def add_room(self, room_data: Dict[str, Any]) -> None:
        """添加新房间"""
        try:
            self.room_service.add_room(room_data)
            self.display_success_message("房间添加成功")
        except Exception as e:
            self.display_error_message(f"添加房间失败: {str(e)}")
