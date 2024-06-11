from tkinter import Tk
from gui import SearchApp

def main():
    # Tkinter 애플리케이션 실행
    root = Tk()
    app = SearchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
