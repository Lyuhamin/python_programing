from tkinter import Tk
from gui import SearchApp
import multiprocessing
import app

def run_flask_app():
    app.app.run(debug=True, use_reloader=False)

def main():
    # Flask 서버를 별도의 프로세스에서 실행
    flask_process = multiprocessing.Process(target=run_flask_app)
    flask_process.start()

    # Tkinter 애플리케이션 실행
    root = Tk()
    app = SearchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()



if __name__ == "__main__":
    main()
