from src.main import build_sample_booking, run_booking_flow


def build_low_balance_sample_booking(equipment_rental=False):
    student, room, booking = build_sample_booking(equipment_rental)
    student.set_balance(10)
    return student, room, booking


def test_run_booking_flow_continues_after_top_up(capsys, monkeypatch):
    inputs = iter([
        "2",
        "1",
        "NEWBEE20",
        "1",
        "10",
        "1",
        "2",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("src.main.build_sample_booking", build_low_balance_sample_booking)

    assert run_booking_flow() is False

    output = capsys.readouterr().out
    assert "Insufficient balance" in output
    assert "Top-up complete. Current balance: $20.0" in output
    assert "Booking confirmed" in output
    assert "===== ORDER DETAIL =====" in output
    assert "Order ID: OD0001" in output
    assert "Payment method: balance" in output
    assert "Checkout finished" in output


def test_run_booking_flow_continues_after_deal_package_purchase(capsys, monkeypatch):
    inputs = iter([
        "2",
        "2",
        "",
        "y",
        "1",
        "100",
        "1",
        "2",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("src.main.build_sample_booking", build_low_balance_sample_booking)

    assert run_booking_flow() is False

    output = capsys.readouterr().out
    assert "Not enough package hours" in output
    assert "Insufficient balance" in output
    assert "Top-up complete. Current balance: $110.0" in output
    assert "Deal package purchased. Added 12.0 hours" in output
    assert "Booking confirmed" in output
    assert "===== ORDER DETAIL =====" in output
    assert "Order ID: OD0001" in output
    assert "Payment method: deal_package" in output
    assert "Checkout finished" in output


def test_run_booking_flow_can_stop_deal_package_purchase(capsys, monkeypatch):
    inputs = iter([
        "2",
        "2",
        "",
        "n",
        "2",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert run_booking_flow() is False

    output = capsys.readouterr().out
    assert "Not enough package hours" in output
    assert "Booking not confirmed" in output
    assert "Checkout finished" in output
