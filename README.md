# CLIUniApp – University Self-Enrolment System

Group Cmp1-08 (Group 8): Shuvam Thakur, Nana Ellis, Nicole Davenport, Jasspreet Singh

A command-line application where students register, log in and manage their subject
enrolments, and admins manage student records. All data is saved to `students.data`.

## Requirements

Python 3.8 or newer. No third-party packages are needed.

## How to run

```bash
python uniapp.py
```

Run the tests with:

```bash
python -m unittest -v
```

## Project structure

| File | Class / contents | User stories |
|---|---|---|
| `uniapp.py` | `UniApp` – entry point, menus, admin functions | 101, 201, 301–306 (menu), 401–406 |
| `student.py` | `Student`, `generate_student_id()` | 103, 202, 301, 302, 304, 305, 306 |
| `enrolment.py` | `Enrolment` – subject ID, mark, grade | 303 |
| `data_mgr.py` | `DataMgr` – reads/writes `students.data` | 404, 405, 501 |
| `validators.py` | Email/password rules, grading scale, pass mark | 102, 303, 306, 406 |
| `test_uniapp.py` | Unit tests | All |

## Business rules

- Email must end in `@university.com`.
- Password must be letters followed by at least 3 digits (e.g. `Helloworld123`).
- Student IDs are random, unique and 6 digits (`000001`–`999999`).
- A student can enrol in at most 4 subjects.
- Each subject gets a random 3-digit ID (`001`–`999`) and a random mark from 25 to 100.
- Grades: Z < 50, P 50–64, C 65–74, D 75–84, HD ≥ 85.
- Admin grade grouping and PASS/FAIL use each student's average mark (PASS ≥ 50).

## Menus

```
University System: (A)dmin, (S)tudent, or X
  Student System: (l)ogin, (r)egister, or x
    Student Course Menu: (c)hange password, (e)nrol, (r)emove, (s)how, or x
  Admin System: (c)lear database, (g)roup by grade, (p)artition PASS/FAIL,
                (r)emove student, (s)how all, or x
```

## Design notes

- The class structure follows the group's UML class diagram. Admin functions are methods
  on `UniApp`, as explained in the design report.
- Private methods in the diagram (`-`) use a leading underscore in Python.
- `students.data` is stored as JSON and written atomically so a crash cannot corrupt it.
- Passwords are stored in plain text because the brief requires no hashing; a real system
  would hash them.

Included is some information about a GitHub repository and its language composition.
repo: shuvamthakur/UniApp
repo ID: 1412917940
The language composition of this repo is [{"name":"Python","percent":100}]
