# 05_01_renamer.py
# GOAL: Add 2 buttons to the widget: 1 renames the selected object when clicked, other cancels and closes widget.
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPalette, QColor
from pyfbsdk import FBModelList, FBGetSelectedModels, FBModel
import pythonidelib


class Renamer(QWidget):
    
    def __init__(self, parent=None):
        super(Renamer, self).__init__(parent, Qt.WindowStaysOnTopHint)  # The flag will ensure the widget stays on top the main application window.
        
        self.setWindowTitle('Renamer')
        self.setMinimumSize(212, 96)

        # Widgets
        selected_label = QLabel('Selected Model:', self)
        self.selected_name_label = QLabel(self)

        self.model = self.get_selected_model(0)
        try:
            if not self.model:
                raise AttributeError('Nothing selected. None has not Name attribute.')
            else:
                self.selected_name_label.setText(self.model.Name)  # gets the name of the first selected model
        except AttributeError as e:
            print(e)
            pythonidelib.FlushOutput()

        self.selected_name_label.setEnabled(False)
        
        new_name_label = QLabel('New Name:', self)

        self.new_name_le = QLineEdit(self, returnPressed=self.rename_selected)
        self.new_name_le.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        rename_btn = QPushButton('Rename', self, clicked=self.rename_selected)
        
        palette = rename_btn.palette()
        palette.setColor(QPalette.Button, QColor(Qt.darkGreen))
        rename_btn.setAutoFillBackground(True)
        rename_btn.setPalette(palette)
        rename_btn.update()

        cancel_btn = QPushButton('Cancel', self, clicked=self.close)
        
        palette = cancel_btn.palette()
        palette.setColor(QPalette.Button, QColor(Qt.darkRed))
        cancel_btn.setAutoFillBackground(True)
        cancel_btn.setPalette(palette)
        cancel_btn.update()
        
        # Layouts
        selected_layout = QHBoxLayout()
        selected_layout.addWidget(selected_label)
        selected_layout.addWidget(self.selected_name_label, Qt.AlignLeft)
        selected_layout.addStretch(1)
        
        new_name_layout = QHBoxLayout()
        new_name_layout.addWidget(new_name_label)
        new_name_layout.addWidget(self.new_name_le)
        new_name_layout.addStretch(1)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(rename_btn)
        buttons_layout.addWidget(cancel_btn)
        
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(selected_layout)
        main_layout.addLayout(new_name_layout)
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
        self.show()
    
    def get_selected_model(self, index:int)->FBModel:
        """
        Returns a model, selected by it's position in the current selection list. 
        """
        try:
            self.current_selection = FBModelList()
            FBGetSelectedModels(self.current_selection)
            if not self.current_selection:
                raise IndexError('WARNING: Nothing selected. Please select 1 model and run the script again.')
            else:
                return self.current_selection[index]
        except IndexError as e:
            print(e)
            pythonidelib.FlushOutput()
    
    @Slot()    
    def rename_selected(self)->None:
        """
        Changes the name of the first model of the current active selection.
        """
        try:
            if not self.new_name_le.text():
                raise ValueError('ERROR: Field is empty. Please type a new name.')
            else:
                self.model.Name = str(self.new_name_le.text())
                self.selected_name_label.setText(self.new_name_le.text())
                self.new_name_le.clear()
        except ValueError as e:
            print(e)
            pythonidelib.FlushOutput()
    
window = Renamer()
        