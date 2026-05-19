"""
FundsUI.
Covers: Acct 11-12
"""
from typing import Dict


class FundsUI:
    """资金管理界面 (Account Management 11-12, Checkout 8)"""
    def display_current_balance(self, balance: float) -> None: pass
    def get_top_up_amount(self) -> float: return 0.0
    def display_top_up_success(self, amount: float, new_balance: float) -> None: pass
    def display_invalid_amount_message(self) -> None: pass
    def display_top_up_options(self) -> None: pass

