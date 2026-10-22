import tkinter as tk
from controllers.auth_controller import AuthController


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
        self.show_welcome_window(student)

    def show_welcome_window(self, student):
        welcome_win = tk.Toplevel(self) #for always appearing on top after initialized
        welcome_win.title(f"Welcome - {student.name}")
        welcome_win.geometry("320x180")

        welcome_win.resizable(False,False)

        frame = tk.Frame(welcome_win,padx = 20, pady = 20)
        frame.pack(expand=True, fill="both")

        first_message = tk.Label(frame, text=f"Welcome, {student.name}!", font=("Arial",12,"bold"))
        first_message.pack(pady=5)
        second_message = tk.Label(frame, text=f"ID: {student.id}\nEmail: {student.email}", justify="center")
        second_message.pack(pady=5)
        def on_close(): #helper function
            welcome_win.destroy()
            self.deiconify()

        logout_btn = tk.Button(frame,text="Log Out", command = on_close)
        logout_btn.pack(pady=5)
        # welcome_win.protocol("WM_DELETE_WINDOW",on_close)


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()