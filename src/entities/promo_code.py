from typing import List


class PromoCode:

    def __init__(
            self,
            code: str,
            discount_amount: float
    ) -> None:

        self.__code = code
        self.__discount_amount = discount_amount
        self.__used_students: List[str] = []

    def get_code(self) -> str:
        return self.__code

    def get_discount_amount(self) -> float:
        return self.__discount_amount

    def get_used_by_students(self) -> List[str]:
        return self.__used_students

    def set_code(self, code: str) -> None:
        self.__code = code

    def set_discount_amount(self, amount: float) -> None:
        self.__discount_amount = amount

    def is_valid(self) -> bool:
        return self.__code.strip() != ""

    def is_used_by(self, student_id: str) -> bool:
        return student_id in self.__used_students

    def mark_used(self, student_id: str) -> None:
        if not self.is_used_by(student_id):
            self.__used_students.append(student_id)

    def apply_discount(
            self,
            original_price: float
    ) -> float:
        discount = original_price * (self.__discount_amount / 100)

        return max(
            0,
            original_price - discount
        )

