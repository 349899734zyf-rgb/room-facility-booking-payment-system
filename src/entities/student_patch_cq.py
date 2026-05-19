"""
Student class patch from CQ (Branch_CQ).
This records CQ's modification to the shared Student class in entity_classes.py.
Apply this change when building the final entities/student.py.

--- Original (master) ---
def mark_promo_code_used(self, code: str) -> None:
    self.__used_promo_codes.append(code)

--- Modified (CQ) ---
def mark_promo_code_used(self, code: str) -> None:
    if not self.has_used_promo_code(code):
        self.__used_promo_codes.append(code)

Purpose: Prevent duplicate promo code records for the same student.
"""
