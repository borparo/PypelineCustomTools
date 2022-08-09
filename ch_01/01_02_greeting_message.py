# 01_02_greeting_message.py
# GOAL: Add a button that prints the message from the field using lambda.
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PySide2.QtCore import Slot, Qt
import sys

class Greeting(QWidget):
    """
    Creates a widget where we can type a message to be printed in the console.
    """
    def __init__(self,parent=None):
        super(Greeting, self).__init__(parent, Qt.WindowStaysOnTopHint)  # Add window flag to keep widget on top main window
        self.setWindowTitle('Greetings!')
        self.setMinimumSize(252, 96)
        
        # Widgets
        greeting_label = QLabel('Greeting Message:', self)
        greeting_label.setGeometry(8, 4, 236, 24)
        
        self.message_le = QLineEdit(self, returnPressed=self.disable_le)
        self.message_le.setGeometry(8, 32, 236, 24)

        # EX_01 Button: Add a button and connect it the same slot as the line edit field.
        greeting_btn = QPushButton('Print Greeting', self)
        greeting_btn.clicked.connect(lambda: self.print_msg(self.message_le.text()))
        greeting_btn.setGeometry(8, 64, 236, 24)
        
        self.show() # We call the show method to display the widget.

    @Slot()
    def disable_le(self):
        """
        Disables the QLineEdit field.z
        """
        self.message_le.setDisabled(True)

    @Slot()
    def print_msg(self, msg):
        """
        Prints in the console the typed message.
        """
        try:
            if not msg:
                raise ValueError('Nothing to print. Field is empty.')
            else:
                print(msg)
                self.message_le.clear()
                self.message_le.setEnabled(True)
        except ValueError as e:
            print(e)


app = QApplication(sys.argv)   
greeting = Greeting()
sys.exit(app.exec_())

