from models.database import Database

GRADES = ["Z", "P", "C", "D", "HD"]                                 # ascending order, as in the sample output


class AdminController:

    def __init__(self):                                             # constructor
        self.db = Database()

    def get_students(self):                                         # all students from students.data
        return self.db.read_from_file()

    def grade_groups(self):                                         # dictionary: grade -> list of students
        students = self.db.read_from_file()
        groups = {}
        for grade in GRADES:
            members = []
            for student in students:
                if student.get_grade() == grade:
                    members.append(student)
            if len(members) > 0:
                groups[grade] = members
        return groups

    def pass_fail_partition(self):                                  # dictionary: FAIL/PASS -> list of students
        students = self.db.read_from_file()
        partition = {"FAIL": [], "PASS": []}
        for student in students:
            if student.is_pass():
                partition["PASS"].append(student)
            else:
                partition["FAIL"].append(student)
        return partition

    def student_by_id(self, student_id):                            # lookup pattern
        for student in self.db.read_from_file():
            if student.id == student_id:
                return student
        return None
