class Room:
    def __init__(self, name, room_type, area, floor, description=""):
        self.name = name
        self.room_type = room_type
        self.area = area
        self.floor = floor
        self.description = description
        self.id = None