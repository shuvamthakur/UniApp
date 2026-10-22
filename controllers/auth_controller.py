import re
import random
from utils.constants import EMAIL_REGEX, PASSWORD_REGEX
from models.student import Student
from models.database import Database
from utils.validators import validate_email, validate_password

class AuthController:
    def __init__(self):
        self.db = Database()

    def validate_email(self, email: str) -> bool:
        return validate_email(email)


    def validate_password(self, password: str) -> bool:
        return validate_password(password)

    def find_by_email(self, email):                                 # validate student doesn't already exist
        students = self.db.read_from_file()
        for s in students:
            if s.email == email:
                return s
        return None


    def generate_id(self, students):                                # create student id
        while True:
            number = random.randint(1, 999999)                      # auto-generate random 6 digit integer
            new_id = f"{number:06d}"                                # convert integer to string, front pad w zeros
            taken = False                                           # check id not yet taken
            for n in students:
                if n.id == new_id:
                    taken = True
            if not taken:
                return new_id

    def register(self, name, email, password):                                             # creates new student object (profile), save to students.data
        if self.find_by_email(email):
            return False, f"Student {name} already exists", None

        students = self.db.read_from_file()
        new_student = Student(self.generate_id(students), name, email, password)
        students.append(new_student)
        self.db.write_to_file(students)
        return True, f"Enrolling Student {name}",new_student

    def authenticate(self, email, password):                        # validate student email, pw combo correct
        students = self.db.read_from_file()
        for s in students:
            if s.matches_credentials(email, password):
                print(f"\tLogin Found!")
                return s
        return None
    
