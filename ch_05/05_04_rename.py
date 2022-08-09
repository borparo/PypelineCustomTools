# 05_04_renamer.py
# GOAL: Decouple addons from code. Use new data in JSON to set them up as prefix or suffix.
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPalette, QColor
from pyfbsdk import FBModelList, FBGetSelectedModels, FBModel
import pythonidelib
import json


class Renamer(QWidget):
    
    def __init__(self, parent=None):
        super(Renamer, self).__init__(parent, Qt.WindowStaysOnTopHint)
        
        self.setWindowTitle('Renamer')
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(300)
        
        addons_file = r"E:\01_PROJECTS\05_PYTHON\CustomPypelineTools\ch_01\json\comics.json"
        
        # Widgets
        self.addons = self.load_addons(addons_file)  # python dict storing all the json keys and values
        self.addons_labels = []
        self.addons_cb = []
        
        # Using the keys and values from the just created dict, create labels for each key and combobox for
        # the values of each key found in the dict. We will give them an object name we can use later when 
        # adding  prefixes or suffixes before or after any text typed in the new name field.  
        for key, values in  self.addons.items():
            label = QLabel(key.capitalize() + ':')
            label.setObjectName(key)
            self.addons_labels.append(label)
            
            combo_box = QComboBox()
            combo_box.addItems(values['entries'])
            combo_box.setObjectName(key)
            combo_box.activated.connect(self.insert_addon)
            self.addons_cb.append(combo_box)
        
        selected_name_label = QLabel('Selected Model:', self)
        try:
            self.model = self.get_selected_model(0)
            self.selected_label = QLabel(self)
            if not self.model:
                raise AttributeError('WARNING: Nothing Selected. None has not Name attribute.')
            else:
                self.selected_label.setText(self.model.Name)
            self.selected_label.setEnabled(False)
        except AttributeError as e:
            print(e)
            pythonidelib.FlushOutput()
        
        new_name_label = QLabel('New Name:', self)
        self.new_name_le = QLineEdit(self, returnPressed=self.rename_selected)
        
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
        selected_layout.addWidget(selected_name_label)
        selected_layout.addWidget(self.selected_label, Qt.AlignLeft)
        
        addons_layout = QHBoxLayout()
        
        for label, cb in zip(self.addons_labels, self.addons_cb):
            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(cb)
            
            addons_layout.addLayout(layout)
        
        new_name_layout = QHBoxLayout()
        new_name_layout.addWidget(new_name_label)
        new_name_layout.addWidget(self.new_name_le)

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
    
    def get_selected_model(self, index:int)->FBModel:
        """
        Return the FBModel from the current active selection list at the given index position
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
            
    def load_addons(self, json_file:str)->dict:
        """
        Returns a dict with keys and values loaded from a json_file
        """
        try:
            with open(json_file, 'r') as f:
                addons_dict = json.load(f)
                for value in addons_dict.values():
                    value['entries'].sort()
            return addons_dict
        except FileNotFoundError as e:
            print(e)
            pythonidelib.FlushOutput()

    @Slot()
    def insert_addon(self)->None:
        """
        Inserts the current text of the combo box into the name, 
        cheking the key['is_prefix'] value from self.addons,
        to make it a prefix or suffix.
        """
        sender = self.sender()
        separator = '_'
        current = self.new_name_le.text()
        
        # insert prefix or suffix.
        if self.addons[sender.objectName()]['is_prefix']:
            self.new_name_le.setText(sender.currentText() + separator + current)
        else:
            self.new_name_le.setText(current + separator + sender.currentText())
    
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
    

window = Renamer()
        