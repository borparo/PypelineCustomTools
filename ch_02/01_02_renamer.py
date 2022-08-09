# 01_02_renamer.py
# GOAL: Add 2 more fields for prefixes and suffixes to use in the new name.
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit
from PySide2.QtCore import Qt, Slot
from pyfbsdk import FBModelList, FBGetSelectedModels, FBModel
import pythonidelib


class Renamer(QWidget):
    
    def __init__(self, parent=None):
        super(Renamer, self).__init__(parent, Qt.WindowStaysOnTopHint)
        
        self.setWindowTitle('Renamer')
        self.setGeometry(200, 200, 216, 92)
        self.setMinimumSize(216, 128)
        
        #Widgets
        selected_label = QLabel('Selected Model:', self)
        selected_label.setGeometry(4, 8, 80, 24)  # Will position the widget in the given coordinates from it's parent.
        
        # Display the name of the seleceted model to rename
        self.selected_name_label = QLabel(self)
        try:
            self.model = self.get_selected_model()
            if not self.model:
                raise AttributeError('WARNING: None has not Name attribute.')
            else:
                self.selected_name_label.setText(self.model.Name)
                self.selected_name_label.setDisabled(True)
        except AttributeError as e:
            print(e)
            pythonidelib.FlushOutput()

        self.selected_name_label.setGeometry(84, 8, 132, 24)

        # Prefixes / Suffixes
        prefix_label = QLabel('Prefix:', self)
        prefix_label.setGeometry(4, 36, 48, 24)

        self.prefix_le = QLineEdit(self)
        self.prefix_le.setToolTip('3 character before the low dash.')
        self.prefix_le.setGeometry(52, 36, 32, 24)
        self.prefix_le.setInputMask('>AAA_')
        self.prefix_le.setCursorPosition(0)
        if self.prefix_le.hasFocus():
            self.prefix_le.setCursorPosition(0)
        

        suffix_label = QLabel('Suffix:', self)
        suffix_label.setGeometry(96, 36, 36, 24)

        self.suffix_le = QLineEdit(self)
        self.suffix_le.setGeometry (136, 36, 56, 24)
        self.suffix_le.setToolTip('Up to 7 characters after the low dash.')
        self.suffix_le.setInputMask('_>nnnnnnn')
        
        if self.suffix_le.hasFocus():
            self.suffix_le.setCursorPosition(1)

        # New Name
        new_name_label = QLabel('New Name:', self)
        new_name_label.setGeometry(4, 64, 208, 24)
        
        self.new_name_le = QLineEdit(self, returnPressed=self.rename_selected) # connects the emited signal to a slot
        self.new_name_le.setPlaceholderText('Type a new name here...')
        self.new_name_le.setGeometry(4, 88, 208, 24)

        self.show()
    
    def get_selected_model(self, index:int = 0)->FBModel:
        """
        Returns the selected model at x position from the current active selection list. Defaults to 0 (first model in list).
        """
        try:
            self.current_selection = FBModelList()
            FBGetSelectedModels(self.current_selection)
            for i, model in enumerate(self.current_selection):
                print(f'[{i}]', model.Name)
                pythonidelib.FlushOutput()
            
            if not self.current_selection:
                raise IndexError('WARNING: Nothing selected. Please select 1 model and run the script again.')
            else:
                return self.current_selection[index]
        except IndexError as e:
            print(e)
            pythonidelib.FlushOutput()
            
    @Slot()    
    def rename_selected(self):
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
        