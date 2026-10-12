
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
        self.password = new_password

    def add_subject(self, subject):
        self.subjects.append(subject)

    def remove_subject(self, subject_id):
        for subject in self.subjects:
            if subject.id == subject_id:                                        # check student enroled in subject
                self.subjects.remove(subject)
                return True
        return False

    def __str__(self):                                                          # print student data
        return f"{self.name} :: {self.id} --> Email: {self.email}"