from src.boundary.payment_ui import PaymentUI


def test_display_payment_options_shows_price_duration_and_choices(capsys):
    ui = PaymentUI()

    ui.display_payment_options(price=50.0, duration=2)

    output = capsys.readouterr().out
    assert "===== PAYMENT =====" in output
    assert "Price: $50.0" in output
    assert "Duration: 2 hours" in output
    assert "1. Balance Payment" in output
    assert "2. Deal Package" in output


def test_get_payment_method_choice_returns_user_input(monkeypatch):
    ui = PaymentUI()
    monkeypatch.setattr("builtins.input", lambda prompt: "1")

    choice = ui.get_payment_method_choice()

    assert choice == "1"


def test_get_promo_code_input_returns_user_input(monkeypatch):
    ui = PaymentUI()
    monkeypatch.setattr("builtins.input", lambda prompt: "SAVE20")

    promo_code = ui.get_promo_code_input()

    assert promo_code == "SAVE20"


def test_display_promo_code_valid_shows_new_price(capsys):
    ui = PaymentUI()

    ui.display_promo_code_valid(new_price=30.0)

    assert capsys.readouterr().out == "Promo applied. New price: $30.0\n"


def test_display_promo_code_invalid_message(capsys):
    ui = PaymentUI()

    ui.display_promo_code_invalid_message()

    assert capsys.readouterr().out == "Invalid promo code\n"


def test_display_promo_code_used_message(capsys):
    ui = PaymentUI()

    ui.display_promo_code_used_message()

    assert capsys.readouterr().out == "Promo code already used\n"


def test_display_booking_confirmed(capsys):
    ui = PaymentUI()

    ui.display_booking_confirmed()

    assert capsys.readouterr().out == "Booking confirmed\n"


def test_display_insufficient_balance_message(capsys):
    ui = PaymentUI()

    ui.display_insufficient_balance_message()

    assert capsys.readouterr().out == "Insufficient balance\n"


def test_display_insufficient_deal_hours_message(capsys):
    ui = PaymentUI()

    ui.display_insufficient_deal_hours_message()

    assert capsys.readouterr().out == "Not enough package hours\n"
