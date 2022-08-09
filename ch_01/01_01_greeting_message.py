# 01_01_greeting_message.py
# GOAL: Create our own 'Hello World!' version using PySide.
from PySide2.QtWidgets import QApplication, QDialog, QWidget, QLabel, QLineEdit, QPushButton
from PySide2.QtCore import Slot, Qt
import sys

class Greeting(QWidget):
    """
    Creates a widget where we can type a message to be printed in the console.
    """
    def __init__(self,parent=None):
        super(Greeting, self).__init__(parent, Qt.WindowStaysOnTopHint)  # Add window flag to keep widget on top main window
        self.setWindowTitle('Greetings!')
        self.setMinimumSize(252, 64)
        
        # Widgets
        greeting_label = QLabel('Greeting Message:', self)
        greeting_label.setGeometry(8, 4, 236, 24)
        
        self.message_le = QLineEdit(self, returnPressed=self.print_msg)
        self.message_le.setGeometry(8, 32, 236, 24)
        
        self.show()
        
    @Slot()
    def print_msg(self):
        """
        Prints in the console the typed message.
        """
        try:
            if not self.message_le.text():
                raise ValueError('Nothing to print. Field is empty.')
            else:
                print(self.message_le.text())
                self.message_le.clear()
                
        except ValueError as e:
            print(e)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    greeting = Greeting()
    sys.exit(app.exec_())
