"""
validators.py
Shared rules used across CLIUniApp.

Stories covered:
    102 - Validate email and password against patterns
    303 - Map a mark to the grading scale (Z, P, C, D, HD)
    306 - Password rules reused when a student changes their password
    406 - PASS / FAIL threshold

Keeping every rule in one module means registration, password change and the
admin views can never disagree about what "valid" or "pass" means.
"""

import re

# ---------------------------------------------------------------------------
# Story 102: credential patterns
# ---------------------------------------------------------------------------

# Email must end in @university.com, e.g. john.smith@university.com
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@university\.com$", re.IGNORECASE)

# Password: one or more letters followed by at least three digits, e.g. Helloworld123
PASSWORD_PATTERN = re.compile(r"^[A-Za-z]+[0-9]{3,}$")

EMAIL_RULE_TEXT = "Email must end in @university.com (e.g. john.smith@university.com)."
PASSWORD_RULE_TEXT = "Password must be letters followed by at least 3 digits (e.g. Helloworld123)."


def validate_email(email: str) -> bool:
    """Return True if the email matches the university email format."""
    return bool(EMAIL_PATTERN.fullmatch(email))


def validate_password(password: str) -> bool:
    """Return True if the password matches the required pattern."""
    return bool(PASSWORD_PATTERN.fullmatch(password))


def validate_credentials(email: str, password: str) -> bool:
    """Return True only if both the email and the password are valid."""
    return validate_email(email) and validate_password(password)


# ---------------------------------------------------------------------------
# Story 303 / 406: grading scale and pass mark
# ---------------------------------------------------------------------------

PASS_MARK = 50

# Checked from highest to lowest; the first threshold the mark reaches wins.
GRADE_BOUNDARIES = (
    (85, "HD"),  # High Distinction: 85-100
    (75, "D"),   # Distinction:      75-84
    (65, "C"),   # Credit:           65-74
    (50, "P"),   # Pass:             50-64
    (0, "Z"),    # Fail:              0-49
)

GRADE_ORDER = tuple(grade for _, grade in GRADE_BOUNDARIES)  # ("HD", "D", "C", "P", "Z")


def mark_to_grade(mark: float) -> str:
    """Convert a numeric mark into its grade letter(s)."""
    for threshold, grade in GRADE_BOUNDARIES:
        if mark >= threshold:
            return grade
    return "Z"


def is_pass(mark: float) -> bool:
    """Return True if the mark is a pass (>= 50)."""
    return mark >= PASS_MARK
