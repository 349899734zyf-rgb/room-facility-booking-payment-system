from src.entities.order import Order


class DummyBooking:
    pass


def test_order_stores_booking_payment_method_and_initial_price():
    booking = DummyBooking()
    order = Order("OD0001", booking, 50.0, "balance")

    assert order.get_booking() is booking
    assert order.get_payment_method() == "balance"
    assert order.get_final_price() == 50.0


def test_set_promo_discount_reduces_final_price():
    order = Order("OD0001", DummyBooking(), 50.0, "balance")

    order.set_promo_discount(20.0)

    assert order.get_final_price() == 30.0


def test_set_promo_discount_does_not_make_final_price_negative():
    order = Order("OD0001", DummyBooking(), 15.0, "balance")

    order.set_promo_discount(20.0)

    assert order.get_final_price() == 0
