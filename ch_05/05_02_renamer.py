# 05_02_renamer.py
# GOAL: Use comboboxes to add prefixes and suffixes to the new name.
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPalette, QColor
from pyfbsdk import FBModelList, FBGetSelectedModels, FBModel
import pythonidelib


class Renamer(QWidget):
    def __init__(self,parent=None):
        super(Renamer, self).__init__(parent, Qt.WindowStaysOnTopHint)  # Add window flag to keep widget on top main window
        self.setWindowTitle('Renamer')
        self.setMinimumSize(216, 128)

        # Widgets
        selected_label = QLabel('Current Name:', self)

        try:
            self.model = self.get_selected_model(0)
            self.selected_name_label = QLabel(self)
            if not self.model:
                raise AttributeError('WARNING: Nothing selected. None has not Name attribute.')
            else:
                self.selected_name_label.setText(self.model.Name)  # gets the name of the first selected model
            self.selected_name_label.setEnabled(False)
        except AttributeError as e:
            print(e)
            pythonidelib.FlushOutput()
        
        new_name_label = QLabel('New Name:', self)
        
        self.new_name_le = QLineEdit(self, returnPressed=self.rename_selected)

        prefix_label = QLabel('Prefix:', self)
        prefixes = ["LEARN", "TST", "TUT"]
        prefix_cb = QComboBox(self)
        prefix_cb.addItems(prefixes)
        prefix_cb.setObjectName('prefix')
        prefix_cb.activated.connect(self.insert_addon)

        suffix_label = QLabel('Suffix:', self)
        suffixes = ["QT", "PYSIDE", "SCRIPT"]
        suffix_cb = QComboBox(self)
        suffix_cb.addItems(suffixes)
        suffix_cb.setObjectName('suffix')
        suffix_cb.activated.connect(self.insert_addon)

        rename_btn = QPushButton('Rename', self, clicked=self.rename_selected)
        rename_btn.setAutoFillBackground(True)
        palette = rename_btn.palette()
        palette.setColor(QPalette.Button, QColor(Qt.darkGreen))
        rename_btn.setPalette(palette)

        cancel_btn = QPushButton('Cancel', self, clicked=self.close)
        cancel_btn.setAutoFillBackground(True)
        palette = cancel_btn.palette()
        palette.setColor(QPalette.Button, QColor(Qt.darkRed))
        cancel_btn.setPalette(palette)
            
        # Layouts

        selected_layout = QHBoxLayout()
        selected_layout.addWidget(selected_label)
        selected_layout.addWidget(self.selected_name_label, Qt.AlignLeft)

        new_name_layout = QHBoxLayout()
        new_name_layout.addWidget(new_name_label)
        new_name_layout.addWidget(self.new_name_le)

        prefix_layout = QVBoxLayout()
        prefix_layout.addWidget(prefix_label)
        prefix_layout.addWidget(prefix_cb)

        suffix_layout = QVBoxLayout()
        suffix_layout.addWidget(suffix_label)
        suffix_layout.addWidget(suffix_cb)

        addons_layout = QHBoxLayout()
        addons_layout.addLayout(prefix_layout)
        addons_layout.addLayout(suffix_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(rename_btn)
        buttons_layout.addWidget(cancel_btn)
            
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(selected_layout)
        main_layout.addLayout(addons_layout)
        main_layout.addLayout(new_name_layout)
        main_layout.addLayout(buttons_layout)
            
        self.setLayout(main_layout)
        self.show()
        
    @Slot()
    def rename_selected(self)->None:
        """
        Applies the current text from the new name field to the selected object. 
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

    @Slot()
    def insert_addon(self)->None:
        """
        Adds to the name a prefix or suffix.
        """
        separator = '_'
        sender = self.sender()
        current = self.new_name_le.text()
        
        if sender.objectName() == 'prefix':
            self.new_name_le.setText(sender.currentText() + separator + current)
        elif sender.objectName()  == 'suffix':
            self.new_name_le.setText(current + separator + sender.currentText())

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
        
    
greeting = Renamer()

