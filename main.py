from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
import sys


class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            pass
        if event.key() == Qt.Key_Down:
            pass

    # code



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
