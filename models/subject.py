import random
from typing import Iterable, Optional
from utils.validators import is_pass, mark_to_grade


MIN_MARK = 25
MAX_MARK = 100
MAX_SUBJECT_ID = 999  # IDs run from 001 to 999

class Subject:
    """A single subject enrolment with an auto-generated ID, mark and grade."""

    def __init__(self, existing_ids=None):
        """
        Create a new enrolment.

        existing_ids: subject IDs the student already holds, so the new ID is
        never a duplicate within that student's enrolment list.
        """
        self._id = ""
        self._mark = 0
        self._grade = ""

        self._generate_id(existing_ids or ())
        self._generate_mark()
        self._calculate_grade()


    # ------------------------------------------------------------------
    # Private generation methods (story 303)
    # ------------------------------------------------------------------

    def _generate_id(self, existing_ids: Optional[Iterable[str]]) -> None:
        """Generate a unique, zero-padded 3-digit subject ID (001-999)."""
        taken = set(existing_ids)
        if len(taken) >= MAX_SUBJECT_ID:
            raise RuntimeError("No subject IDs left to allocate.")

        while True:
            candidate = f"{random.randint(1, MAX_SUBJECT_ID):03d}"
            if candidate not in taken:
                self._id = candidate
                return
    
    def _generate_mark(self) -> None:
        """Generate a random whole-number mark between 25 and 100 inclusive."""
        self._mark = random.randint(MIN_MARK, MAX_MARK)

    def _calculate_grade(self) -> None:
        """Derive the grade from the mark using the shared grading scale."""
        self._grade = mark_to_grade(self._mark)


    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------
    @property
    def get_id(self) -> str:
        return self._id
    @property
    def get_mark(self) -> int:
        return self._mark
    @property
    def get_grade(self) -> str:
        return self._grade
    @property
    def is_pass(self) -> bool:
        return is_pass(self._mark)

    # ------------------------------------------------------------------
    # Persistence helpers (used by DataMgr, story 501)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {"id": self._id, "mark": self._mark, "grade": self._grade}

    @classmethod
    def from_dict(cls, data: dict) -> "Enrolment":
        """Rebuild a saved enrolment without generating new random values."""
        enrolment = cls.__new__(cls)
        enrolment._id = str(data["id"]).zfill(3)
        enrolment._mark = int(data["mark"])
        enrolment._calculate_grade()  # grade is always recomputed from the mark
        return enrolment

    def __str__(self) -> str:
        return f"[ Subject::{self._id} -- mark = {self._mark:>3} -- grade = {self._grade:>2} ]"

    def __repr__(self) -> str:
        return f"Enrolment(id={self._id!r}, mark={self._mark}, grade={self._grade!r})"
