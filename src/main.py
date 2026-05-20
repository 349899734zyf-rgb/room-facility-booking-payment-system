import sys
import os

# Ensure the 'src' directory is in sys.path
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from boundary.main_account_ui import main as run_account_ui
from boundary.main_booking_ui import main as run_booking_ui
from boundary.main_payment_ui import main as run_payment_ui
from boundary.main_admin_ui import main_admin_room_management as run_admin_ui


def display_manager_menu():
    print()
    print("=" * 50)
    print("         MSSRB SYSTEM INTEGRATED MANAGER")
    print("=" * 50)
    print("1. Account & Login Management Flow (Amanda's Part)")
    print("2. Room Booking System Demo")
    print("3. Checkout & Payment System Demo")
    print("4. Administrator & Room Management Demo")
    print("5. Exit Manager")
    print("=" * 50)


def main():
    while True:
        display_manager_menu()
        choice = input("Please select an option (1-5): ").strip()

        if choice == "1":
            print("\n>>> Launching Account & Login Management UI...")
            try:
                run_account_ui()
            except SystemExit:
                print("\n>>> Returned from Account & Login Management.")
            except Exception as e:
                print(f"\n>>> Error running Account UI: {e}")

        elif choice == "2":
            print("\n>>> Launching Room Booking System Demo...")
            try:
                run_booking_ui()
            except SystemExit:
                print("\n>>> Returned from Room Booking System.")
            except Exception as e:
                print(f"\n>>> Error running Booking UI: {e}")

        elif choice == "3":
            print("\n>>> Launching Checkout & Payment System Demo...")
            try:
                run_payment_ui()
            except SystemExit:
                print("\n>>> Returned from Checkout & Payment System.")
            except Exception as e:
                print(f"\n>>> Error running Payment UI: {e}")

        elif choice == "4":
            print("\n>>> Launching Administrator & Room Management Demo...")
            try:
                run_admin_ui()
            except SystemExit:
                print("\n>>> Returned from Admin & Room Management.")
            except Exception as e:
                print(f"\n>>> Error running Admin UI: {e}")

        elif choice == "5":
            print("\nThank you for using MSSRB System. Exiting...")
            break
        else:
            print("\nError: Invalid choice! Please select 1-5.")


if __name__ == "__main__":
    main()
