import re
import random
from constants import EMAIL_REGEX, PASSWORD_REGEX
from student import Student
from database import Database

class StudentController:

    def __init__(self):
        self.db = Database()                                        # create student database file if none                                          

    def read_name(self):                                            # get new student name input
        print("\tName: ", end="")
        return input().strip()
    
    def read_email(self):                                           # get new student email input
        print("\tEmail: ", end="")
        return input().strip()

    def read_password(self):                                        # get new/change student password input
        print("\tPassword: ", end="")
        return input().strip()
    
    def check_email(self, email):                                   # new student email meets criteria?
        if re.fullmatch(EMAIL_REGEX, email):
            return True
        else:
            return False

    def check_password(self, password):                             # new/change student password meets criteria?
        if re.fullmatch(PASSWORD_REGEX, password):
            return True
        else:
            return False

    def read_credentials(self):                                     # confirm both email, password meet criteria
        while True:
            email = self.read_email()
            password = self.read_password()
            if self.check_email(email) and self.check_password(password):
                print("\tEmail and password formats acceptable")
                return email, password
            print("\tIncorrect email or password format")

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
        
    def register(self):                                             # creates new student object (profile), save to students.data
        email, password = self.read_credentials()  
        existing = self.find_by_email(email)
        if existing:
            print(f"\tStudent {existing.name} already exists")
            return
        name = self.read_name()
        students = self.db.read_from_file()
        new_student = Student(self.generate_id(students), name, email, password)
        students.append(new_student)
        self.db.write_to_file(students)
        print(f"\tEnrolling Student {name}")

    def authenticate(self, email, password):                        # validate student email, pw combo correct
        students = self.db.read_from_file()
        for s in students:
            if s.matches_credentials(email, password):
                return s
        return None

    def student_login(self):                                        # log in existing student
        email, password = self.read_credentials()                       
        s = self.authenticate(email, password)
        if s:
            return s
        else:
            print (f"\tIncorrect email or password")
            return None

    def read_choice(self):                                          # show student menu
        print("\tStudent System (l/r/x): ", end="")
        return input().strip().lower()

    def run_menu(self):                                                  # student menu controls
        choice = self.read_choice()
        while choice != 'x':
            match choice:
                case 'l':
                    s = self.student_login()
                    if s:
                        pass
                case 'r':
                    self.register()
                case _:
                    self.help()
            choice = self.read_choice()

    def help(self):
        print("\tMenu options")
        print("\tl = Log in")
        print("\tr = Register")
        print("\tx = Exit")