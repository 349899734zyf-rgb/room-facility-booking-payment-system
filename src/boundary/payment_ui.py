"""
Module: payment_ui.py
Layer: Boundary
User Stories: Checkout 1-9

Text-based user interface for the checkout and payment flow,
including payment method selection, promo code input, deal package
display, booking summary, top-up prompts, and order confirmation.
"""


class PaymentUI:
    """Boundary class for checkout and payment user interactions (Checkout 1-9)."""

    def display_payment_options(
            self,
            price,
            duration
    ):

        print("\n===== PAYMENT =====")
        print(f"Price: ${price}")
        print(f"Duration: {duration} hours")
        print("1. Balance Payment")
        print("2. Deal Package")

    def get_payment_method_choice(self):
        return input("Choose payment method (1 for Balance, 2 for Deal Package, or enter 'CANCEL' to return): ")

    def display_balance_payment_info(
            self,
            price,
            balance
    ):
        print(f"Price: ${price}")
        print(f"Current balance: ${balance}")

    def get_promo_code_input(self):
        return input("Enter promo code (or press Enter to skip, or enter 'CANCEL' to return): ")

    def display_promo_code_valid(self, new_price):
        print(f"Promo applied. New price: ${new_price}")

    def display_promo_code_invalid_message(self):
        print("Invalid promo code")

    def display_promo_code_used_message(self):
        print("Promo code already used")

    def display_deal_package_info(
            self,
            duration,
            remaining
    ):
        print(f"Required hours: {duration}")
        print(f"Remaining package hours: {remaining}")

    def display_booking_confirmed(self):
        print("Booking confirmed")

    def display_insufficient_balance_message(self):
        print("Insufficient balance")

    def display_insufficient_deal_hours_message(self):
        print("Not enough package hours")

    def display_equipment_restriction_message(self):
        print("Deal package cannot be used with equipment rental")

    def display_promo_deal_package_restriction_message(self):
        print("Promo code cannot be used with deal package")

    def display_booking_summary(
            self,
            name,
            room,
            building,
            time_period,
            price,
            equipment
    ):
        print("\n===== BOOKING SUMMARY =====")
        print(f"Name: {name}")
        print(f"Room: {room}")
        print(f"Building: {building}")
        print(f"Time: {time_period}")
        print(f"Price: ${price}")
        print(f"Equipment rental: {'Yes' if equipment else 'No'}")

    def display_next_step_options(self):
        print("1. Make another booking")
        print("2. Finish")

    def get_next_step_choice(self):
        return input("Choose next step (1 to make another booking, 2 to finish, or enter 'CANCEL' to return): ")

    # Methods imported from Branch_CQ

    def display_equipment_options(self):
        print("\n===== EQUIPMENT RENTAL =====")
        print("Equipment rental?")
        print("1. Yes")
        print("2. No")

    def get_equipment_choice(self):
        return input("Choose equipment option (1 for Yes, 2 for No, or enter 'CANCEL' to return): ")

    def display_invalid_equipment_option_message(self):
        print("Invalid equipment option")

    def display_invalid_payment_option_message(self):
        print("Invalid payment option")

    def display_proceed_confirmation_prompt(self):
        print('If you want to proceed')
        print("1 for yes, 2 for no")

    def get_proceed_confirmation_choice(self):
        return input("Choose option (1 for Yes, 2 for No, or enter 'CANCEL' to return): ")

    def display_booking_not_confirmed(self):
        print("Booking not confirmed")

    def display_top_up_option(self):
        print("1. Add funds")
        print("2. Stop payment")

    def get_top_up_choice(self):
        return input("Choose top-up option (1 to add funds, 2 to stop payment, or enter 'CANCEL' to return): ")

    def get_top_up_amount(self):
        return input("Enter top-up amount (positive number, or enter 'CANCEL' to return): ")

    def display_top_up_success(self, balance):
        print(f"Top-up complete. Current balance: ${balance}")

    def display_order_detail(
            self,
            order_id,
            name,
            room,
            building,
            time_period,
            price,
            equipment,
            payment_method
    ):
        print("\n===== ORDER DETAIL =====")
        print(f"Order ID: {order_id}")
        print(f"Name: {name}")
        print(f"Room: {room}")
        print(f"Building: {building}")
        print(f"Time: {time_period}")
        print(f"Price: ${price}")
        print(f"Equipment rental: {'Yes' if equipment else 'No'}")
        print(f"Payment method: {payment_method}")

    def display_checkout_finished(self):
        print("Checkout finished")

