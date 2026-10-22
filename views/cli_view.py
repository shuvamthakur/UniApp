from controllers.auth_controller import AuthController
from controllers.enrol_controller import EnrolController
from controllers.admin_controller import AdminController
from utils.validators import validate_password

class CLIView:

    def __init__(self):
        self.auth_ctrl = AuthController()
        self.enrol_ctrl = EnrolController()
        self.admin_ctrl = AdminController()

        # =========================================================================   
        # 1. UNIVERSITY SYSTEM MENU (The Top Menu)
        # =========================================================================   
    def run_university_menu(self):
        while True:
            choice = input("University System: (A)dmin, (S)tudent, or X : ").strip().upper()
            if choice == "A":
                self.run_admin_menu()
            elif choice == "S":
                self.run_student_menu()
            elif choice == "X":
                print("Thank You")
                break

    # =========================================================================   
    # 2. STUDENT SYSTEM MENU (Nicole's Section: 100 & 200 Stories)
    # =========================================================================   
    def run_student_menu(self):
        while True:
            choice = input("\tStudent System (l/r/x): ").strip().lower()
            if choice == "l":
                student = self.student_login()
                if student:
                    self.run_course_menu(student)
            elif choice == "r":
                    self.student_register()
            elif choice == "x":
                    break
  
    def read_credentials(self):
        """Loops until email and password formats are valid."""
        while True:
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()
            if self.auth_ctrl.validate_email(email) and self.auth_ctrl.validate_password(password):
                print("\temail and password formats acceptable")
                return email, password
            print("\tIncorrect email or password format")

    def student_register(self):
        print("\tStudent Sign Up")
        email, password = self.read_credentials()
        existing = self.auth_ctrl.find_by_email(email)
        if existing:
            print(f"\tStudent {existing.name} already exists")
            return
        name = input("\tName: ").strip()
        self.auth_ctrl.register(name, email, password)
        print(f"\tEnrolling Student {name}")

    def student_login(self):
        print("\tStudent Sign In")
        email, password = self.read_credentials()
        student = self.auth_ctrl.authenticate(email, password)
        if student:
            return student
        print("\tStudent does not exist")
        return None

    # =========================================================================   
    # 3. SUBJECT ENROLMENT MENU (Jass's Section: 300 Stories)
    # =========================================================================   
    def run_course_menu(self, student):
        while True:
            choice = input("\tStudent Course Menu (c/e/r/s/x): ").strip().lower()

            if choice == "s":
                print(f"\tShowing {len(student.subjects)} subjects")
                for s in student.subjects:
                    print(f"\t{s}")
            elif choice == "e":
                success, msg, new_subj = self.enrol_ctrl.enrol_subject(student)   
                if success:
                    print(f"\t{msg}")
                    print(f"\tYou are now enrolled in {len(student.subjects)} out of 4 subjects")
                else:
                    print(f"\t{msg}")

            elif choice == "r":
                subj_id = input("\tRemove Subject by ID: ").strip()
                success, msg = self.enrol_ctrl.remove_subject(student, subj_id)   
                print(f"\t{msg}")
                print(f"\tYou are now enrolled in {len(student.subjects)} out of 4 subjects")

            elif choice == "c":
                self.change_password_flow(student)

            elif choice == "x":
                break

    def change_password_flow(self, student):
        print("\tUpdating Password")
        while True:
            new_pw = input("\tNew Password: ").strip()
            confirm_pw = input("\tConfirm Password: ").strip()
            if new_pw != confirm_pw:
                print("\tPassword does not match - try again")
                continue
            if not validate_password(new_pw):
                print("\tIncorrect password format")
                continue
            student.set_password(new_pw)
            self.enrol_ctrl.save_student(student)
            break

    # =========================================================================   
    # 4. ADMIN SYSTEM MENU (Nana's Section: 400 Stories)
    # =========================================================================   
    def run_admin_menu(self):
        pass

