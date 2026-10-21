"""
data_mgr.py
DataMgr: the only class that reads from or writes to students.data.

Stories covered:
    202 - Provide stored records for login verification
    404 - Remove a single student from the file
    405 - Clear the whole file
    501 - Save student registration and enrolment details

Data is stored as JSON so the file is human-readable while you develop.
Writes go to a temporary file first and are then swapped in, so a crash
mid-write can never leave students.data half-written.
"""

import json
import os
from typing import List, Optional

from student import Student

# students.data lives next to this file, wherever the app is launched from.
DEFAULT_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.data")


class DataFileError(Exception):
    """Raised when students.data cannot be read or written."""


class DataMgr:
    """Reads and writes Student objects to students.data."""

    def __init__(self, file_path: Optional[str] = None):
        # Read the module constant at call time so tests can point it elsewhere.
        self._file_path = file_path or DEFAULT_FILE_PATH

    # ------------------------------------------------------------------
    # Public API (matches the class diagram)
    # ------------------------------------------------------------------

    def save_student(self, student: Student) -> None:
        """Story 501: insert a new student or update an existing one by ID."""
        students = self.load_all_students()
        for index, existing in enumerate(students):
            if existing.get_id() == student.get_id():
                students[index] = student
                break
        else:
            students.append(student)
        self.save_all_students(students)

    def load_all_students(self) -> List[Student]:
        """Return every stored student. A missing or empty file means no students."""
        if not os.path.exists(self._file_path):
            return []

        try:
            with open(self._file_path, "r", encoding="utf-8") as handle:
                content = handle.read().strip()
            if not content:
                return []
            records = json.loads(content)
            if not isinstance(records, list):
                raise ValueError("expected a list of student records")
            return [Student.from_dict(record) for record in records]
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise DataFileError(
                f"Could not read '{self._file_path}'. The file may be corrupted: {error}"
            ) from error

    def delete_all_students(self) -> None:
        """Story 405: wipe every record from students.data."""
        self.save_all_students([])

    # ------------------------------------------------------------------
    # Supporting methods
    # ------------------------------------------------------------------

    def save_all_students(self, students: List[Student]) -> None:
        """Overwrite the file with the given list (written atomically)."""
        temp_path = self._file_path + ".tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as handle:
                json.dump([s.to_dict() for s in students], handle, indent=2)
            os.replace(temp_path, self._file_path)
        except OSError as error:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise DataFileError(
                f"Could not save to '{self._file_path}'. Check the file is not open in "
                f"another program and that you have permission to write to it ({error})."
            ) from error

    def remove_student(self, student_id: str) -> bool:
        """Story 404: delete one student by ID. Returns False if not found."""
        students = self.load_all_students()
        remaining = [s for s in students if s.get_id() != student_id]
        if len(remaining) == len(students):
            return False
        self.save_all_students(remaining)
        return True

    def get_file_path(self) -> str:
        return self._file_path
