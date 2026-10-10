# CLIUniApp: University and Student System (Nicole's part)

Context for teammates (and any AI assistant you share this with). Python 3.10+ required (uses `match`).

## A note on AI use

The brief says AI-generated code can receive zero. Use an AI to explain this code, review your own code, and find bugs. Do not have it write all of your code verbatim for the submission.

## What exists

| File | Role |
|---|---|
| `constants.py` | Shared values: `STUDENTS_FILE`, `EMAIL_REGEX`, `PASSWORD_REGEX`, `MAX_SUBJECTS` |
| `database.py` | `Database` class. Creates `students.data` if missing, reads, writes, clears (pickle) |
| `student.py` | `Student` model. Data and rules only, no `print()` or `input()` |
| `student_controller.py` | `StudentController`. Student menu (l/r/x), register, login, regex checks, ID generation |
| `university.py` | `University`. Top menu (A/S/X). **Run this file to start the app** |

Not built yet (teammates): `Subject`, subject enrolment controller, admin controller, GUI.

## Architecture

- **Model** (`Student`, `Database`): holds data and rules. Never prints or asks for input.
- **Controller** (`StudentController`, `University`): owns the menus, prompts and printing. Talks to the Model.
- Imports point one way: controllers import models and constants. Models never import controllers.

## Shared contracts (please follow these)

**Database** (`from database import Database`)
- `db = Database()` creates `students.data` if missing
- `db.read_from_file()` returns the list of `Student` objects (`[]` if empty)
- `db.write_to_file(students)` saves the whole list
- `db.clear()` writes an empty list

Pattern: **read the list, change it, write the whole list back.** Anything that changes a student (enrolling, removing a subject, changing password) must call `write_to_file` afterwards, or `students.data` goes stale.

**Student** fields: `id`, `name`, `email`, `password`, `subjects` (list). Read them directly (`student.name`), no getters.
Methods: `matches_credentials(email, password)`, `set_password(new_password)`, `add_subject(subject)`, `remove_subject(subject_id)` (returns True/False), `__str__` (admin list line).

**Conventions**
- Student IDs are 6-digit strings, e.g. `"000042"`.
- Subject IDs should be 3-digit zero-padded strings, e.g. `"097"`. Pad user input with `.zfill(3)` before comparing.
- `Subject` needs an `id` field, because `Student.remove_subject` compares `subject.id`.
- Use `MAX_SUBJECTS` from `constants.py` for the 4-subject limit.
- Menu output is indented with `\t` to match the sample I/O.

## Hand-off points

1. **Enrolment:** in `student_controller.py`, `run_menu`, `case 'l'`. After login, `s` is the logged-in `Student`. The `pass` there should call the enrolment controller with `s`.
2. **Admin:** in `university.py`, `run_menu`, `case 'A'`. The `pass` there should call the admin controller.

## Deliberate deviations from the brief (flag in the contribution statement)

- **Password regex:** `^[A-Z][A-Za-z]{5,}\d{3,}$`. The brief's wording ("at least five letters") would accept `Hello123`, but the sample I/O rejects it, so we follow the sample. Confirm with the tutor.
- **Login failure message:** prints `Incorrect email or password` instead of the sample's `Student does not exist`, because the sample wording reads as if the person does not exist.

## Run

```
python university.py
```
Type `S`, then `r` to register or `l` to log in. `x` goes back, `X` exits.
