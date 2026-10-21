"""
student.py
The Student class: a registered student and their enrolments.

Stories covered:
    103 - Generate a unique 6-digit student ID (000001-999999)
    202 - Credential check used during login (matches_credentials)
    301 - Enrol in a new subject (add_enrolment)
    302 - Enforce the four-subject limit (can_enrol / add_enrolment)
    304 - Remove a subject from the enrolment list (remove_enrolment)
    305 - View the current enrolment list (view_enrolled)
    306 - Change password (set_password)
    501 - Persist itself through DataMgr (save)
"""

import random
from typing import Iterable, List, Optional

from enrolment import Enrolment
from validators import is_pass, mark_to_grade, validate_password

MAX_ENROLMENTS = 4
MAX_STUDENT_ID = 999_999


def generate_student_id(existing_ids: Iterable[str]) -> str:
    """Story 103: return a random, unused, zero-padded 6-digit student ID."""
    taken = set(existing_ids)
    if len(taken) >= MAX_STUDENT_ID:
        raise RuntimeError("No student IDs left to allocate.")

    while True:
        candidate = f"{random.randint(1, MAX_STUDENT_ID):06d}"
        if candidate not in taken:
            return candidate


class Student:
    """A registered student who can hold between 0 and 4 enrolments."""

    def __init__(self, name: str, email: str, password: str, student_id: str):
        self._name = name
        self._email = email
        self._password = password
        self._id = student_id
        self._enrolments: List[Enrolment] = []

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> str:
        return self._id

    def get_email(self) -> str:
        return self._email

    # ------------------------------------------------------------------
    # Account (stories 202, 306)
    # ------------------------------------------------------------------

    def set_password(self, new_password: str) -> bool:
        """Story 306: change the password if it passes validation."""
        if not validate_password(new_password):
            return False
        self._password = new_password
        return True

    def matches_credentials(self, email: str, password: str) -> bool:
        """Story 202: emails are case-insensitive, passwords are not."""
        return self._email.lower() == email.lower() and self._password == password

    # ------------------------------------------------------------------
    # Enrolments (stories 301-305)
    # ------------------------------------------------------------------

    def can_enrol(self) -> bool:
        """Story 302: True while the student is below the four-subject limit."""
        return len(self._enrolments) < MAX_ENROLMENTS

    def add_enrolment(self) -> Optional[Enrolment]:
        """
        Stories 301-303: enrol in a new auto-generated subject.

        Returns the new Enrolment, or None if the four-subject limit has
        already been reached (the caller is responsible for telling the user).
        """
        if not self.can_enrol():
            return None

        current_ids = {e.get_id() for e in self._enrolments}
        enrolment = Enrolment(existing_ids=current_ids)
        self._enrolments.append(enrolment)
        return enrolment

    def remove_enrolment(self, subject_id: str) -> bool:
        """Story 304: remove the subject with this ID. Returns False if not found."""
        subject_id = subject_id.strip()
        if subject_id.isdigit():
            subject_id = subject_id.zfill(3)  # lets the user type "7" for "007"

        for enrolment in self._enrolments:
            if enrolment.get_id() == subject_id:
                self._enrolments.remove(enrolment)
                return True
        return False

    def view_enrolled(self) -> List[Enrolment]:
        """Story 305: return a copy of the enrolment list (callers cannot mutate it)."""
        return list(self._enrolments)

    def enrolment_count(self) -> int:
        return len(self._enrolments)

    # ------------------------------------------------------------------
    # Results (used by the admin views, stories 403 and 406)
    # ------------------------------------------------------------------

    def get_average_mark(self) -> Optional[float]:
        """Average mark across all subjects, or None if not enrolled in any."""
        if not self._enrolments:
            return None
        return sum(e.get_mark() for e in self._enrolments) / len(self._enrolments)

    def get_overall_grade(self) -> Optional[str]:
        average = self.get_average_mark()
        return None if average is None else mark_to_grade(average)

    def is_passing(self) -> Optional[bool]:
        average = self.get_average_mark()
        return None if average is None else is_pass(average)

    # ------------------------------------------------------------------
    # Persistence (story 501)
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Persist this student via DataMgr (the <<use>> dependency in the diagram)."""
        # Imported here to avoid a circular import: data_mgr imports Student.
        from data_mgr import DataMgr
        DataMgr().save_student(self)

    def snapshot(self) -> dict:
        """Capture the current state so it can be restored if a save fails."""
        return self.to_dict()

    def restore(self, snapshot: dict) -> None:
        """Roll this student back to a state captured by snapshot()."""
        self._password = snapshot["password"]
        self._enrolments = [Enrolment.from_dict(e) for e in snapshot["enrolments"]]

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "email": self._email,
            "password": self._password,
            "id": self._id,
            "enrolments": [e.to_dict() for e in self._enrolments],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        student = cls(data["name"], data["email"], data["password"], str(data["id"]).zfill(6))
        student._enrolments = [Enrolment.from_dict(e) for e in data.get("enrolments", [])]
        return student

    def __str__(self) -> str:
        return f"{self._name} :: {self._id} --> Email: {self._email}"

    def __repr__(self) -> str:
        return f"Student(id={self._id!r}, name={self._name!r}, enrolments={len(self._enrolments)})"
