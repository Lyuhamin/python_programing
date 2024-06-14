from tkinter import Tk
from gui import SearchApp
import multiprocessing
import app
import webbrowser
import time

def run_flask_app():
    app.app.run(debug=True, use_reloader=False)

def main():
    # Flask 서버를 별도의 프로세스에서 실행
    flask_process = multiprocessing.Process(target=run_flask_app)
    flask_process.start()

    # 잠시 대기하여 Flask 서버가 시작될 시간을 줌
    time.sleep(1)  # 필요에 따라 조정 가능

    # 웹 브라우저에서 Flask 앱 열기
    webbrowser.open("http://127.0.0.1:5000")

    # Tkinter 애플리케이션 실행
    root = Tk()
    app = SearchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
