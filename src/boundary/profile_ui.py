"""
ProfileUI.
Covers: Acct 5-7
"""
from typing import Dict


class ProfileUI:
    """个人资料界面 (Account Management 5-7)"""
    def display_profile(self, first_name: str, last_name: str, student_id: str,
                        email: str, phone: str, balance: float) -> None: pass
    def get_new_mobile_number(self) -> str: return ""
    def get_confirm_mobile_number(self) -> str: return ""
    def display_mobile_update_success(self) -> None: pass
    def display_invalid_mobile_format_message(self) -> None: pass
    def get_password_change_input(self) -> Dict[str, str]: return {}
    def display_password_change_success(self) -> None: pass
    def display_password_requirement_message(self) -> None: pass

