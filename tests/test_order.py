from src.entities.order import Order


class DummyBooking:
    pass


def test_order_stores_booking_payment_method_and_initial_price():
    booking = DummyBooking()
    order = Order("OD0001", booking, 20.0, "balance")

    assert order.get_order_id() == "OD0001"
    assert order.get_booking() is booking
    assert order.get_price() == 20.0
    assert order.get_payment_method() == "balance"
    assert order.get_promo_discount() == 0
    assert order.get_promo_code_used() is None
    assert order.get_final_price() == 20.0


def test_set_promo_discount_reduces_final_price():
    order = Order("OD0001", DummyBooking(), 20.0, "balance")

    order.set_promo_discount(20.0)

    assert order.get_final_price() == 0


def test_set_promo_discount_does_not_make_final_price_negative():
    order = Order("OD0001", DummyBooking(), 15.0, "balance")

    order.set_promo_discount(20.0)

    assert order.get_final_price() == 0


def test_calculate_final_price_uses_current_discount():
    order = Order("OD0001", DummyBooking(), 20.0, "balance")
    order.set_promo_discount(15.0)

    final_price = order.calculate_final_price()

    assert final_price == 5.0
    assert order.get_final_price() == 5.0


def test_set_payment_method_updates_method():
    order = Order("OD0001", DummyBooking(), 20.0, "balance")

    order.set_payment_method("deal_package")

    assert order.get_payment_method() == "deal_package"


def test_set_promo_code_used_updates_code():
    order = Order("OD0001", DummyBooking(), 20.0, "balance")

    order.set_promo_code_used("NEWBEE20")

    assert order.get_promo_code_used() == "NEWBEE20"
