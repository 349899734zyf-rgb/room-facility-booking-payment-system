from typing import Optional


class DealPackageUI:
    """Deal Package boundary class (Checkout 7)"""

    def display_deal_package_info(self, price: float, hours: float) -> None:
        """Display details of the deal package available for purchase."""
        print("\n===== DEAL PACKAGE =====")
        print(f"Price: ${price}")
        print(f"Hours: {hours}")

    def get_purchase_confirmation(self) -> Optional[bool]:
        """Get confirmation from the student for purchase."""
        ans = input("Purchase deal package? (y/n, or enter 'CANCEL' to return): ").strip().lower()
        if ans.upper() == "CANCEL":
            return None
        return ans == "y"

    def display_purchase_success(self, hours: float) -> None:
        """Display success message upon purchase."""
        print(f"Deal package purchased. Added {hours} hours")
