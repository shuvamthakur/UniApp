from utils.validators import mark_to_grade, is_pass, validate_password

class Student:

    def __init__(self, id, name, email, password):                              # constructor, collect these data points
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def matches_credentials(self, email, password):                             # check student credentials match existing student
        return self.email == email and self.password == password

    def set_password(self, new_password):
        if not validate_password(new_password):
            return False
        self.password = new_password
        return True

    def add_subject(self, subject):
        if len(self.subjects) < 4:
            self.subjects.append(subject)
            return True
        return False

    def remove_subject(self, subject_id):
        target_id = str(subject_id).strip().zfill(3) if str(subject_id).strip().isdigit() else str(subject_id).strip()
        for subject in self.subjects:
            if subject._id == target_id:
                self.subjects.remove(subject)
                return True
        return False
    
    def get_average_mark(self):
        if not self.subjects:
            return None
        return sum(s.mark for s in self.subjects) / len(self.subjects)
    
    def get_grade(self):
        avg = self.get_average_mark()
        return None if avg is None else mark_to_grade(avg)

    def is_pass(self):
        avg = self.get_average_mark()
        return None if avg is None else is_pass(avg)
    
    #Aliases
    get_overall_grade = get_grade
    is_passing = is_pass
    enrolment_count = lambda self: len(self.subjects)

    def __str__(self):
        return f"{self.name} :: {self.id} --> Email: {self.email}"