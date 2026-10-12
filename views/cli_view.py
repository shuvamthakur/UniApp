from controllers.auth_controller import AuthController

class CLIView:

    def __init__(self):
        self.auth = AuthController()

    def read_name(self):                                            # get new student name input
        print("\tName: ", end="")
        return input().strip()    
    
    def read_email(self):                                           # get new student email input
        print("\tEmail: ", end="")
        return input().strip()

    def read_password(self):                                        # get new/change student password input
        print("\tPassword: ", end="")
        return input().strip()

    def read_credentials(self):                                     # confirm both email, password meet criteria
        while True:
            email = self.read_email()
            password = self.read_password()
            if self.auth.validate_email(email) and self.auth.validate_password(password):
                print("\tEmail and password formats acceptable")
                return email, password
            print("\tIncorrect email or password")


    def register_flow(self):
        email, password = self.read_credentials()
        existing = self.auth.find_by_email(email)
        if existing:
            print(f"\tStudent {existing.name} already exists")
            return

        name = self.read_name()
        success, message, _ = self.auth.register(name, email, password)
        print(f"\t{message}")
    
    def login_flow(self):
        email, password = self.read_credentials()
        student = self.auth.authenticate(email, password)
        if student:
                # Hand-off to Jass's enrolment controller later:
                # EnrolController(student).run_menu()
            return student
        else:
            print("\tIncorrect email or password")
            return None

    def read_student_choice(self):                                          # show student menu
        print("\tStudent System (l/r/x): ", end="")
        return input().strip().lower()    
    
    def run_student_menu(self):                                                  # student menu controls
        choice = self.read_student_choice()
        while choice != 'x':
            match choice:
                case 'l':
                    s = self.login_flow()
                    if s:
                        pass #Jass's enrolment system will plug in here 
                case 'r':
                    self.register_flow()
                case _:
                    self.student_help()
            choice = self.read_student_choice()

    def student_help(self):
        print("\tMenu options")
        print("\tl = Log in")
        print("\tr = Register")
        print("\tx = Exit")

    def read_uni_choice(self):
        print("University System: (A)dmin, (S)tudent, or X : ", end="")             # get user menu input
        return input().strip().upper()

    def run_uni_menu(self):                                                             # uni menu controls
        choice = self.read_uni_choice()
        while choice != 'X':
            match choice:
                case 'A':
                    pass  # Nana's admin system will plug in here
                case 'S':
                    self.run_student_menu()
                case _:
                    self.uni_help()
            choice = self.read_uni_choice()
        print("Thank You")

    def uni_help(self):
        print("Menu options")
        print("\tA = Enter Admin")
        print("\tS = Log in as Student")
        print("\tX = Exit")
    