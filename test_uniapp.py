"""
test_uniapp.py
Unit tests for CLIUniApp. Run with:  python -m unittest -v
"""

import os
import tempfile
import unittest

import data_mgr
from data_mgr import DataMgr
from enrolment import Enrolment, MAX_MARK, MIN_MARK
from student import MAX_ENROLMENTS, Student, generate_student_id
from validators import is_pass, mark_to_grade, validate_email, validate_password


class TestValidators(unittest.TestCase):
    """Story 102 and the grading scale from story 303."""

    def test_valid_emails(self):
        self.assertTrue(validate_email("john.smith@university.com"))
        self.assertTrue(validate_email("jsmith1@university.com"))
        self.assertTrue(validate_email("John.Smith@University.com"))

    def test_invalid_emails(self):
        for email in ("john@gmail.com", "@university.com", "john.university.com", "john@university.com.au"):
            self.assertFalse(validate_email(email), email)

    def test_valid_passwords(self):
        self.assertTrue(validate_password("Helloworld123"))
        self.assertTrue(validate_password("abc1234"))

    def test_invalid_passwords(self):
        for password in ("hello12", "123hello", "hello", "hello 123", ""):
            self.assertFalse(validate_password(password), password)

    def test_grade_boundaries(self):
        cases = {25: "Z", 49: "Z", 50: "P", 64: "P", 65: "C", 74: "C",
                 75: "D", 84: "D", 85: "HD", 100: "HD"}
        for mark, grade in cases.items():
            self.assertEqual(mark_to_grade(mark), grade, mark)

    def test_pass_threshold(self):
        self.assertTrue(is_pass(50))
        self.assertFalse(is_pass(49.99))


class TestEnrolment(unittest.TestCase):
    """Story 303."""

    def test_generated_values_in_range(self):
        for _ in range(500):
            e = Enrolment()
            self.assertEqual(len(e.get_id()), 3)
            self.assertTrue(1 <= int(e.get_id()) <= 999)
            self.assertTrue(MIN_MARK <= e.get_mark() <= MAX_MARK)
            self.assertEqual(e.get_grade(), mark_to_grade(e.get_mark()))

    def test_id_avoids_existing(self):
        taken = {f"{i:03d}" for i in range(1, 999)}  # only "999" left
        self.assertEqual(Enrolment(existing_ids=taken).get_id(), "999")

    def test_round_trip(self):
        e = Enrolment()
        copy = Enrolment.from_dict(e.to_dict())
        self.assertEqual((copy.get_id(), copy.get_mark(), copy.get_grade()),
                         (e.get_id(), e.get_mark(), e.get_grade()))


class TestStudentEnrolment(unittest.TestCase):
    """Stories 301, 302, 304, 305, 306."""

    def setUp(self):
        self.student = Student("John Smith", "john.smith@university.com", "Hello123", "000001")

    def test_enrol_up_to_limit(self):
        for _ in range(MAX_ENROLMENTS):
            self.assertIsNotNone(self.student.add_enrolment())
        self.assertFalse(self.student.can_enrol())
        self.assertIsNone(self.student.add_enrolment())
        self.assertEqual(self.student.enrolment_count(), MAX_ENROLMENTS)

    def test_subject_ids_unique_per_student(self):
        for _ in range(MAX_ENROLMENTS):
            self.student.add_enrolment()
        ids = [e.get_id() for e in self.student.view_enrolled()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_remove_enrolment(self):
        enrolment = self.student.add_enrolment()
        self.assertFalse(self.student.remove_enrolment("not-an-id"))
        self.assertTrue(self.student.remove_enrolment(enrolment.get_id()))
        self.assertEqual(self.student.enrolment_count(), 0)

    def test_remove_accepts_unpadded_id(self):
        enrolment = self.student.add_enrolment()
        self.assertTrue(self.student.remove_enrolment(str(int(enrolment.get_id()))))

    def test_view_enrolled_returns_copy(self):
        self.student.add_enrolment()
        self.student.view_enrolled().clear()
        self.assertEqual(self.student.enrolment_count(), 1)

    def test_set_password(self):
        self.assertFalse(self.student.set_password("weak"))
        self.assertTrue(self.student.matches_credentials("john.smith@university.com", "Hello123"))
        self.assertTrue(self.student.set_password("Newpass456"))
        self.assertTrue(self.student.matches_credentials("JOHN.SMITH@university.com", "Newpass456"))
        self.assertFalse(self.student.matches_credentials("john.smith@university.com", "Hello123"))


class TestStudentId(unittest.TestCase):
    """Story 103."""

    def test_format(self):
        sid = generate_student_id([])
        self.assertEqual(len(sid), 6)
        self.assertTrue(sid.isdigit())
        self.assertTrue(1 <= int(sid) <= 999_999)


class TestDataMgr(unittest.TestCase):
    """Stories 404, 405, 501."""

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.original_path = data_mgr.DEFAULT_FILE_PATH
        data_mgr.DEFAULT_FILE_PATH = os.path.join(self.tmp_dir.name, "students.data")

    def tearDown(self):
        data_mgr.DEFAULT_FILE_PATH = self.original_path
        self.tmp_dir.cleanup()

    def test_missing_file_means_no_students(self):
        self.assertEqual(DataMgr().load_all_students(), [])

    def test_save_load_update_remove_clear(self):
        student = Student("Jane Doe", "jane.doe@university.com", "Secret123", "000042")
        student.add_enrolment()
        student.save()

        loaded = DataMgr().load_all_students()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].get_id(), "000042")
        self.assertEqual(loaded[0].enrolment_count(), 1)

        student.add_enrolment()
        student.save()  # updates rather than duplicates
        loaded = DataMgr().load_all_students()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].enrolment_count(), 2)

        self.assertFalse(DataMgr().remove_student("999999"))
        self.assertTrue(DataMgr().remove_student("000042"))
        self.assertEqual(DataMgr().load_all_students(), [])

        student.save()
        DataMgr().delete_all_students()
        self.assertEqual(DataMgr().load_all_students(), [])

    def test_corrupted_file_raises(self):
        with open(data_mgr.DEFAULT_FILE_PATH, "w", encoding="utf-8") as handle:
            handle.write("{not json")
        with self.assertRaises(data_mgr.DataFileError):
            DataMgr().load_all_students()


    def test_non_list_file_raises(self):
        with open(data_mgr.DEFAULT_FILE_PATH, "w", encoding="utf-8") as handle:
            handle.write("{}")
        with self.assertRaises(data_mgr.DataFileError):
            DataMgr().load_all_students()

    def test_write_failure_raises_and_cleans_up(self):
        original_replace = data_mgr.os.replace

        def failing_replace(*_args):
            raise PermissionError("locked")

        data_mgr.os.replace = failing_replace
        try:
            with self.assertRaises(data_mgr.DataFileError):
                DataMgr().save_all_students([])
        finally:
            data_mgr.os.replace = original_replace
        self.assertFalse(os.path.exists(data_mgr.DEFAULT_FILE_PATH + ".tmp"))


class TestSnapshotRestore(unittest.TestCase):
    """Rollback used when a save fails."""

    def test_restore_undoes_changes(self):
        student = Student("A", "a@university.com", "Abc123", "000001")
        student.add_enrolment()
        snapshot = student.snapshot()
        student.add_enrolment()
        student.set_password("Changed999")
        student.restore(snapshot)
        self.assertEqual(student.enrolment_count(), 1)
        self.assertTrue(student.matches_credentials("a@university.com", "Abc123"))


if __name__ == "__main__":
    unittest.main()
