"""
UsageStatusUI.
Covers: Acct 8
"""
from typing import Dict


class UsageStatusUI:
    """Usage status UI (Account Management 8)"""
    def display_usage_status(self, bookings: list, ban_status: bool,
                             balance: float, deposit_status: str) -> None:
        print()
        print("=== Account Usage Status ===")

        bookings_count = len(bookings) if bookings else "None Active"
        print("Current Bookings:          {}".format(bookings_count))

        ban_text = "Banned" if ban_status else "Clear / Eligible to Book"
        print("Booking Restriction Status: {}".format(ban_text))
        print("Equipment Deposit Status:  {}".format(deposit_status))

        if balance > 0:
            print("Balance Status:            ${:.2f} (Sufficient for next booking slot)".format(balance))
        else:
            print("Balance Status:            ${:.2f} (Insufficient funds for upcoming slots)".format(balance))
        print("-" * 45)

    def display_return_option(self) -> None:
        input("Press Enter to return to the main portal...")

