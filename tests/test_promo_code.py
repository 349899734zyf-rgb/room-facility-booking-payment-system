from src.entities.promo_code import PromoCode


def test_promo_code_stores_code_and_discount():
    promo_code = PromoCode("SAVE20", 20.0)

    assert promo_code.get_code() == "SAVE20"
    assert promo_code.get_discount_amount() == 20.0


def test_promo_code_is_not_used_by_student_initially():
    promo_code = PromoCode("SAVE20", 20.0)

    assert promo_code.is_used_by("S001") is False


def test_mark_used_records_student_usage():
    promo_code = PromoCode("SAVE20", 20.0)

    promo_code.mark_used("S001")

    assert promo_code.is_used_by("S001") is True
    assert promo_code.is_used_by("S002") is False
