from student_controller import StudentController

class University:

    def __init__(self):                                                             # constructor
        self.student_controller = StudentController()                               # call student controller

    def read_choice(self):
        print("University System: (A)dmin, (S)tudent, or X : ", end="")             # get user menu input
        return input().strip().upper()                                              # uppercases input so menu works

    def run_menu(self):                                                             # uni menu controls
        choice = self.read_choice()
        while choice != 'X':
            match choice:
                case 'A':
                    pass
                case 'S':
                    self.student_controller.run_menu()
                case _:
                    self.help()
            choice = self.read_choice()
        print("Thank You")

    def help(self):
        print("Menu options")
        print("\tA = Enter Admin")
        print("\tS = Log in as Student")
        print("\tX = Exit")

if __name__ == "__main__":                                                          # program starts here
    University().run_menu()