from datetime import datetime


class ActivityHistoryUI:
    """Activity history UI (Account Management 9-10)"""

    def display_page(self, page_num: int, total_pages: int) -> None:
        print()
        print("--- Student Activity Ledger History (Page {} of {}) ---".format(page_num, total_pages))

    def display_activity_records(self, records_slice: list, start_idx: int) -> None:
        for idx, rec in enumerate(records_slice, start=start_idx + 1):
            if hasattr(rec, 'get_date'):
                date_str = rec.get_date().strftime("%Y-%m-%d") if isinstance(rec.get_date(), datetime) else str(rec.get_date())
                rec_type = rec.get_record_type().capitalize()
                details = rec.get_details()
                amount_str = "-${:.2f}".format(rec.get_amount()) if rec_type != "Recharge" else "+${:.2f}".format(rec.get_amount())
            else:
                date_str = rec.get("date", "")
                rec_type = rec.get("type", "").capitalize()
                details = rec.get("details", "")
                amount_str = rec.get("amount", "")
            
            print("{}. [{}] Type: {} | {} | Amount: {}".format(idx, date_str, rec_type, details, amount_str))

    def display_record_type_legend(self) -> None:
        print("-" * 60)
        print("Legend Types Reference Guide: Booking | Recharge | Late Cancellation | No Show")
        print("-" * 60)

    def display_navigation_menu(self) -> None:
        print("1. Next Page")
        print("2. Previous Page")
        print("3. Enter Direct Page Number Target")
        print("4. Return to Main Menu")
        print()

    def get_page_navigation_input(self) -> str:
        return input("Selection: ").strip()

    def get_direct_page_input(self, total_pages: int) -> int:
        target_str = input("Enter target page index number (1-{}): ".format(total_pages)).strip()
        if target_str.isdigit() and 1 <= int(target_str) <= total_pages:
            return int(target_str)
        else:
            print("[ERROR] Out of range tracking index targets.")
            return -1

    def display_newest_page_warning(self) -> None:
        print("You are already displaying the newest transaction records page.")

    def display_oldest_page_warning(self) -> None:
        print("You are already displaying the oldest transaction records page.")

