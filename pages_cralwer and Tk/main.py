from multiprocessing import Process
import webbrowser
import time

def start_flask():
    # app.py에서 정의한 Flask 애플리케이션 실행
    import app
    app.run_flask()

def start_tkinter():
    # gui.py에서 정의한 Tkinter 애플리케이션 실행
    import tkinter as tk
    from gui import SearchApp

    root = tk.Tk()
    app = SearchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    # Flask를 별도의 프로세스에서 실행
    flask_process = Process(target=start_flask)
    flask_process.start()

    # Flask 서버가 시작될 시간을 대기 (필요에 따라 조정)
    time.sleep(2)

    # 웹 브라우저에서 Flask 앱 열기
    webbrowser.open("http://127.0.0.1:5000")

    # Tkinter 애플리케이션 실행
    start_tkinter()

    # 프로그램 종료 시 Flask 프로세스도 종료
    flask_process.join()
