from models.student import Student
from models.subject import Subject


class EnrolController:
    def __init__(self):
        pass

    def add_enrolment(self, student, subject):
        if student is None or subject is None:
            return False

        student.add_subject(subject)
        return True

    def remove_enrolment(self, student, subject_id):
        if student is None:
            return False

        return student.remove_subject(subject_id)

    def view_enrolments(self, student):
        if student is None:
            return []

        return student.subjects
