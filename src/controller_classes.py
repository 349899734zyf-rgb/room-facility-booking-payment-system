from typing import List, Optional, Dict
from datetime import datetime, timedelta
from entity_classes import (User, Student, Admin, Room, Booking,
                            PromoCode, DealPackage, Equipment, ActivityRecord, Order)


class AuthController:
    """认证控制器 (Account Management 1-4, 6-7, 13-15)"""

    def __init__(self) -> None:
        self.__students: List[Student] = []
        self.__admins: List[Admin] = []

    def get_students(self) -> List[Student]:
        return self.__students

    def get_admins(self) -> List[Admin]:
        return self.__admins

    def validate_email(self, email: str) -> bool:
        return email.endswith("@student.monash.edu")

    def validate_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_upper and has_digit

    def validate_mobile(self, mobile: str) -> bool:
        return len(mobile) == 10 and mobile.startswith("04") and mobile.isdigit()

    def register_student(self, email: str, password: str, first_name: str,
                         last_name: str, phone: str, student_id: str) -> Optional[Student]:
        if not all([email, password, first_name, last_name, phone, student_id]):
            return None
        if not self.validate_email(email):
            return None
        if not self.validate_password(password):
            return None
        student = Student(email, password, first_name, last_name, phone, student_id)
        self.__students.append(student)
        return student

    def login(self, email: str, password: str) -> Optional[User]:
        """login"""
        for s in self.__students:
            if s.get_email() == email and s.verify_password(password):
                return s
        for a in self.__admins:
            if a.get_email() == email and a.verify_password(password):
                return a
        return None

    def identify_role(self, user: User) -> str:
        """角色识别 (Acct 13)"""
        return user.get_role()

    def change_password(self, user: User, current_pwd: str, new_pwd: str, confirm_pwd: str) -> bool:
        """修改密码 (Acct 7)"""
        if not user.verify_password(current_pwd):
            return False
        if new_pwd != confirm_pwd:
            return False
        if not self.validate_password(new_pwd):
            return False
        user.set_password(new_pwd)
        return True

    def update_mobile(self, user: User, new_mobile: str, confirm_mobile: str) -> bool:
        """更新手机号 (Acct 6)"""
        if new_mobile != confirm_mobile:
            return False
        if not self.validate_mobile(new_mobile):
            return False
        user.set_phone(new_mobile)
        return True


class BookingController:
    """预定控制器 (Booking Management 1-15)"""

    def __init__(self) -> None:
        self.__rooms: List[Room] = []
        self.__all_bookings: List[Booking] = []
        self.__booking_counter: int = 0

    def get_rooms(self) -> List[Room]:
        return self.__rooms

    def get_all_bookings(self) -> List[Booking]:
        return self.__all_bookings

    def find_booking(self, booking_id: str) -> Optional[Booking]:
        """查找特定预订 (Story 2.9)"""
        for booking in self.__all_bookings:
            if booking.get_booking_id() == booking_id:
                return booking
        return None

    def search_rooms(self, building: str, start_time: str, end_time: str) -> List[Room]:
        """搜索可用房间 (Book 1)"""
        result = []
        for room in self.__rooms:
            if room.get_building() == building and room.is_available(start_time, end_time):
                result.append(room)
        return result

    def validate_duration(self, start_time: datetime, end_time: datetime) -> bool:
        """验证预定时长规则 (Book 8): >=1h, 30min增量"""
        duration = (end_time - start_time).total_seconds() / 3600
        if duration < 1.0:
            return False
        if (duration * 2) != int(duration * 2):
            return False
        return True

    def check_eligibility(self, student: Student) -> Dict[str, bool]:
        """检查预定资格 (Book 7)"""
        return {
            "is_eligible": student.is_eligible_to_book(),
            "is_banned": student.get_booking_ban_status(),
            "has_reached_limit": student.has_reached_booking_limit()
        }

    def create_booking(self, student: Student, room: Room, start_time: datetime,
                       end_time: datetime, equipment_rental: bool) -> Optional[Booking]:
        """创建预定 (Book 15, Checkout 10)"""
        if not student.is_eligible_to_book():
            return None
        if student.has_reached_booking_limit():
            return None
        if not self.validate_duration(start_time, end_time):
            return None
        duration = (end_time - start_time).total_seconds() / 3600
        total_price = duration * room.get_price_per_hour()
        self.__booking_counter += 1
        bid = f"BK{self.__booking_counter:04d}"
        booking = Booking(bid, student, room, start_time, end_time, equipment_rental, total_price)
        self.__all_bookings.append(booking)
        student.add_booking(booking)
        room.update_availability(f"{start_time}-{end_time}", False)
        return booking

    def cancel_booking(self, student: Student, booking: Booking) -> Dict[str, object]:
        """取消预定 (Book 2, Book 3)"""
        cancel_type = booking.cancel()
        result = {"type": cancel_type, "refund": 0.0}
        if cancel_type == "regular_cancellation":
            result["refund"] = booking.get_total_price()
            student.add_funds(booking.get_total_price())
        else:
            student.record_late_cancellation()
        student.remove_booking(booking)
        room = booking.get_room()
        st = booking.get_start_time()
        et = booking.get_end_time()
        room.update_availability(f"{st}-{et}", True)
        return result

    def get_student_bookings(self, student: Student) -> List[Booking]:
        """获取学生预定列表 (Book 11-3.12)"""
        return student.get_active_bookings()


class PaymentController:
    """支付控制器 (Checkout and Booking Handling 1-11)"""

    def __init__(self) -> None:
        self.__promo_codes: List[PromoCode] = []
        self.__deal_package: DealPackage = DealPackage("DP001", 100.0, 12.0)
        self.__order_counter: int = 0

    def get_promo_codes(self) -> List[PromoCode]:
        return self.__promo_codes

    def get_deal_package(self) -> DealPackage:
        return self.__deal_package

    def pay_by_balance(self, student: Student, amount: float) -> bool:
        """余额支付 (Checkout 2)"""
        return student.deduct_balance(amount)

    def check_balance_sufficient(self, student: Student, amount: float) -> bool:
        """检查余额是否充足 (Checkout 2)"""
        return student.get_balance() >= amount

    def pay_by_deal_package(self, student: Student, hours: float,
                            has_equipment: bool) -> bool:
        """套餐支付 (Checkout 5, Checkout 6)"""
        if has_equipment:
            return False
        return student.deduct_deal_package_hours(hours)

    def validate_promo_code(self, code: str, student: Student) -> Optional[PromoCode]:
        """验证优惠码 (Checkout 4-4.5)"""
        for pc in self.__promo_codes:
            if pc.get_code() == code:
                if pc.is_used_by(student.get_student_id()):
                    return None
                return pc
        return None

    def apply_promo_code(self, promo: PromoCode, student: Student,
                         order: Order) -> float:
        """应用优惠码 (Checkout 4)"""
        discount = promo.get_discount_amount()
        order.set_promo_discount(discount)
        promo.mark_used(student.get_student_id())
        student.mark_promo_code_used(promo.get_code())
        return order.get_final_price()

    def purchase_deal_package(self, student: Student) -> bool:
        """购买套餐 (Checkout 7)"""
        if student.deduct_balance(self.__deal_package.get_price()):
            student.add_deal_package_hours(self.__deal_package.get_hours())
            return True
        return False

    def create_order(self, booking: Booking, payment_method: str) -> Order:
        """创建订单 (Checkout 9)"""
        self.__order_counter += 1
        oid = f"OD{self.__order_counter:04d}"
        order = Order(oid, booking, booking.get_total_price(), payment_method)
        return order

    def confirm_order(self, order: Order, student: Student) -> bool:
        """确认订单 (Checkout 10)"""
        booking = order.get_booking()
        booking.set_payment_method(order.get_payment_method())
        booking.set_status("confirmed")
        return True

    def can_use_deal_package(self, has_equipment: bool) -> bool:
        """检查套餐支付限制 (Checkout 6)"""
        return not has_equipment


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


class AccountController:
    """账户控制器 (Account Management 5, 8-12)"""

    def __init__(self) -> None:
        pass

    def get_profile_info(self, student: Student) -> Dict[str, object]:
        """获取个人资料 (Acct 5)"""
        return {
            "first_name": student.get_first_name(),
            "last_name": student.get_last_name(),
            "student_id": student.get_student_id(),
            "email": student.get_email(),
            "phone": student.get_phone(),
            "balance": student.get_balance()
        }

    def get_usage_status(self, student: Student) -> Dict[str, object]:
        """获取使用状态 (Acct 8)"""
        return {
            "current_bookings": student.get_active_bookings(),
            "ban_status": student.get_booking_ban_status(),
            "balance": student.get_balance(),
            "deal_package_hours": student.get_deal_package_hours()
        }

    def get_activity_history(self, student: Student, page: int) -> List:
        """获取活动历史 (Acct 9-1.10)"""
        return student.get_activity_history_page(page)

    def get_funds_summary(self, student: Student) -> Dict[str, float]:
        """获取资金摘要 (Acct 11)"""
        return {"balance": student.get_balance()}

    def add_funds(self, student: Student, amount: float) -> bool:
        """充值 (Acct 12)"""
        return student.add_funds(amount)


class AdminController:
    """管理员控制器 (Room Management 2, 9-11)"""

    class AdminController:
        """管理员控制器 (Room Management 2, 9-11)"""

    def __init__(self) -> None:
        self.__all_bookings: List[Booking] = []
        self.__equipments: List[Equipment] = []
        self.__students: List[Student] = []  # 【新增】

    def get_all_bookings(self) -> List[Booking]:
        return self.__all_bookings

    def set_all_bookings(self, bookings: List[Booking]) -> None:
        self.__all_bookings = bookings

    def get_equipments(self) -> List[Equipment]:
        return self.__equipments

    def get_all_students(self) -> List[Student]:
        """获取所有学生 (Story 2.10)"""
        return self.__students

    def set_all_students(self, students: List[Student]) -> None:
        """设置学生列表"""
        self.__students = students

    def add_student(self, student: Student) -> None:
        """添加学生"""
        self.__students.append(student)

    def find_student(self, student_id: str) -> Optional[Student]:
        """查找特定学生 (Story 2.10)"""
        for student in self.__students:
            if student.get_student_id() == student_id:
                return student
        return None

    def get_admin_info(self, admin: Admin) -> Dict[str, str]:
        """获取管理员信息 (Account Management 14)"""
        return {
            "email": admin.get_email(),
            "first_name": admin.get_first_name(),
            "last_name": admin.get_last_name(),
            "phone": admin.get_phone()
        }

    def record_promotion_idea(self, admin: Admin, idea: str) -> bool:
        """记录推广创意 (Room Management 2)"""
        return admin.record_promotion_idea(idea)

    def update_booking_status(self, booking_id: str, new_status: str) -> bool:
        """更新预定状态 (Room Management 9)"""
        for b in self.__all_bookings:
            if b.get_booking_id() == booking_id:
                b.set_status(new_status)
                return True
        return False

    def ban_student(self, student: Student) -> bool:
        """封禁学生预定资格 (Room Management 10)"""
        if not student.get_booking_ban_status():
            student.set_booking_ban_status(True)
            return True
        return False

    def unban_student(self, student: Student) -> bool:
        """解除学生封禁 (Room Management 10)"""
        if student.get_booking_ban_status():
            student.set_booking_ban_status(False)
            return True
        return False

    def get_all_equipment(self) -> List[Equipment]:
        """获取所有设备 (Story 2.11)"""
        return self.__equipments

    def find_equipment(self, equipment_id: str) -> Optional[Equipment]:
        """查找特定设备 (Story 2.11)"""
        for equipment in self.__equipments:
            if equipment.get_equipment_id() == equipment_id:
                return equipment
        return None

    def set_equipment_deposit(self, equipment: Equipment, amount: float) -> bool:
        """设置设备押金金额 (Room Management 11)"""
        if amount <= 0:
            return False
        equipment.set_deposit_amount(amount)
        return True

    def refund_equipment_deposit(self, equipment: Equipment, student: Student) -> bool:
        """退还设备押金 (Room Management 11)"""
        refund = equipment.refund_deposit()
        student.add_funds(refund)
        return True