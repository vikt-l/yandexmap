from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
import sys


class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.delta = "0.005"

    def initUI(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.PgUp:
            if (int(self.delta) > 0) and (int(self.delta) + 0.001 < 100):
                self.delta = str(int(self.delta) + 0.001)
            pass
        if event.key() == Qt.PgDown:
            if (int(self.delta) > 0) and (int(self.delta) - 0.001 > 0):
                self.delta = str(int(self.delta) - 0.001)
            pass

    # code


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
