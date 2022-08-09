# 01_01_renamer.py
# GOAL: Create a Widget with a field to rename a selected FBModel.
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit
from PySide2.QtCore import Qt, Slot
from pyfbsdk import FBModelList, FBGetSelectedModels, FBModel
import pythonidelib


class Renamer(QWidget):
    
    def __init__(self, parent=None):
        super(Renamer, self).__init__(parent, Qt.WindowStaysOnTopHint)
        
        self.setWindowTitle('Renamer')
        self.setGeometry(200, 200, 216, 92)
        self.setMinimumSize(216, 92)
        
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
        
        # New Name
        new_name_label = QLabel('New Name:', self)
        new_name_label.setGeometry(4, 36, 208, 24)
        
        self.new_name_le = QLineEdit(self, returnPressed=self.rename_selected) # connects the emited signal to a slot
        self.new_name_le.setInputMask('')
        self.new_name_le.setPlaceholderText('Type a new name here...')
        self.new_name_le.setGeometry(4, 64, 208, 24)
        
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
                self.model.Name = str(self.new_name_le.text())
                self.selected_name_label.setText(self.new_name_le.text())
                self.new_name_le.clear()
        except ValueError as e:
            print(e)
            pythonidelib.FlushOutput()
        
    
window = Renamer()
        