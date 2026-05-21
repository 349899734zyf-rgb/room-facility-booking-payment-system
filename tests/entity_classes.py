from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

class User(ABC):
    def __init__(self, email: str, password: str, first_name: str, last_name: str, phone: str) -> None:
        self.__email: str = email
        self.__password: str = password
        self.__first_name: str = first_name
        self.__last_name: str = last_name
        self.__phone: str = phone

    # --- Accessors ---
    def get_email(self) -> str:
        return self.__email

    def get_password(self) -> str:
        return self.__password

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def get_phone(self) -> str:
        return self.__phone

    # --- Mutators ---
    def set_email(self, email: str) -> None:
        self.__email = email

    def set_password(self, password: str) -> None:
        self.__password = password

    def set_first_name(self, first_name: str) -> None:
        self.__first_name = first_name

    def set_last_name(self, last_name: str) -> None:
        self.__last_name = last_name

    def set_phone(self, phone: str) -> None:
        self.__phone = phone

    # --- Business Methods ---
    @abstractmethod
    def get_role(self) -> str:
        pass

    def verify_password(self, input_password: str) -> bool:
        return self.__password == input_password

    def __str__(self) -> str:
        return f"User({self.__email}, {self.__first_name} {self.__last_name})"


class Student(User):
    """学生实体类 (Account Management 1-13, Booking, Checkout)"""

    def __init__(self, email: str, password: str, first_name: str, last_name: str,
                 phone: str, student_id: str) -> None:
        super().__init__(email, password, first_name, last_name, phone)
        self.__student_id: str = student_id
        self.__balance: float = 0.0
        self.__booking_ban_status: bool = False
        self.__late_cancellation_count: int = 0
        self.__no_show_count: int = 0
        self.__deal_package_hours: float = 0.0
        self.__bookings: List['Booking'] = []
        self.__activity_history: List['ActivityRecord'] = []
        self.__used_promo_codes: List[str] = []

    # --- Accessors ---
    def get_student_id(self) -> str:
        return self.__student_id

    def get_balance(self) -> float:
        return self.__balance

    def get_booking_ban_status(self) -> bool:
        return self.__booking_ban_status

    def get_late_cancellation_count(self) -> int:
        return self.__late_cancellation_count

    def get_no_show_count(self) -> int:
        return self.__no_show_count

    def get_deal_package_hours(self) -> float:
        return self.__deal_package_hours

    def get_bookings(self) -> List['Booking']:
        return self.__bookings

    def get_activity_history(self) -> List['ActivityRecord']:
        return self.__activity_history

    def get_used_promo_codes(self) -> List[str]:
        return self.__used_promo_codes

    # --- Mutators ---
    def set_student_id(self, student_id: str) -> None:
        self.__student_id = student_id

    def set_balance(self, balance: float) -> None:
        self.__balance = balance

    def set_booking_ban_status(self, status: bool) -> None:
        self.__booking_ban_status = status

    def set_late_cancellation_count(self, count: int) -> None:
        self.__late_cancellation_count = count

    def set_no_show_count(self, count: int) -> None:
        self.__no_show_count = count

    def set_deal_package_hours(self, hours: float) -> None:
        self.__deal_package_hours = hours

    # --- Business Methods ---
    def get_role(self) -> str:
        return "student"

    def add_funds(self, amount: float) -> bool:
        """充值 (Acct 12)"""
        if amount <= 0:
            return False
        self.__balance += amount
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "recharge", f"Added ${amount}", amount))
        return True

    def deduct_balance(self, amount: float) -> bool:
        """扣除余额"""
        if self.__balance >= amount:
            self.__balance -= amount
            return True
        return False

    def is_eligible_to_book(self) -> bool:
        """检查预定资格 (Book 7)"""
        return not self.__booking_ban_status

    def has_reached_booking_limit(self) -> bool:
        """检查是否达到预定上限 (Book 10): 最多3个"""
        active = [b for b in self.__bookings if b.get_status() == "confirmed"]
        return len(active) >= 3

    def add_booking(self, booking: 'Booking') -> None:
        """添加预定到列表"""
        self.__bookings.append(booking)
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "booking", str(booking), booking.get_total_price()))

    def remove_booking(self, booking: 'Booking') -> None:
        """移除预定"""
        if booking in self.__bookings:
            self.__bookings.remove(booking)

    def record_late_cancellation(self) -> None:
        """记录迟到取消 (Book 3)"""
        self.__late_cancellation_count += 1
        self.__activity_history.append(
            ActivityRecord(datetime.now(), "late_cancellation", "Late cancellation recorded", 0.0))
        self._check_ban_threshold()

    def record_no_show(self) -> None:
        """记录缺席"""
        self.__no_show_count += 1
        self._check_ban_threshold()

    def _check_ban_threshold(self) -> None:
        """检查是否需要封禁"""
        if (self.__late_cancellation_count + self.__no_show_count) >= 3:
            self.__booking_ban_status = True

    def add_deal_package_hours(self, hours: float) -> None:
        """添加套餐时长 (Checkout 7)"""
        self.__deal_package_hours += hours

    def deduct_deal_package_hours(self, hours: float) -> bool:
        """扣除套餐时长 (Checkout 5)"""
        if self.__deal_package_hours >= hours:
            self.__deal_package_hours -= hours
            return True
        return False

    def has_used_promo_code(self, code: str) -> bool:
        """检查优惠码是否已使用 (Checkout 4)"""
        return code in self.__used_promo_codes

    def mark_promo_code_used(self, code: str) -> None:
        """标记优惠码已使用"""
        if not self.has_used_promo_code(code):
            self.__used_promo_codes.append(code)

    def get_active_bookings(self) -> List['Booking']:
        """获取有效预定列表"""
        return [b for b in self.__bookings if b.get_status() == "confirmed"]

    def get_activity_history_page(self, page: int, page_size: int = 10) -> List['ActivityRecord']:
        """分页获取活动历史 (Acct 10)"""
        start = (page - 1) * page_size
        end = start + page_size
        return self.__activity_history[start:end]


class Admin(User):
    """管理员实体类 (Account Management 14-15, Room Management 1-11)"""

    def __init__(self, email: str, password: str, first_name: str, last_name: str,
                 phone: str, admin_id: str) -> None:
        super().__init__(email, password, first_name, last_name, phone)
        self.__admin_id: str = admin_id
        self.__promotion_ideas: List[str] = []

    # --- Accessors ---
    def get_admin_id(self) -> str:
        return self.__admin_id

    def get_promotion_ideas(self) -> List[str]:
        return self.__promotion_ideas

    # --- Mutators ---
    def set_admin_id(self, admin_id: str) -> None:
        self.__admin_id = admin_id

    # --- Business Methods ---
    def get_role(self) -> str:
        return "admin"

    def record_promotion_idea(self, idea: str) -> bool:
        """记录推广创意 (Room 2)"""
        if idea.strip():
            self.__promotion_ideas.append(idea)
            return True
        return False


class Room:
    """房间实体类 (Room Management 1, 4-8, Booking Management 1)"""

    def __init__(self, room_id: str, room_name: str, building: str,
                 capacity: int, price_per_hour: float, opening_hours: str) -> None:
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
    def is_available(self, start_time: str, end_time: str) -> bool:
        """检查房间在指定时段是否可用 (Book 1)"""
        time_slot = f"{start_time}-{end_time}"
        return time_slot in self.__available_time_slots

    def calculate_predicted_income(self) -> float:
        """计算预测收入 (Room 7)"""
        booked_slots = len(self.__available_time_slots)
        income = booked_slots * self.__price_per_hour
        if self.__is_equipment_rented:
            income += 10.0  # equipment rental fee
        return income

    def update_availability(self, time_slot: str, available: bool) -> None:
        """更新可用时段 (Room 5/6)"""
        if available and time_slot not in self.__available_time_slots:
            self.__available_time_slots.append(time_slot)
        elif not available and time_slot in self.__available_time_slots:
            self.__available_time_slots.remove(time_slot)


class Booking:
    """预定实体类 (Booking Management 2-3, 5-6, 15, Checkout 10)"""

    def __init__(self, booking_id: str, student: Student, room: Room,
                 start_time: datetime, end_time: datetime,
                 equipment_rental: bool, total_price: float) -> None:
        self.__booking_id: str = booking_id
        self.__student: Student = student
        self.__room: Room = room
        self.__start_time: datetime = start_time
        self.__end_time: datetime = end_time
        self.__equipment_rental: bool = equipment_rental
        self.__total_price: float = total_price
        self.__status: str = "confirmed"  # confirmed / cancelled / completed
        self.__payment_method: str = ""
        self.__promo_code_used: Optional[str] = None

    # --- Accessors ---
    def get_booking_id(self) -> str:
        return self.__booking_id

    def get_student(self) -> Student:
        return self.__student

    def get_room(self) -> Room:
        return self.__room

    def get_start_time(self) -> datetime:
        return self.__start_time

    def get_end_time(self) -> datetime:
        return self.__end_time

    def get_equipment_rental(self) -> bool:
        return self.__equipment_rental

    def get_total_price(self) -> float:
        return self.__total_price

    def get_status(self) -> str:
        return self.__status

    def get_payment_method(self) -> str:
        return self.__payment_method

    def get_promo_code_used(self) -> Optional[str]:
        return self.__promo_code_used

    # --- Mutators ---
    def set_status(self, status: str) -> None:
        self.__status = status

    def set_payment_method(self, method: str) -> None:
        self.__payment_method = method

    def set_promo_code_used(self, code: str) -> None:
        self.__promo_code_used = code

    def set_total_price(self, price: float) -> None:
        self.__total_price = price

    # --- Business Methods ---
    def calculate_duration_hours(self) -> float:
        """计算预定时长（小时）"""
        delta = self.__end_time - self.__start_time
        return delta.total_seconds() / 3600

    def is_late_cancellation(self) -> bool:
        """判断是否为迟到取消 (Book 3): 开始前30分钟内"""
        from datetime import timedelta
        remaining = self.__start_time - datetime.now()
        return remaining <= timedelta(minutes=30)

    def cancel(self) -> str:
        """取消预定并返回取消类型 (Book 2, Book 3)"""
        self.__status = "cancelled"
        if self.is_late_cancellation():
            return "late_cancellation"
        return "regular_cancellation"


class PromoCode:
    """优惠码实体类 (Checkout 4)"""

    def __init__(self, code: str, discount_amount: float) -> None:
        self.__code: str = code
        self.__discount_amount: float = discount_amount
        self.__used_by_students: List[str] = []

    # --- Accessors ---
    def get_code(self) -> str:
        return self.__code

    def get_discount_amount(self) -> float:
        return self.__discount_amount

    def get_used_by_students(self) -> List[str]:
        return self.__used_by_students

    # --- Mutators ---
    def set_code(self, code: str) -> None:
        self.__code = code

    def set_discount_amount(self, amount: float) -> None:
        self.__discount_amount = amount

    # --- Business Methods ---
    def is_valid(self) -> bool:
        """验证优惠码是否有效"""
        return self.__code.strip() != ""

    def is_used_by(self, student_id: str) -> bool:
        """检查学生是否已使用过 (Checkout 4)"""
        return student_id in self.__used_by_students

    def mark_used(self, student_id: str) -> None:
        """标记为已使用"""
        if not self.is_used_by(student_id):
            self.__used_by_students.append(student_id)

    def apply_discount(self, original_price: float) -> float:
        """应用折扣 (Checkout 4)"""
        discount = original_price * (self.__discount_amount / 100)
        return max(0, original_price - discount)


class DealPackage:
    """套餐实体类 (Checkout 3, 5, 7)"""

    def __init__(self, package_id: str, price: float = 100.0, hours: float = 12.0) -> None:
        self.__package_id: str = package_id
        self.__price: float = price
        self.__hours: float = hours

    # --- Accessors ---
    def get_package_id(self) -> str:
        return self.__package_id

    def get_price(self) -> float:
        return self.__price

    def get_hours(self) -> float:
        return self.__hours

    # --- Mutators ---
    def set_package_id(self, pid: str) -> None:
        self.__package_id = pid

    def set_price(self, price: float) -> None:
        self.__price = price

    def set_hours(self, hours: float) -> None:
        self.__hours = hours


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


class ActivityRecord:
    """活动记录实体类 (Account Management 9-10)"""

    def __init__(self, date: datetime, record_type: str, details: str, amount: float) -> None:
        self.__date: datetime = date
        self.__record_type: str = record_type  # booking/recharge/late_cancellation/no_show
        self.__details: str = details
        self.__amount: float = amount

    # --- Accessors ---
    def get_date(self) -> datetime:
        return self.__date

    def get_record_type(self) -> str:
        return self.__record_type

    def get_details(self) -> str:
        return self.__details

    def get_amount(self) -> float:
        return self.__amount

    # --- Mutators ---
    def set_date(self, date: datetime) -> None:
        self.__date = date

    def set_record_type(self, record_type: str) -> None:
        self.__record_type = record_type

    def set_details(self, details: str) -> None:
        self.__details = details

    def set_amount(self, amount: float) -> None:
        self.__amount = amount

    def __str__(self) -> str:
        return f"[{self.__date}] {self.__record_type}: {self.__details} (${self.__amount})"


class Order:
    """订单实体类 (Checkout 9-10)"""

    def __init__(self, order_id: str, booking: Booking, price: float,
                 payment_method: str) -> None:
        self.__order_id: str = order_id
        self.__booking: Booking = booking
        self.__price: float = price
        self.__promo_discount: float = 0.0
        self.__final_price: float = price
        self.__payment_method: str = payment_method
        self.__promo_code_used: Optional[str] = None

    # --- Accessors ---
    def get_order_id(self) -> str:
        return self.__order_id

    def get_booking(self) -> Booking:
        return self.__booking

    def get_price(self) -> float:
        return self.__price

    def get_promo_discount(self) -> float:
        return self.__promo_discount

    def get_final_price(self) -> float:
        return self.__final_price

    def get_payment_method(self) -> str:
        return self.__payment_method

    def get_promo_code_used(self) -> Optional[str]:
        return self.__promo_code_used

    # --- Mutators ---
    def set_promo_discount(self, discount: float) -> None:
        self.__promo_discount = discount
        self.__final_price = max(0, self.__price - discount)

    def set_payment_method(self, method: str) -> None:
        self.__payment_method = method

    def set_promo_code_used(self, code: str) -> None:
        self.__promo_code_used = code

    # --- Business Methods ---
    def calculate_final_price(self) -> float:
        """计算最终价格 (Checkout 4)"""
        self.__final_price = max(0, self.__price - self.__promo_discount)
        return self.__final_price
