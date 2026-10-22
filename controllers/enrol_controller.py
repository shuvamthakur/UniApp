from models.subject import Subject
from models.database import Database
from utils.constants import MAX_SUBJECTS


class EnrolController:
    def __init__(self):
        self.db = Database()

    def enrol_subject(self, student):
        if len(student.subjects) >= MAX_SUBJECTS:
            return False, f"Students are allowed to enrol in {MAX_SUBJECTS} subjects only", None

        existing_ids = [s._id for s in student.subjects]
        new_subject = Subject(existing_ids=existing_ids)
        student.add_subject(new_subject)
        self.save_student(student)
        return True, f"Enrolling in Subject-{new_subject._id}", new_subject

    def remove_subject(self, student, subject_id):
        target_id = str(subject_id).strip().zfill(3) if str(subject_id).strip().isdigit() else str(subject_id).strip()
        removed = student.remove_subject(target_id)
        if removed:
            self.save_student(student)
            return True, f"Droping Subject-{target_id}"
        return False, f"Subject-{target_id} does not exist"

    def save_student(self, student):
        all_students = self.db.read_from_file()
        for i, s in enumerate(all_students):
            if s.id == student.id:
                all_students[i] = student
                break
        self.db.write_to_file(all_students)
