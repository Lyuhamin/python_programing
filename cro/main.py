from tkinter import Tk
from gui import SearchApp

def main():
    root = Tk()
    app = SearchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
