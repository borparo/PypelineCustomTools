#06_01_doors_tool.py
#GOAL: Create a tool to set up basic rigs for doors

from PySide2.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QSlider, QSpinBox,
                                QCheckBox, QVBoxLayout, QHBoxLayout, QRadioButton)
from PySide2.QtCore import Slot, Qt
import sys


class Door():
    pass


class DoorsTool(QWidget):
    def __init__(self, parent=None):
        super(DoorsTool, self).__init__(parent, Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Doors Tool')

        # Widgets
        self.one_wing_door = None
        self.double_wing_door = None
        self.hinge_num_label = None
        self.hinge_number = None
        self.hinge_left = None
        self.hinge_right = None
        self.handle_ckb = None
        self.door_knobs_ckb = None
        self.create_door_btn = None
        
        self.initialize_ui()

        self.setLayout(self.create_layouts())
        self.show()

    def initialize_ui(self):
        self.one_wing_door = QPushButton('One Wing', self)

        self.double_wing_door = QPushButton('Double Wing', self)

        self.hinge_num_label = QLabel('Hinge Number:')
        self.hinge_number = QSpinBox(self)
        self.hinge_left = QRadioButton('Left', self)
        self.hinge_right = QRadioButton('Right', self)

        self.handle_ckb = QCheckBox('handle', self)
        self.door_knobs_ckb = QCheckBox('door knob', self)

        self.create_door_btn = QPushButton('Make Door')


    def create_layouts(self):
        doors_btn_layout = QHBoxLayout()
        doors_btn_layout.addWidget(self.one_wing_door)
        doors_btn_layout.addWidget(self.double_wing_door)

        hinges_layout = QHBoxLayout()
        hinges_layout.addWidget(self.hinge_num_label)
        hinges_layout.addWidget(self.hinge_number)
        hinges_layout.addWidget(self.hinge_left)
        hinges_layout.addWidget(self.hinge_right)

        door_addons_layout = QHBoxLayout()
        door_addons_layout.addWidget(self.handle_ckb)
        door_addons_layout.addWidget(self.door_knobs_ckb)


        main_layout = QVBoxLayout(self)
        main_layout.addLayout(doors_btn_layout)
        main_layout.addLayout(hinges_layout)
        main_layout.addLayout(door_addons_layout)
        main_layout.addWidget(self.create_door_btn)

        return main_layout

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tool = DoorsTool()
    sys.exit(app.exec_())
