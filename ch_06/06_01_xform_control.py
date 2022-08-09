# 02_01_xfrom_control.py
# GOAL: Display the FBModel.Name from a selected model or prompt the user to select one after searching for them if any is found.
from PySide2.QtWidgets import (QWidget,QLabel, QHBoxLayout, QVBoxLayout, QInputDialog)
from PySide2.QtCore import Qt
from pyfbsdk import FBModelList, FBGetSelectedModels, FBSystem, FBModel
import pythonidelib

lsystem = FBSystem()
lscene = lsystem.Scene

class XformControl(QWidget):
    def __init__(self, parent=None):
        super(XformControl,self).__init__(parent, Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Xform Controls")
        self.setMinimumWidth(256)

        # Layout and slider controls
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self._init_selected())

        self.setLayout(main_layout)
        self.show()

    def get_selected_model(self)->FBModel:
        """
        Returns a FBModel, the first one found in the selection list if there's a current selection active, 
        otherwise promts the user to select one of the available ones if any.
        """
        # If there's current selected model return the first on the list.
        try:
            selected = FBModelList()
            FBGetSelectedModels(selected)

            if not selected:
                raise IndexError('Nothing selected.\nSearching for models...')
            else:
                return selected[0]
        except IndexError as e: 
            print(e)
            pythonidelib.FlushOutput()

            # Find models in the scene and prompt the user to select one if any are found. 
            # If the scene is empty close the widget.
            available_models = lscene.RootModel.Children

            if not available_models:
                print('Nothing found.\nClossing Widget...')
                self.setAttribute(Qt.WA_DeleteOnClose)
                self.close()
                print('Widget closed.')
                pythonidelib.FlushOutput()
            else:
                print('Models found.')
                pythonidelib.FlushOutput()
                model_names = [model.Name for model in available_models]
                select, ok = QInputDialog().getItem(self, 'Model Selection', 'Select a model:', model_names, 0, False, Qt.WindowSystemMenuHint)
                
                if ok and select:
                    for model in available_models:
                        if model.Name == select:
                            model.Selected = True
                            return model

    def _init_selected(self)->QHBoxLayout:
        """
        Initialize the widgets showing the selected model information.
        """
        model = self.get_selected_model()

        # Widgets    
        self.selected_label = QLabel('Selected:', self)
        self.selected_name_label = QLabel(self)
        try:
            if not model:
                raise AttributeError('No model found. Name attribute failed.')
            else:
                self.selected_name_label.setText(model.Name)
        except AttributeError as e:
            print(e)
            pythonidelib.FlushOutput()

        # Layout
        layout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.selected_label)
        layout.addWidget(self.selected_name_label)
        layout.addStretch(1)
        
        return layout
    
xform_ctrl = XformControl()