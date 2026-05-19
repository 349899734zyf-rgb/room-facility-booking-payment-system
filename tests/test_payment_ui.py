from src.boundary.payment_ui import DealPackageUI, PaymentUI


def test_display_payment_options_shows_price_duration_and_choices(capsys):
    ui = PaymentUI()

    ui.display_payment_options(price=20.0, duration=2)

    output = capsys.readouterr().out
    assert "===== PAYMENT =====" in output
    assert "Price: $20.0" in output
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
    monkeypatch.setattr("builtins.input", lambda prompt: "NEWBEE20")

    promo_code = ui.get_promo_code_input()

    assert promo_code == "NEWBEE20"


def test_display_promo_code_valid_shows_new_price(capsys):
    ui = PaymentUI()

    ui.display_promo_code_valid(new_price=30.0)

    assert capsys.readouterr().out == "Promo applied. New price: $30.0\n"


def test_display_balance_payment_info(capsys):
    ui = PaymentUI()

    ui.display_balance_payment_info(price=20.0, balance=80.0)

    output = capsys.readouterr().out
    assert "Price: $20.0" in output
    assert "Current balance: $80.0" in output


def test_display_deal_package_info(capsys):
    ui = PaymentUI()

    ui.display_deal_package_info(duration=2.0, remaining=5.0)

    output = capsys.readouterr().out
    assert "Required hours: 2.0" in output
    assert "Remaining package hours: 5.0" in output


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


def test_display_equipment_restriction_message(capsys):
    ui = PaymentUI()

    ui.display_equipment_restriction_message()

    assert capsys.readouterr().out == "Deal package cannot be used with equipment rental\n"


def test_display_promo_deal_package_restriction_message(capsys):
    ui = PaymentUI()

    ui.display_promo_deal_package_restriction_message()

    assert capsys.readouterr().out == "Promo code cannot be used with deal package\n"


def test_display_booking_summary(capsys):
    ui = PaymentUI()

    ui.display_booking_summary(
        name="Test Student",
        room="Study Room",
        building="Clayton",
        time_period="10:00-12:00",
        price=20.0,
        equipment=True
    )

    output = capsys.readouterr().out
    assert "===== BOOKING SUMMARY =====" in output
    assert "Name: Test Student" in output
    assert "Room: Study Room" in output
    assert "Building: Clayton" in output
    assert "Time: 10:00-12:00" in output
    assert "Price: $20.0" in output
    assert "Equipment rental: Yes" in output


def test_next_step_options_and_choice(capsys, monkeypatch):
    ui = PaymentUI()
    monkeypatch.setattr("builtins.input", lambda prompt: "2")

    ui.display_next_step_options()
    choice = ui.get_next_step_choice()

    output = capsys.readouterr().out
    assert "1. View my bookings" in output
    assert "2. Return to home" in output
    assert choice == "2"


def test_deal_package_ui_displays_and_confirms_purchase(capsys, monkeypatch):
    ui = DealPackageUI()
    monkeypatch.setattr("builtins.input", lambda prompt: "y")

    ui.display_deal_package_info(price=100.0, hours=12.0)
    confirmed = ui.get_purchase_confirmation()
    ui.display_purchase_success(hours=12.0)

    output = capsys.readouterr().out
    assert "===== DEAL PACKAGE =====" in output
    assert "Price: $100.0" in output
    assert "Hours: 12.0" in output
    assert "Deal package purchased. Added 12.0 hours" in output
    assert confirmed is True
