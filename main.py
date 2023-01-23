from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys


class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
