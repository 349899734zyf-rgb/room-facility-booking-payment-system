from typing import Optional


class FundsUI:
    """Funds management UI (Account Management 11-12, Checkout 8)"""

    def display_current_balance(self, balance: float) -> None:
        print("Current Available Balance: ${:.2f}".format(balance))

    def display_top_up_options(self) -> None:
        print("-" * 35)
        print("1. Add Funds (Top-Up)")
        print("2. Return to Main Menu")
        print()

    def get_menu_choice(self) -> str:
        return input("Selection: ").strip()

    def get_top_up_amount(self) -> Optional[float]:
        amount_str = input("Enter top-up amount (positive number, e.g. 50.00, or enter 'CANCEL' to return): ").strip()
        if amount_str.upper() == "CANCEL":
            return None
        try:
            amount = float(amount_str)
            if amount <= 0:
                self.display_invalid_amount_message()
                return 0.0
            return amount
        except ValueError:
            self.display_invalid_number_message()
            return 0.0

    def display_payment_confirmation(self, amount: float) -> None:
        print()
        print("Payment Confirmation: Add ${:.2f} to account?".format(amount))

    def get_payment_confirmation(self) -> Optional[bool]:
        conf = input("Type 'CONFIRM' to authorise simulated banking payment or enter 'CANCEL' to return: ").strip().upper()
        if conf == "CANCEL":
            return None
        return conf == "CONFIRM"

    def display_top_up_success(self, amount: float, new_balance: float) -> None:
        print("[SUCCESS] Payment success message displayed!")
        print("Updated Balance: ${:.2f} (Added Amount: ${:.2f})".format(new_balance, amount))

    def display_payment_cancelled(self) -> None:
        print("Payment cancelled. Original balance maintained unchanged.")

    def display_invalid_amount_message(self) -> None:
        print("[ERROR] Invalid amount message: Values must be strictly positive.")

    def display_invalid_number_message(self) -> None:
        print("[ERROR] Please enter a valid numerical dollar currency digit.")

