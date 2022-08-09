# 00_00_greeting.py
# GOAL: Create a window that displays 'Hello World'.
from PySide2.QtWidgets import QApplication, QWidget, QLabel
import sys


class Greeting(QWidget):
    def __init__(self, parent=None):
        super(Greeting,self).__init__(parent)
        self.setWindowTitle('Greetings!')

        greeting_label = QLabel("Hello World!", self)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Greeting()
    sys.exit(app.exec_())

