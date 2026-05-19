"""
RegistrationUI.
Covers: Acct 1-3
"""
from typing import Dict


class RegistrationUI:
    """注册界面 (Account Management 1-3)"""
    def display_registration_form(self) -> None: pass
    def get_registration_input(self) -> Dict[str, str]: return {}
    def display_success_message(self) -> None: pass
    def display_error_message(self, message: str) -> None: pass
    def display_invalid_email_message(self) -> None: pass
    def display_password_requirement_message(self) -> None: pass
    def display_incomplete_details_message(self) -> None: pass

