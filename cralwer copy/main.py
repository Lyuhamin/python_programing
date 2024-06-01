# main.py

from tkinter import Tk
from gui import SearchApp
import threading
from app import run_flask

def main():
    # Flask 서버를 별도의 스레드에서 실행
    threading.Thread(target=run_flask).start()

    # Tkinter 애플리케이션 실행
    root = Tk()
    app = SearchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
