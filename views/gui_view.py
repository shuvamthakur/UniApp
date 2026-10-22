import tkinter as tk
from controllers.auth_controller import AuthController
from controllers.enrol_controller import EnrolController
from utils.constants import MAX_SUBJECTS


class ExceptionWindow(tk.Toplevel):
    def __init__(self, parent, title: str, message:str):
        super().__init__(parent)
        self.title(title)
        self.geometry("340x140")
        self.resizable(False, False)
        self.grab_set() #forces focus to this window

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        error_label = tk.Label(frame, text = message, wraplength=280, justify="center", foreground= "red")
        error_label.pack(pady=10)
        ok_button=tk.Button(frame, text="OK", command = self.destroy)
        ok_button.pack(pady=5)

class SubjectWindow(tk.Toplevel):
    """Display all enrolled subjects with their marks and grades in a table"""
    def __init__(self, parent, student):
        super().__init__(parent)
        self.title(f"Enrolled Subjects - {student.name}")
        self.geometry("450x300")
        self.resizable(False,False)
        self.grab_set()

        frame = tk.Frame(self, padx = 20, pady=15)
        frame.pack(expand=True, fill="both")

        title_label = tk.Label(frame, text=f"Subject List for {student.name}({student.id})",font=("Arial",12,"bold"))
        title_label.pack(pady=(0,10))

        #header for the listbox
        header_text= f"{'Subject Id':<18}{'Mark':<14}{'Grade':<10}"
        header_label = tk.Label(frame,text=header_text,font=("Courier",10,"bold"),anchor="w")
        header_label.pack(fill="x")

        #Listbox with Scrollbar 
        list_frame = tk.Frame(frame)
        list_frame.pack(fill="both", expand=True, pady=5)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Courier", 10),
            height=5,
            selectmode="none"
        )
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)

        # Populate rows
        if not student.subjects:
            self.listbox.insert("end", "No subjects enrolled yet.")
        else:
            for s in student.subjects:
                row_str = f"Subject-{s.id:<10}{str(s.mark):<14}{s.grade:<10}"
                self.listbox.insert("end", row_str)

        # Overall Summary
        avg = student.get_average_mark()
        avg_str = f"{avg:.2f}" if avg is not None else "N/A"
        grade_str = student.get_grade() or "N/A"

        summary_label = tk.Label(
            frame,
            text=f"Overall Average: {avg_str}   |   Overall Grade: {grade_str}",
            font=("Arial", 10, "italic")
        )
        summary_label.pack(pady=8)

        close_btn = tk.Button(frame, text="Close", width=12, command=self.destroy)
        close_btn.pack(pady=4)


class EnrolmentWindow(tk.Toplevel):
    """Allows student to enrol in subjects, view enrolments, and log out."""

    def __init__(self, parent, student):
        super().__init__(parent)
        self.parent = parent
        self.student = student
        self.enrol_ctrl = EnrolController()

        self.title(f"Subject Enrolment - {student.name}")
        self.geometry("400x320")
        self.resizable(False, False)

        frame = tk.Frame(self, padx=25, pady=20)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Subject Enrolment System", font=("Arial", 14, "bold")).pack(pady=(0, 5))    
        tk.Label(frame, text=f"Welcome, {student.name}! (ID: {student.id})", font=("Arial", 10)).pack(pady=2)

        # Dynamic Status text
        self.status_label = tk.Label(
            frame,
            text=f"You are currently enrolled in {len(student.subjects)} out of {MAX_SUBJECTS} subjects.",
            justify="center",
            font=("Arial", 10, "bold"),
            fg="#0055aa"
        )
        self.status_label.pack(pady=15)

        # Action Buttons
        enrol_btn = tk.Button(frame, text="Enrol in a Subject", height=1, command=self.handle_enrol)      
        enrol_btn.pack(fill="x", pady=5)

        view_btn = tk.Button(frame, text="View Enrolled Subjects", height=1, command=self.handle_view_subjects)
        view_btn.pack(fill="x", pady=5)

        logout_btn = tk.Button(frame, text="Log Out", height=1, command=self.handle_logout)
        logout_btn.pack(fill="x", pady=10)

        # Handle window 'X' button
        self.protocol("WM_DELETE_WINDOW", self.handle_logout)

    def handle_enrol(self):
        # 4-Subject Limit Exception Check
        if len(self.student.subjects) >= MAX_SUBJECTS:
            ExceptionWindow(
                self,
                "Enrolment Limit Reached",
                f"Students are allowed to enrol in {MAX_SUBJECTS} subjects only.")
            return

        # Enrol via Controller
        success, msg, new_subj = self.enrol_ctrl.enrol_subject(self.student)
        if success:
            self.status_label.config(
            text=f"Enrolled in Subject-{new_subj.id} (Mark: {new_subj.mark}, Grade: {new_subj.grade})\n"
                 f"Total: {len(self.student.subjects)} out of {MAX_SUBJECTS} subjects.")

    def handle_view_subjects(self):
        # Open Window 3
        SubjectWindow(self, self.student)

    def handle_logout(self):
        self.destroy()
        self.parent.deiconify()  # Restore login window



class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.auth = AuthController()
        self.title("GUIUniApp - Student Login")
        self.geometry("360x260")
        self.resizable(False,False)
        frame = tk.Frame(self, padx=25, pady=25)
        frame.pack(expand = True, fill="both")
        heading = tk.Label(frame, text = "Student Sign In", font=("Arial", 14, "bold"))

        heading.pack(pady = 10)

        email_label = tk.Label(frame, text="Email:")
        email_label.pack(anchor="w")

        self.email_entry = tk.Entry(frame, width = 35)
        self.email_entry.pack(fill="x", pady=(0,10))

        password_label = tk.Label(frame, text="Password:")
        password_label.pack(anchor="w")

        self.password_entry = tk.Entry(frame, width=25, show="*")
        self.password_entry.pack(fill="x", pady=(0,15))

        login_btn = tk.Button(frame, text="Log In", command=self.handle_login)
        login_btn.pack(fill="x", pady=5)

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            ExceptionWindow(self, "Input Error", "Please fill in both email and password fields.")
            return

        if not self.auth.validate_email(email) or not self.auth.validate_password(password):
            ExceptionWindow(self, "Format Error","Incorrect email or password format")
            return
    
        student = self.auth.authenticate(email, password)

        if not student:
            ExceptionWindow(self, "Login Error", "Student does not exist or credentials invalid.")
            return

        self.withdraw()
        EnrolmentWindow(self,student)


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()