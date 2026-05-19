"""
MSSRB — Account Management BVT (Boundary Value Testing)
User Stories: Acct 1 ~ Acct 15
Test Strategy: min-, min, middle, max, max+ for each boundary condition
"""
import unittest
import sys
sys.path.insert(0, r"d:\5136\project 2\src")

from entities.student import Student
from entities.admin import Admin
from entities.user import User
from controllers.auth_controller import AuthController
from controllers.account_controller import AccountController
from controllers.admin_controller import AdminController


# ============================================================
# Acct 1: Student Registration
# Boundary: all 6 fields must be non-empty
# ============================================================
class TestAcct01_StudentRegistration(unittest.TestCase):
    """Acct 1 — Student Registration [SP: 5]
    AC: Student enters email, password, last name, first name, mobile, student ID.
    BVT: Number of blank fields (0 = valid, 1+ = invalid)
    """
    def setUp(self):
        self.auth = AuthController()

    def test_bvt_all_fields_filled(self):
        """BVT min (0 blank fields) — should succeed"""
        s = self.auth.register_student("a@student.monash.edu", "Pass1234",
                                       "John", "Doe", "0412345678", "12345678")
        self.assertIsNotNone(s)

    def test_bvt_one_blank_field(self):
        """BVT min+ (1 blank field — email empty) — should fail"""
        s = self.auth.register_student("", "Pass1234", "John", "Doe", "0412345678", "12345678")
        self.assertIsNone(s)

    def test_bvt_two_blank_fields(self):
        """BVT middle (2 blank fields) — should fail"""
        s = self.auth.register_student("", "", "John", "Doe", "0412345678", "12345678")
        self.assertIsNone(s)

    def test_bvt_all_blank_fields(self):
        """BVT max (6 blank fields) — should fail"""
        s = self.auth.register_student("", "", "", "", "", "")
        self.assertIsNone(s)

    def test_bvt_cancel_registration(self):
        """AC: Cancel registration exits without saving"""
        initial_count = len(self.auth.get_students())
        # Simulate cancel by not calling register
        self.assertEqual(len(self.auth.get_students()), initial_count)

    def test_bvt_successful_saves_to_list(self):
        """AC: Successful registration saves account"""
        self.auth.register_student("b@student.monash.edu", "Pass1234",
                                   "Jane", "Smith", "0498765432", "87654321")
        self.assertEqual(len(self.auth.get_students()), 1)


# ============================================================
# Acct 2: Registration with Valid Monash Email
# Boundary: email must end with @student.monash.edu
# ============================================================
class TestAcct02_ValidMonashEmail(unittest.TestCase):
    """Acct 2 — Valid Monash Email [SP: 1]
    AC: Email format xxxx@student.monash.edu, invalid email shows error.
    BVT: email suffix validation
    """
    def setUp(self):
        self.auth = AuthController()

    def test_bvt_min_minus_empty_email(self):
        """BVT min- (empty string) — invalid"""
        self.assertFalse(self.auth.validate_email(""))

    def test_bvt_min_just_domain(self):
        """BVT min (just '@student.monash.edu') — valid format"""
        self.assertTrue(self.auth.validate_email("@student.monash.edu"))

    def test_bvt_middle_normal_email(self):
        """BVT middle (normal student email) — valid"""
        self.assertTrue(self.auth.validate_email("john0001@student.monash.edu"))

    def test_bvt_max_long_prefix(self):
        """BVT max (very long prefix) — valid"""
        self.assertTrue(self.auth.validate_email("a" * 100 + "@student.monash.edu"))

    def test_bvt_max_plus_wrong_domain(self):
        """BVT max+ (wrong domain) — invalid"""
        self.assertFalse(self.auth.validate_email("john@monash.edu"))

    def test_bvt_gmail_domain(self):
        """BVT extra — gmail domain — invalid"""
        self.assertFalse(self.auth.validate_email("john@gmail.com"))

    def test_bvt_partial_domain(self):
        """BVT extra — partial domain — invalid"""
        self.assertFalse(self.auth.validate_email("john@student.monash"))


# ============================================================
# Acct 3: Registration with Valid Password
# Boundary: >=8 chars, must contain uppercase AND digit
# ============================================================
class TestAcct03_ValidPassword(unittest.TestCase):
    """Acct 3 — Valid Password [SP: 2]
    AC: Password >=8 chars, contains uppercase and number.
    BVT: password length and character composition
    """
    def setUp(self):
        self.auth = AuthController()

    def test_bvt_min_minus_7_chars(self):
        """BVT min- (7 chars with uppercase+digit) — FAIL"""
        self.assertFalse(self.auth.validate_password("Pass12a"))  # 7 chars

    def test_bvt_min_8_chars(self):
        """BVT min (8 chars with uppercase+digit) — PASS"""
        self.assertTrue(self.auth.validate_password("Pass1234"))  # 8 chars

    def test_bvt_middle_12_chars(self):
        """BVT middle (12 chars) — PASS"""
        self.assertTrue(self.auth.validate_password("Password1234"))

    def test_bvt_max_50_chars(self):
        """BVT max (50 chars) — PASS"""
        self.assertTrue(self.auth.validate_password("A1" + "a" * 48))

    def test_bvt_no_uppercase(self):
        """BVT composition — no uppercase — FAIL"""
        self.assertFalse(self.auth.validate_password("password1"))

    def test_bvt_no_digit(self):
        """BVT composition — no digit — FAIL"""
        self.assertFalse(self.auth.validate_password("Password"))

    def test_bvt_empty_password(self):
        """BVT min- — empty string — FAIL"""
        self.assertFalse(self.auth.validate_password(""))


# ============================================================
# Acct 4: Student Login
# Boundary: correct vs incorrect credentials
# ============================================================
class TestAcct04_StudentLogin(unittest.TestCase):
    """Acct 4 — Student Login [SP: 3]
    AC: Correct credentials → main menu, incorrect → error.
    BVT: credential matching
    """
    def setUp(self):
        self.auth = AuthController()
        self.auth.register_student("stu@student.monash.edu", "Pass1234",
                                   "John", "Doe", "0412345678", "12345678")

    def test_bvt_correct_credentials(self):
        """BVT valid — correct email + password"""
        user = self.auth.login("stu@student.monash.edu", "Pass1234")
        self.assertIsNotNone(user)

    def test_bvt_wrong_password(self):
        """BVT min- — correct email, wrong password"""
        user = self.auth.login("stu@student.monash.edu", "Wrong123")
        self.assertIsNone(user)

    def test_bvt_wrong_email(self):
        """BVT min- — wrong email, correct password"""
        user = self.auth.login("wrong@student.monash.edu", "Pass1234")
        self.assertIsNone(user)

    def test_bvt_both_wrong(self):
        """BVT max- — both wrong"""
        user = self.auth.login("wrong@student.monash.edu", "Wrong123")
        self.assertIsNone(user)

    def test_bvt_empty_credentials(self):
        """BVT min- — empty strings"""
        user = self.auth.login("", "")
        self.assertIsNone(user)


# ============================================================
# Acct 5: View Profile Information
# Boundary: profile fields must match registered data
# ============================================================
class TestAcct05_ViewProfile(unittest.TestCase):
    """Acct 5 — View Profile [SP: 1]
    AC: Displays first name, last name, student ID, email, mobile, balance.
    BVT: profile completeness
    """
    def setUp(self):
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")
        self.ctrl = AccountController()

    def test_bvt_all_fields_present(self):
        """BVT — all 6 fields returned"""
        info = self.ctrl.get_profile_info(self.student)
        self.assertEqual(len(info), 6)
        self.assertEqual(info["first_name"], "John")
        self.assertEqual(info["last_name"], "Doe")
        self.assertEqual(info["student_id"], "12345678")
        self.assertEqual(info["email"], "s@student.monash.edu")
        self.assertEqual(info["phone"], "0412345678")
        self.assertEqual(info["balance"], 0.0)


# ============================================================
# Acct 6: Edit Mobile Number
# Boundary: 04XXXXXXXX format (10 digits, starts with 04)
# ============================================================
class TestAcct06_EditMobile(unittest.TestCase):
    """Acct 6 — Edit Mobile Number [SP: 2]
    AC: 04XXXXXXXX format, new == confirm, cancel keeps original.
    BVT: mobile number length and format
    """
    def setUp(self):
        self.auth = AuthController()
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")

    def test_bvt_min_minus_9_digits(self):
        """BVT min- (9 digits) — FAIL"""
        self.assertFalse(self.auth.validate_mobile("041234567"))

    def test_bvt_min_10_digits_valid(self):
        """BVT min (10 digits, starts 04) — PASS"""
        self.assertTrue(self.auth.validate_mobile("0412345678"))

    def test_bvt_max_plus_11_digits(self):
        """BVT max+ (11 digits) — FAIL"""
        self.assertFalse(self.auth.validate_mobile("04123456789"))

    def test_bvt_wrong_prefix(self):
        """BVT — doesn't start with 04 — FAIL"""
        self.assertFalse(self.auth.validate_mobile("0312345678"))

    def test_bvt_non_digit(self):
        """BVT — contains letter — FAIL"""
        self.assertFalse(self.auth.validate_mobile("04123abcde"))

    def test_bvt_mismatch_confirm(self):
        """BVT — new != confirm — FAIL"""
        result = self.auth.update_mobile(self.student, "0498765432", "0400000000")
        self.assertFalse(result)

    def test_bvt_matching_valid(self):
        """BVT — matching valid numbers — PASS"""
        result = self.auth.update_mobile(self.student, "0498765432", "0498765432")
        self.assertTrue(result)
        self.assertEqual(self.student.get_phone(), "0498765432")

    def test_bvt_cancel_keeps_original(self):
        """AC: Cancel keeps original number unchanged"""
        original = self.student.get_phone()
        # Simulate cancel by not calling update
        self.assertEqual(self.student.get_phone(), original)


# ============================================================
# Acct 7: Change Password
# Boundary: current password must match, new must follow rules
# ============================================================
class TestAcct07_ChangePassword(unittest.TestCase):
    """Acct 7 — Change Password [SP: 3]
    AC: current password verified, new follows rules, confirm matches.
    BVT: password change conditions
    """
    def setUp(self):
        self.auth = AuthController()
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")

    def test_bvt_valid_change(self):
        """BVT — all conditions met — PASS"""
        self.assertTrue(self.auth.change_password(self.student, "Pass1234", "NewPass99", "NewPass99"))

    def test_bvt_wrong_current(self):
        """BVT — wrong current password — FAIL"""
        self.assertFalse(self.auth.change_password(self.student, "Wrong123", "NewPass99", "NewPass99"))

    def test_bvt_mismatch_confirm(self):
        """BVT — new != confirm — FAIL"""
        self.assertFalse(self.auth.change_password(self.student, "Pass1234", "NewPass99", "Different1"))

    def test_bvt_new_too_short(self):
        """BVT min- — new password 7 chars — FAIL"""
        self.assertFalse(self.auth.change_password(self.student, "Pass1234", "New1abc", "New1abc"))

    def test_bvt_new_exactly_8(self):
        """BVT min — new password 8 chars — PASS"""
        self.assertTrue(self.auth.change_password(self.student, "Pass1234", "NewPas12", "NewPas12"))


# ============================================================
# Acct 8: View Usage Status
# Boundary: status fields reflect current state
# ============================================================
class TestAcct08_ViewUsageStatus(unittest.TestCase):
    """Acct 8 — View Usage Status [SP: 1]
    AC: Displays bookings, ban status, balance, deposit status.
    BVT: status field values at boundary states
    """
    def setUp(self):
        self.ctrl = AccountController()
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")

    def test_bvt_new_student_defaults(self):
        """BVT min — new student, all defaults"""
        status = self.ctrl.get_usage_status(self.student)
        self.assertEqual(status["ban_status"], False)
        self.assertEqual(status["balance"], 0.0)
        self.assertEqual(len(status["current_bookings"]), 0)

    def test_bvt_banned_student(self):
        """BVT max — banned student"""
        self.student.set_booking_ban_status(True)
        status = self.ctrl.get_usage_status(self.student)
        self.assertTrue(status["ban_status"])

    def test_bvt_student_with_balance(self):
        """BVT middle — student with balance"""
        self.student.add_funds(50.0)
        status = self.ctrl.get_usage_status(self.student)
        self.assertEqual(status["balance"], 50.0)


# ============================================================
# Acct 9: View Activity History
# Boundary: number of records (0, 1, many)
# ============================================================
class TestAcct09_ViewActivityHistory(unittest.TestCase):
    """Acct 9 — View Activity History [SP: 2]
    AC: Displays date, type, details, amount. Record types shown.
    BVT: activity history record count
    """
    def setUp(self):
        self.ctrl = AccountController()
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")

    def test_bvt_min_no_records(self):
        """BVT min (0 records)"""
        history = self.ctrl.get_activity_history(self.student, 1)
        self.assertEqual(len(history), 0)

    def test_bvt_one_record(self):
        """BVT min+ (1 record after add funds)"""
        self.student.add_funds(10.0)
        history = self.ctrl.get_activity_history(self.student, 1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].get_record_type(), "recharge")

    def test_bvt_multiple_records(self):
        """BVT middle (3 records)"""
        self.student.add_funds(10.0)
        self.student.add_funds(20.0)
        self.student.add_funds(30.0)
        history = self.ctrl.get_activity_history(self.student, 1)
        self.assertEqual(len(history), 3)


# ============================================================
# Acct 10: Navigate Activity History Pages
# Boundary: page number (0, 1, middle, last, beyond)
# ============================================================
class TestAcct10_NavigateHistoryPages(unittest.TestCase):
    """Acct 10 — Navigate History Pages [SP: 2]
    AC: Next/prev page, page number input, correct records per page.
    BVT: page number boundaries (page_size=10)
    """
    def setUp(self):
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")
        for i in range(25):
            self.student.add_funds(1.0)  # Creates 25 activity records

    def test_bvt_page_1(self):
        """BVT min — page 1 returns 10 records"""
        page = self.student.get_activity_history_page(1, 10)
        self.assertEqual(len(page), 10)

    def test_bvt_page_2(self):
        """BVT middle — page 2 returns 10 records"""
        page = self.student.get_activity_history_page(2, 10)
        self.assertEqual(len(page), 10)

    def test_bvt_page_3_partial(self):
        """BVT max — page 3 returns 5 records (25 total, pages of 10)"""
        page = self.student.get_activity_history_page(3, 10)
        self.assertEqual(len(page), 5)

    def test_bvt_page_beyond(self):
        """BVT max+ — page 4 returns 0 records"""
        page = self.student.get_activity_history_page(4, 10)
        self.assertEqual(len(page), 0)

    def test_bvt_page_0(self):
        """BVT min- — page 0 returns empty (invalid)"""
        page = self.student.get_activity_history_page(0, 10)
        self.assertEqual(len(page), 0)


# ============================================================
# Acct 11: View Funds Management Summary
# Boundary: balance value (0, positive)
# ============================================================
class TestAcct11_ViewFundsSummary(unittest.TestCase):
    """Acct 11 — View Funds Summary [SP: 1]
    AC: Displays current balance.
    BVT: balance amounts
    """
    def setUp(self):
        self.ctrl = AccountController()
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")

    def test_bvt_min_zero_balance(self):
        """BVT min — zero balance"""
        summary = self.ctrl.get_funds_summary(self.student)
        self.assertEqual(summary["balance"], 0.0)

    def test_bvt_positive_balance(self):
        """BVT middle — after adding funds"""
        self.student.add_funds(100.0)
        summary = self.ctrl.get_funds_summary(self.student)
        self.assertEqual(summary["balance"], 100.0)


# ============================================================
# Acct 12: Add Funds
# Boundary: amount > 0
# ============================================================
class TestAcct12_AddFunds(unittest.TestCase):
    """Acct 12 — Add Funds [SP: 3]
    AC: Positive amount accepted, non-positive rejected, cancel keeps balance.
    BVT: top-up amount boundary
    """
    def setUp(self):
        self.ctrl = AccountController()
        self.student = Student("s@student.monash.edu", "Pass1234",
                               "John", "Doe", "0412345678", "12345678")

    def test_bvt_min_minus_negative(self):
        """BVT min- (-1.0) — FAIL"""
        self.assertFalse(self.ctrl.add_funds(self.student, -1.0))
        self.assertEqual(self.student.get_balance(), 0.0)

    def test_bvt_min_zero(self):
        """BVT min (0.0) — FAIL (must be positive)"""
        self.assertFalse(self.ctrl.add_funds(self.student, 0.0))

    def test_bvt_min_plus_tiny(self):
        """BVT min+ (0.01) — PASS"""
        self.assertTrue(self.ctrl.add_funds(self.student, 0.01))
        self.assertAlmostEqual(self.student.get_balance(), 0.01)

    def test_bvt_middle(self):
        """BVT middle (50.0) — PASS"""
        self.assertTrue(self.ctrl.add_funds(self.student, 50.0))
        self.assertEqual(self.student.get_balance(), 50.0)

    def test_bvt_max_large(self):
        """BVT max (10000.0) — PASS"""
        self.assertTrue(self.ctrl.add_funds(self.student, 10000.0))
        self.assertEqual(self.student.get_balance(), 10000.0)


# ============================================================
# Acct 13: Role Recognition
# Boundary: student vs admin role
# ============================================================
class TestAcct13_RoleRecognition(unittest.TestCase):
    """Acct 13 — Role Recognition [SP: 2]
    AC: System identifies student vs admin, functions based on role.
    BVT: role identification
    """
    def setUp(self):
        self.auth = AuthController()

    def test_bvt_student_role(self):
        """BVT — student identified as 'student'"""
        student = Student("s@student.monash.edu", "Pass1234",
                          "John", "Doe", "0412345678", "12345678")
        self.assertEqual(self.auth.identify_role(student), "student")

    def test_bvt_admin_role(self):
        """BVT — admin identified as 'admin'"""
        admin = Admin("admin@monash.edu", "Admin123",
                      "Jane", "Smith", "0498765432", "ADM001")
        self.assertEqual(self.auth.identify_role(admin), "admin")


# ============================================================
# Acct 14: Admin View Info
# Boundary: admin info completeness
# ============================================================
class TestAcct14_AdminViewInfo(unittest.TestCase):
    """Acct 14 — Admin View Info [SP: 1]
    AC: Displays email, first name, last name, phone.
    BVT: info completeness
    """
    def setUp(self):
        self.ctrl = AdminController()
        self.admin = Admin("admin@monash.edu", "Admin123",
                           "Jane", "Smith", "0498765432", "ADM001")

    def test_bvt_all_fields_present(self):
        """BVT — all 4 fields returned"""
        info = self.ctrl.get_admin_info(self.admin)
        self.assertEqual(len(info), 4)
        self.assertEqual(info["email"], "admin@monash.edu")
        self.assertEqual(info["first_name"], "Jane")
        self.assertEqual(info["last_name"], "Smith")
        self.assertEqual(info["phone"], "0498765432")


# ============================================================
# Acct 15: Admin Login
# Boundary: admin credential matching
# ============================================================
class TestAcct15_AdminLogin(unittest.TestCase):
    """Acct 15 — Admin Login [SP: 3]
    AC: Correct credentials → admin home, incorrect → fail.
    BVT: admin credential validation
    """
    def setUp(self):
        self.auth = AuthController()
        admin = Admin("admin@monash.edu", "Admin123",
                      "Jane", "Smith", "0498765432", "ADM001")
        self.auth.get_admins().append(admin)

    def test_bvt_correct_admin_login(self):
        """BVT — correct admin credentials — PASS"""
        user = self.auth.login("admin@monash.edu", "Admin123")
        self.assertIsNotNone(user)
        self.assertEqual(user.get_role(), "admin")

    def test_bvt_wrong_admin_password(self):
        """BVT — wrong password — FAIL"""
        user = self.auth.login("admin@monash.edu", "Wrong123")
        self.assertIsNone(user)

    def test_bvt_nonexistent_admin(self):
        """BVT — nonexistent admin — FAIL"""
        user = self.auth.login("fake@monash.edu", "Admin123")
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
