import sys, threading, subprocess, time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import socket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEG Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        browser = QWebEngineView()
        browser.setUrl(QUrl("http://127.0.0.1:8000"))
        self.setCentralWidget(browser)

def start_django():
    subprocess.Popen(["python", "manage.py", "runserver", "127.0.0.1:8000"], stdout=subprocess.DEVNULL)


def wait_for_server(host, port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

if __name__ == "__main__":
    if wait_for_server("127.0.0.1", 8000):
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        print("❌ Django server tidak bisa dijangkau.")
