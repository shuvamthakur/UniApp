import os
import pickle                                                               # supports read/write data to file
from utils.constants import STUDENTS_FILE

class Database:

    def __init__(self):                                                     # constructor
        try:
            students = []
            if not os.path.exists(STUDENTS_FILE):
                with open(STUDENTS_FILE, 'wb') as f:
                    pickle.dump(students, f)                                # save empty list

        except Exception as ex:
            print("Error occurred during initialization:", ex)

    def read_from_file(self):                                               # load student list from file
        students = []
        try:
            with open(STUDENTS_FILE, 'rb') as file_in:
                students = pickle.load(file_in)
        except FileNotFoundError as ex:
            print(f"File not found: {ex}")
        except IOError as ex:
            print(f"Reading error: {ex}")
        except EOFError as ex:
            print(f"End of file error: {ex}")                               # empty file error
        return students       

    def write_to_file(self, students):                                      # save student list to file
        try:
            with open(STUDENTS_FILE, 'wb') as file_out:
                pickle.dump(students, file_out)
        except FileNotFoundError as ex:
            print(f"File not found: {ex}")
        except IOError as ex:
            print(f"Writing error: {ex}")

    def clear(self):
        self.write_to_file([])                                              # clear student list