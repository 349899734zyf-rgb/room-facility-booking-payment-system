"""
EquipmentDepositUI - Equipment deposit management interface.
Covers: Room 11
"""


class EquipmentDepositUI:
    """Equipment Deposit User Interface - Story 2.11: Set Equipment Deposit"""
   
    def __init__(self, admin_controller):
        self.admin_controller = admin_controller

    def display_equipment_list(self, equipments: list) -> None:
        """Display all equipment"""
        if not equipments:
            print("\nNo equipment found")
            return

        print("\n" + "=" * 120)
        print(" " * 45 + "EQUIPMENT LIST")
        print("=" * 120)
        print(f"{'Equipment ID':<15} {'Current Deposit':<20} {'Available':<15}")
        print("-" * 120)

        for equipment in equipments:
            deposit = equipment.get_deposit_amount()
            available = 'Yes' if equipment.get_is_available() else 'No'
            print(f"{equipment.get_equipment_id():<15} "
                  f"${deposit:<19.2f} {available:<15}")

        print("=" * 120)

    def get_equipment_selection(self) -> str:
        """Get equipment selection from user"""
        print("\n" + "-" * 80)
        print(" " * 25 + "SELECT EQUIPMENT")
        print("-" * 80)
        return input("Enter equipment ID: ").strip()

    def display_current_deposit(self, equipment_id: str, amount: float) -> None:
        """Display current deposit information"""
        print("\n" + "-" * 80)
        print("Current Deposit Information:")
        print(f"  Equipment ID: {equipment_id}")
        print(f"  Current Deposit: ${amount:.2f}")
        print("-" * 80)

    def get_deposit_amount_input(self) -> float:
        """Get deposit amount input from user"""
        print("\n" + "-" * 80)
        print(" " * 20 + "SET EQUIPMENT DEPOSIT AMOUNT")
        print("-" * 80)

        try:
            amount_str = input("Enter deposit amount ($): ").strip()

            if not amount_str:
                print("Error: Deposit amount cannot be empty")
                return 0.0

            amount = float(amount_str)

            if amount < 0:
                print("Error: Deposit amount cannot be negative")
                return 0.0

            return amount

        except ValueError:
            print("Error: Please enter a valid number")
            return 0.0

    def get_deposit_confirmation(self) -> bool:
        """Get deposit confirmation from user"""
        confirm = input("\nConfirm setting this deposit amount? (y/n): ").strip().lower()
        return confirm in ['y', 'yes']

    def display_deposit_set_success(self, amount: float) -> None:
        """Display deposit set success message"""
        print(f"\nSuccess: Equipment deposit amount set to ${amount:.2f} successfully!")

    def display_deposit_refund_success(self, amount: float) -> None:
        """Display deposit refund success message"""
        print(f"\nSuccess: Equipment deposit of ${amount:.2f} refunded successfully!")

    def display_invalid_amount_message(self) -> None:
        """Display invalid amount message"""
        print("\nError: Invalid deposit amount. Please try again.")

