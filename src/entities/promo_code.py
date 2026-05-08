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

    def is_used_by(self, student_id: str) -> bool:
        return student_id in self.__used_students

    def mark_used(self, student_id: str) -> None:
        self.__used_students.append(student_id)