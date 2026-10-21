"""
uniapp.py
UniApp: the entry point and menu system for CLIUniApp.

Run with:  python uniapp.py

Stories covered:
    101 - Register a student
    201 - Student login
    301-306 - Student course menu (enrol, remove, show, change password)
    401 - Admin access
    402 - View all students
    403 - Organise students by grade
    404 - Remove a student
    405 - Clear students.data
    406 - PASS / FAIL categorisation

As described in the brief, admin features are methods on UniApp rather than
a separate class, and the admin menu needs no login.
"""

import sys
from typing import List, Optional

from data_mgr import DataFileError, DataMgr
from student import MAX_ENROLMENTS, Student, generate_student_id
from validators import (
    EMAIL_RULE_TEXT,
    GRADE_ORDER,
    PASSWORD_RULE_TEXT,
    validate_email,
    validate_password,
)

DIVIDER = "-" * 60


def ask(prompt: str) -> str:
    """Read one line of input with surrounding whitespace removed."""
    return input(prompt).strip()


class UniApp:
    """Coordinates students, admin actions and persistence."""

    def __init__(self):
        # UniApp uses DataMgr to load at startup without keeping a reference to it.
        self._students: List[Student] = DataMgr().load_all_students()
        self._current_student: Optional[Student] = None

    # ==================================================================
    # Registration and login (stories 101-103, 201-202)
    # ==================================================================

    def _register_student(self, name: str, email: str, password: str) -> bool:
        """Story 101: validate details, generate an ID and save the student."""
        if not name:
            print("Name cannot be empty.")
            return False
        if not validate_email(email):
            print(f"Invalid email. {EMAIL_RULE_TEXT}")
            return False
        if not validate_password(password):
            print(f"Invalid password. {PASSWORD_RULE_TEXT}")
            return False
        if self._find_by_email(email):
            print(f"Student with email {email} already exists.")
            return False

        student_id = generate_student_id(s.get_id() for s in self._students)
        student = Student(name, email, password, student_id)
        try:
            student.save()
        except DataFileError as error:
            print(f"Registration failed. {error}")
            return False
        self._students.append(student)
        print(f"Registration successful. Welcome {name}! Your student ID is {student_id}.")
        return True

    def _student_login(self, email: str, password: str) -> bool:
        """Stories 201-202: check the credentials against stored records."""
        for student in self._students:
            if student.matches_credentials(email, password):
                self._current_student = student
                return True
        return False

    @staticmethod
    def _commit(student: Student, snapshot: dict) -> bool:
        """
        Save a student's changes. If saving fails, roll the change back so what
        the user sees always matches what is in students.data.
        """
        try:
            student.save()
            return True
        except DataFileError as error:
            student.restore(snapshot)
            print(f"Change not saved. {error}")
            return False

    def _find_by_email(self, email: str) -> Optional[Student]:
        for student in self._students:
            if student.get_email().lower() == email.lower():
                return student
        return None

    def _find_by_id(self, student_id: str) -> Optional[Student]:
        for student in self._students:
            if student.get_id() == student_id:
                return student
        return None

    # ==================================================================
    # Student menus
    # ==================================================================

    def _student_menu(self) -> None:
        """Login / register menu."""
        while True:
            print(DIVIDER)
            choice = ask("Student System: (l)ogin, (r)egister, or x to go back: ").lower()

            if choice == "l":
                email = ask("Email: ")
                password = ask("Password: ")
                if self._student_login(email, password):
                    print(f"Welcome back, {self._current_student.get_name()}.")
                    self._course_menu()
                else:
                    print("Incorrect email or password.")
            elif choice == "r":
                name = ask("Name: ")
                email = ask("Email: ")
                password = ask("Password: ")
                self._register_student(name, email, password)
            elif choice == "x":
                return
            else:
                print("Invalid option, please try again.")

    def _course_menu(self) -> None:
        """Stories 301-306: what a logged-in student can do."""
        while True:
            print(DIVIDER)
            choice = ask(
                "Student Course Menu: (c)hange password, (e)nrol, (r)emove, (s)how, or x to log out: "
            ).lower()

            if choice == "c":
                self._change_password()
            elif choice == "e":
                self._enrol_subject()
            elif choice == "r":
                self._remove_subject()
            elif choice == "s":
                self._show_enrolments()
            elif choice == "x":
                print("Logged out.")
                self._current_student = None
                return
            else:
                print("Invalid option, please try again.")

    def _enrol_subject(self) -> None:
        """Stories 301-303: enrol in an auto-generated subject, respecting the limit."""
        student = self._current_student
        snapshot = student.snapshot()
        enrolment = student.add_enrolment()
        if enrolment is None:
            print(f"Students are allowed to enrol in {MAX_ENROLMENTS} subjects only.")
            return

        if not self._commit(student, snapshot):
            return
        print(f"Enrolling in Subject-{enrolment.get_id()}")
        print(f"You are now enrolled in {student.enrolment_count()} out of {MAX_ENROLMENTS} subjects.")

    def _remove_subject(self) -> None:
        """Story 304: remove a subject by its ID."""
        student = self._current_student
        if student.enrolment_count() == 0:
            print("You are not enrolled in any subjects.")
            return

        self._show_enrolments()
        subject_id = ask("Enter the subject ID to remove: ")
        snapshot = student.snapshot()
        if student.remove_enrolment(subject_id):
            if not self._commit(student, snapshot):
                return
            print(f"Dropping Subject-{subject_id.zfill(3)}")
        else:
            print(f"Subject {subject_id} was not found in your enrolments.")
        print(f"You are now enrolled in {student.enrolment_count()} out of {MAX_ENROLMENTS} subjects.")

    def _show_enrolments(self) -> None:
        """Story 305: list the current enrolments."""
        enrolments = self._current_student.view_enrolled()
        print(f"Showing {len(enrolments)} subject(s)")
        for enrolment in enrolments:
            print(f"    {enrolment}")

    def _change_password(self) -> None:
        """Story 306: change password after validation and confirmation."""
        new_password = ask("New password: ")
        confirm = ask("Confirm password: ")

        if new_password != confirm:
            print("Passwords do not match.")
            return
        snapshot = self._current_student.snapshot()
        if not self._current_student.set_password(new_password):
            print(f"Invalid password. {PASSWORD_RULE_TEXT}")
            return

        if not self._commit(self._current_student, snapshot):
            return
        print("Password updated successfully.")

    # ==================================================================
    # Admin subsystem (stories 401-406)
    # ==================================================================

    def _enter_admin_menu(self) -> None:
        """Story 401: admin management menu."""
        while True:
            print(DIVIDER)
            choice = ask(
                "Admin System: (c)lear database, (g)roup by grade, (p)artition PASS/FAIL, "
                "(r)emove student, (s)how all, or x to go back: "
            ).lower()

            if choice == "c":
                self._clear_student_list()
            elif choice == "g":
                self._view_by_grade()
            elif choice == "p":
                self._categorise_pass_fail()
            elif choice == "r":
                self._remove_student(ask("Enter the student ID to remove: "))
            elif choice == "s":
                self._view_all_students()
            elif choice == "x":
                return
            else:
                print("Invalid option, please try again.")

    def _view_all_students(self) -> None:
        """Story 402: list every registered student."""
        print("Student List")
        if not self._students:
            print("    < Nothing to display >")
            return
        for student in self._students:
            print(f"    {student}")

    def _view_by_grade(self) -> None:
        """Story 403: group students by the grade of their average mark."""
        print("Grade Grouping")
        graded = [s for s in self._students if s.get_overall_grade() is not None]
        if not graded:
            print("    < Nothing to display >")
            return

        for grade in GRADE_ORDER:
            group = sorted(
                (s for s in graded if s.get_overall_grade() == grade),
                key=lambda s: s.get_average_mark(),
                reverse=True,
            )
            if group:
                print(f"{grade:>2} --> [")
                for student in group:
                    print(f"        {student.get_name()} :: {student.get_id()} "
                          f"--> GRADE: {grade:>2} - MARK: {student.get_average_mark():.2f}")
                print("    ]")

        self._print_unenrolled_note(len(self._students) - len(graded))

    def _categorise_pass_fail(self) -> None:
        """Story 406: split students into PASS (avg >= 50) and FAIL (avg < 50)."""
        print("PASS/FAIL Partition")
        graded = [s for s in self._students if s.is_passing() is not None]
        if not graded:
            print("    < Nothing to display >")
            self._print_unenrolled_note(len(self._students))
            return
        passed = [s for s in graded if s.is_passing()]
        failed = [s for s in graded if not s.is_passing()]

        for label, group in (("PASS", passed), ("FAIL", failed)):
            print(f"{label} --> [")
            for student in group:
                print(f"        {student.get_name()} :: {student.get_id()} "
                      f"--> GRADE: {student.get_overall_grade():>2} - MARK: {student.get_average_mark():.2f}")
            print("    ]")

        self._print_unenrolled_note(len(self._students) - len(graded))

    @staticmethod
    def _print_unenrolled_note(count: int) -> None:
        if count:
            print(f"    ({count} student(s) with no enrolments not shown)")

    def _remove_student(self, student_id: str) -> None:
        """Story 404: remove one student from memory and from the file."""
        student_id = student_id.zfill(6) if student_id.isdigit() else student_id
        student = self._find_by_id(student_id)
        if student is None:
            print(f"Student {student_id} does not exist.")
            return

        try:
            DataMgr().remove_student(student_id)
        except DataFileError as error:
            print(f"Student not removed. {error}")
            return
        self._students.remove(student)
        print(f"Removing student {student_id} ({student.get_name()}).")

    def _clear_student_list(self) -> None:
        """Story 405: wipe students.data after confirmation."""
        confirm = ask("Are you sure you want to clear the database (Y)ES / (N)O: ").lower()
        if confirm not in ("y", "yes"):
            print("Clear cancelled.")
            return

        try:
            DataMgr().delete_all_students()
        except DataFileError as error:
            print(f"Data not cleared. {error}")
            return
        self._students.clear()
        print("Students data cleared.")

    # ==================================================================
    # Entry point
    # ==================================================================

    def run(self) -> None:
        """Top-level menu shared by both actors."""
        while True:
            print(DIVIDER)
            choice = ask("University System: (A)dmin, (S)tudent, or X to exit: ").lower()

            if choice == "a":
                self._enter_admin_menu()
            elif choice == "s":
                self._student_menu()
            elif choice == "x":
                print("Thank you.")
                return
            else:
                print("Invalid option, please try again.")


def main() -> None:
    try:
        UniApp().run()
    except DataFileError as error:
        print(error)
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting. Goodbye.")


if __name__ == "__main__":
    main()
