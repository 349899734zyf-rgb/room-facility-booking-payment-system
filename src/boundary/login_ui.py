"""
LoginUI.
Covers: Acct 4, 15
"""
from typing import Dict


class LoginUI:
    """登录界面 (Account Management 4, 15)"""
    def display_login_form(self) -> None: pass
    def get_login_credentials(self) -> Dict[str, str]: return {}
    def display_login_success(self, role: str) -> None: pass
    def display_invalid_credentials_message(self) -> None: pass

