import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from MainWindow import Ui_Dialog


class MyDesiger(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyDesiger, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyDesiger()
    ui.show()
    sys.exit(app.exec_())