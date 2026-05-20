class PaymentUI:

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
        return input("Choose payment method: ")

    def display_balance_payment_info(
            self,
            price,
            balance
    ):
        print(f"Price: ${price}")
        print(f"Current balance: ${balance}")

    def get_promo_code_input(self):
        return input("Enter promo code: ")

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
        print("1. View my bookings")
        print("2. Return to home")

    def get_next_step_choice(self):
        return input("Choose next step: ")

