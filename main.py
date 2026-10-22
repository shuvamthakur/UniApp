import sys
from views.cli_view import CLIView
from views.gui_view import LoginWindow

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "--gui":
        app = LoginWindow()
        app.mainloop()
    else:    
        app = CLIView()
        app.run_university_menu()