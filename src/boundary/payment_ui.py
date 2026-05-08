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

    def get_promo_code_input(self):
        return input("Enter promo code: ")

    def display_promo_code_valid(self, new_price):
        print(f"Promo applied. New price: ${new_price}")

    def display_promo_code_invalid_message(self):
        print("Invalid promo code")

    def display_promo_code_used_message(self):
        print("Promo code already used")

    def display_booking_confirmed(self):
        print("Booking confirmed")

    def display_insufficient_balance_message(self):
        print("Insufficient balance")

    def display_insufficient_deal_hours_message(self):
        print("Not enough package hours")