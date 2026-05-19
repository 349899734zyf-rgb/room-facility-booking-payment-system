from datetime import datetime, timedelta
from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.boundary.payment_ui import DealPackageUI, PaymentUI
from src.controllers.payment_controller import PaymentController
from src.entity_classes import Booking, Room, Student


def build_sample_booking(equipment_rental=False):
    student = Student(
        "test@student.monash.edu",
        "Password1",
        "Tom",
        "Lee",
        "0412345678",
        "12345678"
    )
    student.add_funds(200)
    student.add_deal_package_hours(1)

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
        equipment_rental,
        20
    )

    return student, room, booking


def main():
    while True:
        should_continue = run_booking_flow()
        if not should_continue:
            break


def run_booking_flow():
    payment_ui = PaymentUI()
    deal_package_ui = DealPackageUI()
    payment_controller = PaymentController()

    payment_ui.display_equipment_options()
    equipment_choice = payment_ui.get_equipment_choice()
    if equipment_choice == "1":
        equipment_rental = True
    elif equipment_choice == "2":
        equipment_rental = False
    else:
        payment_ui.display_invalid_equipment_option_message()
        return False

    student, room, booking = build_sample_booking(equipment_rental)
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
    payment_method = payment_controller.select_payment_method(choice)
    if payment_method is None:
        payment_ui.display_invalid_payment_option_message()
        return

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
        success = payment_controller.check_balance_sufficient(
            student,
            payable_amount
        )
    else:
        if not payment_controller.can_use_deal_package(booking.get_equipment_rental()):
            payment_ui.display_equipment_restriction_message()
            return prompt_for_next_step(payment_ui, payment_controller)

        payment_ui.display_deal_package_info(
            duration=duration,
            remaining=student.get_deal_package_hours()
        )
        success = student.get_deal_package_hours() >= duration

        if not success and student.get_deal_package_hours() < duration:
            payment_ui.display_insufficient_deal_hours_message()
            package = payment_controller.get_deal_package()
            deal_package_ui.display_deal_package_info(
                package.get_price(),
                package.get_hours()
            )
            if not deal_package_ui.get_purchase_confirmation():
                payment_ui.display_booking_not_confirmed()
                return prompt_for_next_step(payment_ui, payment_controller)

            if not payment_controller.purchase_deal_package(student):
                payment_ui.display_insufficient_balance_message()
                payment_ui.display_top_up_option()
                if payment_ui.get_top_up_choice() != "1":
                    payment_ui.display_checkout_finished()
                    return False

                try:
                    top_up_amount = float(payment_ui.get_top_up_amount())
                except ValueError:
                    payment_ui.display_invalid_payment_option_message()
                    return False

                if not payment_controller.top_up_account(student, top_up_amount):
                    payment_ui.display_invalid_payment_option_message()
                    return False

                payment_ui.display_top_up_success(student.get_balance())
                if not payment_controller.purchase_deal_package(student):
                    payment_ui.display_insufficient_balance_message()
                    return False

            deal_package_ui.display_purchase_success(package.get_hours())
            payment_ui.display_deal_package_info(
                duration=duration,
                remaining=student.get_deal_package_hours()
            )
            success = student.get_deal_package_hours() >= duration

    if success:
        payment_ui.display_proceed_confirmation_prompt()
        if payment_ui.get_proceed_confirmation_choice() != "1":
            payment_ui.display_booking_not_confirmed()
            return

        if payment_method == "balance":
            payment_controller.pay_by_balance(student, payable_amount)
        else:
            payment_controller.pay_by_deal_package(
                student,
                duration,
                booking.get_equipment_rental()
            )
            payment_ui.display_deal_package_info(
                duration=duration,
                remaining=student.get_deal_package_hours()
            )

        payment_controller.confirm_order(order, student)
        payment_ui.display_booking_confirmed()
        display_order_detail(payment_ui, payment_controller, order)
        payment_ui.display_next_step_options()
        next_step = payment_controller.choose_next_step(
            payment_ui.get_next_step_choice()
        )
        if next_step == "continue_booking":
            return True
        payment_ui.display_checkout_finished()
        return False
    elif payment_method == "balance":
        payment_ui.display_insufficient_balance_message()
        payment_ui.display_top_up_option()
        if payment_ui.get_top_up_choice() != "1":
            payment_ui.display_checkout_finished()
            return False

        try:
            top_up_amount = float(payment_ui.get_top_up_amount())
        except ValueError:
            payment_ui.display_invalid_payment_option_message()
            return False

        if not payment_controller.top_up_account(student, top_up_amount):
            payment_ui.display_invalid_payment_option_message()
            return False

        payment_ui.display_top_up_success(student.get_balance())

        if not payment_controller.check_balance_sufficient(student, payable_amount):
            payment_ui.display_insufficient_balance_message()
            return False

        payment_ui.display_proceed_confirmation_prompt()
        if payment_ui.get_proceed_confirmation_choice() != "1":
            payment_ui.display_booking_not_confirmed()
            return False

        payment_controller.pay_by_balance(student, payable_amount)
        payment_controller.confirm_order(order, student)
        payment_ui.display_booking_confirmed()
        display_order_detail(payment_ui, payment_controller, order)
        return prompt_for_next_step(payment_ui, payment_controller)

    return False


def display_order_detail(payment_ui, payment_controller, order):
    summary = payment_controller.get_booking_summary(order)
    payment_ui.display_order_detail(
        order_id=order.get_order_id(),
        name=summary["name"],
        room=summary["room"],
        building=summary["building"],
        time_period=summary["time_period"],
        price=summary["price"],
        equipment=summary["equipment"],
        payment_method=order.get_payment_method()
    )


def prompt_for_next_step(payment_ui, payment_controller):
    payment_ui.display_next_step_options()
    next_step = payment_controller.choose_next_step(
        payment_ui.get_next_step_choice()
    )
    if next_step == "continue_booking":
        return True
    payment_ui.display_checkout_finished()
    return False


if __name__ == "__main__":
    main()
