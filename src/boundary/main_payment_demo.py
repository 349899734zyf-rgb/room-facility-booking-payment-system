from datetime import datetime, timedelta
from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from boundary.payment_ui import DealPackageUI, PaymentUI
from controllers.payment_controller import PaymentController
from entities.booking import Booking
from entities.room import Room
from entities.student import Student


def build_sample_booking():
    student = Student(
        "test@student.monash.edu",
        "Password1",
        "Tom",
        "Lee",
        "0412345678",
        "12345678"
    )
    student.add_funds(200)

    room = Room(
        "RM001",
        "Study Room",
        "Clayton",
        4,
        10,
        "08:00-22:00"
    )

    start = datetime.now().replace(microsecond=0)
    end = start + timedelta(hours=2)

    booking = Booking(
        "BK001",
        student,
        room,
        start,
        end,
        False,
        20
    )

    return student, room, booking


def main():
    payment_ui = PaymentUI()
    deal_package_ui = DealPackageUI()
    payment_controller = PaymentController()

    student, room, booking = build_sample_booking()
    duration = booking.calculate_duration_hours()
    time_period = f"{booking.get_start_time()} to {booking.get_end_time()}"

    payment_ui.display_booking_summary(
        name=f"{student.get_first_name()} {student.get_last_name()}",
        room=room.get_room_name(),
        building=room.get_building(),
        time_period=time_period,
        price=booking.get_total_price(),
        equipment=booking.get_equipment_rental()
    )

    payment_ui.display_payment_options(
        price=booking.get_total_price(),
        duration=duration
    )

    choice = payment_ui.get_payment_method_choice()
    payment_method = "deal_package" if choice == "2" else "balance"
    order = payment_controller.create_order(booking, payment_method)

    promo_input = payment_ui.get_promo_code_input().strip()
    if promo_input and payment_method == "deal_package":
        payment_ui.display_promo_deal_package_restriction_message()
    elif promo_input:
        promo = payment_controller.validate_promo_code(promo_input, student)
        if promo is None:
            if student.has_used_promo_code(promo_input):
                payment_ui.display_promo_code_used_message()
            else:
                payment_ui.display_promo_code_invalid_message()
        else:
            final_price = payment_controller.apply_promo_code(
                promo,
                student,
                order
            )
            payment_ui.display_promo_code_valid(final_price)

    if payment_method == "balance":
        payable_amount = payment_controller.get_order_payable_amount(order)
        payment_ui.display_balance_payment_info(
            price=payable_amount,
            balance=student.get_balance()
        )
        success = payment_controller.pay_by_balance(
            student,
            payable_amount
        )
    else:
        payment_ui.display_deal_package_info(
            duration=duration,
            remaining=student.get_deal_package_hours()
        )
        success = payment_controller.pay_by_deal_package(
            student,
            duration,
            booking.get_equipment_rental()
        )

        if not success and student.get_deal_package_hours() < duration:
            payment_ui.display_insufficient_deal_hours_message()
            package = payment_controller.get_deal_package()
            deal_package_ui.display_deal_package_info(
                package.get_price(),
                package.get_hours()
            )

    if success:
        payment_controller.confirm_order(order, student)
        payment_ui.display_booking_confirmed()
        payment_ui.display_next_step_options()
    elif payment_method == "balance":
        payment_ui.display_insufficient_balance_message()


if __name__ == "__main__":
    main()
