# 01_03_renamer.py
# GOAL: Create layouts to control the widgets position and their arrangement.
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide2.QtCore import Qt, Slot
from pyfbsdk import FBModelList, FBGetSelectedModels, FBModel
import pythonidelib


class Renamer(QWidget):
    
    def __init__(self, parent=None):
        super(Renamer, self).__init__(parent, Qt.WindowStaysOnTopHint)
        
        self.setWindowTitle('Renamer')
        self.setMinimumSize(200, 92)
        
        # Widgets
        selected_label = QLabel('Selected Model:', self)
        
        try:
            self.model = self.get_selected_model(0)
            self.selected_name_label = QLabel(self)
            if not self.model:
                raise AttributeError('WARNING: Nothing Selected. None has not Name attribute.')
            else:
                self.selected_name_label.setText(self.model.Name)
            self.selected_name_label.setEnabled(False)
        except AttributeError as e:
            print(e)
            pythonidelib.FlushOutput()

        # Prefixes / Suffixes
        prefix_label = QLabel('Prefix:', self)

        self.prefix_le = QLineEdit(self)
        self.prefix_le.setToolTip('3 character before the low dash.')
        self.prefix_le.setInputMask('>AAA_')
        self.prefix_le.setCursorPosition(0)
        if self.prefix_le.hasFocus():
            self.prefix_le.setCursorPosition(0)
        
        suffix_label = QLabel('Suffix:', self)

        self.suffix_le = QLineEdit(self)
        self.suffix_le.setToolTip('Up to 7 characters after the low dash.')
        self.suffix_le.setInputMask('_>nnnnnnn')
        
        if self.suffix_le.hasFocus():
            self.suffix_le.setCursorPosition(1)

        # New name    
        new_name_label = QLabel('New Name:', self)

        self.new_name_le = QLineEdit(self, returnPressed=self.rename_selected)
        self.new_name_le.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        
        # Layouts
        selected_layout = QHBoxLayout()
        selected_layout.addWidget(selected_label)
        selected_layout.addWidget(self.selected_name_label, Qt.AlignLeft)

        addons_layout = QHBoxLayout()
        addons_layout.addWidget(prefix_label)
        addons_layout.addWidget(self.prefix_le)
        addons_layout.addWidget(suffix_label)
        addons_layout.addWidget(self.suffix_le)

        new_name_layout = QHBoxLayout()
        new_name_layout.addWidget(new_name_label)
        new_name_layout.addWidget(self.new_name_le)
        
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(selected_layout)
        main_layout.addLayout(addons_layout)
        main_layout.addLayout(new_name_layout)
        
        self.setLayout(main_layout)
        self.show()
    
    def get_selected_model(self, index)->FBModel:
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
        Renames the selected FBModel and clears the field.
        """
        try:
            if not self.new_name_le.text():
                raise ValueError("ERROR: Field is empty. Please type a new name.")
            else:
                # Check if prefix and suffix have text
                if self.prefix_le.text() == '_':
                    self.prefix_le.setInputMask('')
                if self.suffix_le.text() == '_':
                    self.suffix_le.setInputMask('')
                # rename
                self.model.Name = str(self.prefix_le.text() + self.new_name_le.text() + self.suffix_le.text())
                self.selected_name_label.setText(self.prefix_le.text() + self.new_name_le.text() + self.suffix_le.text())
                self.new_name_le.clear()
                self.prefix_le.setInputMask('>aaa_')
                self.suffix_le.setInputMask('_>nnnnnnn')
        except ValueError as e:
            print(e)
            pythonidelib.FlushOutput()
    

window = Renamer()
        