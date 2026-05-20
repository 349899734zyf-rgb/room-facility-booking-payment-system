from src.entities.promo_code import PromoCode


def test_promo_code_stores_code_and_discount():
    promo_code = PromoCode("NEWBEE20", 20.0)

    assert promo_code.get_code() == "NEWBEE20"
    assert promo_code.get_discount_amount() == 20.0


def test_promo_code_is_not_used_by_student_initially():
    promo_code = PromoCode("NEWBEE20", 20.0)

    assert promo_code.is_used_by("S001") is False


def test_mark_used_records_student_usage():
    promo_code = PromoCode("NEWBEE20", 20.0)

    promo_code.mark_used("S001")

    assert promo_code.is_used_by("S001") is True
    assert promo_code.is_used_by("S002") is False
    assert promo_code.get_used_by_students() == ["S001"]


def test_mark_used_does_not_duplicate_same_student():
    promo_code = PromoCode("NEWBEE20", 20.0)

    promo_code.mark_used("S001")
    promo_code.mark_used("S001")

    assert promo_code.get_used_by_students() == ["S001"]


def test_promo_code_setters_and_validation():
    promo_code = PromoCode("NEWBEE20", 20.0)

    promo_code.set_code("WELCOME10")
    promo_code.set_discount_amount(10.0)

    assert promo_code.get_code() == "WELCOME10"
    assert promo_code.get_discount_amount() == 10.0
    assert promo_code.is_valid() is True

    promo_code.set_code("   ")

    assert promo_code.is_valid() is False


def test_apply_discount_reduces_price_without_going_negative():
    promo_code = PromoCode("NEWBEE20", 20.0)

    assert promo_code.apply_discount(20.0) == 16.0
    assert promo_code.apply_discount(15.0) == 12.0
