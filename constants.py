import os

script_path = os.path.dirname(os.path.abspath(__file__))

STUDENTS_FILE = os.path.join(script_path, "students.data")
# create students.data file

EMAIL_REGEX = r"^[A-Za-z]+\.[A-Za-z]+@university\.com$"
# ^ = start regex
# [A-Za-z]+ = add multiple letters of any case
# \. = escapes dot so not wildcard
# $ = end regex

PASSWORD_REGEX = r"^[A-Z][A-Za-z]{5,}\d{3,}$"
# ^ = start regex
# [A-Z] = requires capital letter
# [A-Za-z]{5,} = add at least 5 letters of any case
# \d{3,} = add at least 3 digits
# $ = end regex

MAX_SUBJECTS = 4