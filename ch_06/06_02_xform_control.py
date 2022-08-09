# 02_02_xfrom_control.py
# GOAL: Create a set of sliders with spinboxes used to manipulate the selected object xform values.
from PySide2.QtWidgets import (QWidget, QGroupBox, QLabel, QCheckBox, QDoubleSpinBox,
                                QSlider, QHBoxLayout, QVBoxLayout, QInputDialog)
from PySide2.QtCore import Qt
from pyfbsdk import FBModelList, FBGetSelectedModels, FBSystem, FBModel
import pythonidelib

lsystem = FBSystem()
lscene = lsystem.Scene

class XformControl(QWidget):
    """
    Set of label, sliders and spinbox widgets to manipulate a FBModel Translation, Rotation and Scale values
    """
    def __init__(self, parent=None):
        super(XformControl,self).__init__(parent, Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Xform Controls")
        self.setMinimumWidth(256)

        # Layout and slider controls
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self._init_selected())
        main_layout.addWidget(self._init_slider_grp('Translate'))
        main_layout.addWidget(self._init_slider_grp('Rotate'))
        main_layout.addWidget(self._init_slider_grp('Scaling'))

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
        Initialize the widgets showing the selected model information
        """
        model = self.get_selected_model()
            
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
        
        layout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.selected_label)
        layout.addWidget(self.selected_name_label)
        layout.addStretch(1)
        
        return layout
    
    def _init_slider(self, label:str, range_min:int=0, range_max:int=100, step:int=1, interval:int=4)->QHBoxLayout:
        """
        Initialize all the required widgets of the slider control.
        Returns the layout containing the arranged widgets.
        @param label: Label for the slider.
        @param range_min: minimum value available for the slider and spinbox. Defaults to 0
        @param range_max: maximum value available for the slider and spinbox. Defaults to 100
        @param step: increment in the slider and spinbox when using the keyboard. Defaults to  1
        @param interval: number ob Ticks segments available for the slider. Defaults to 4
        """
        # Widgets
        self._control_label = QLabel(label, self)

        self._control_slider = QSlider(self, orientation=Qt.Horizontal)
        self._control_slider.setRange(range_min, range_max)
        self._control_slider.setSingleStep(step/range_max)
        self._control_slider.setTickInterval(range_max / interval)
        self._control_slider.setTickPosition(QSlider.TicksAbove)
        
        self._control_spinbox = QDoubleSpinBox(self)
        self._control_spinbox.setRange(range_min,range_max)
        self._control_spinbox.setSingleStep(step / range_max)

        # Connections
        self._control_slider.sliderMoved.connect(self._control_spinbox.setValue)
        self._control_spinbox.valueChanged.connect(self._control_slider.setValue)

        # Layout
        group_layout = QHBoxLayout(self)
        group_layout.addWidget(self._control_label)
        group_layout.addWidget(self._control_slider)
        group_layout.addWidget(self._control_spinbox)

        return group_layout

    def _init_slider_grp(self, grp_label: str, grp_items_labels:list=['X', 'Y', 'Z'])->QGroupBox:
        """
        Initialize a set of n sliders per group. Returns the group box containing all the needed sliders.
        @param grp_label: Label that will appear on top of the group frame.
        @param grp_items_label: List of labels used to create the total amount of sliders. Defaults to 3: 'X', 'Y', and 'Z'.
        """
        # Widgets
        self._control_group_box = QGroupBox(grp_label, self)  # Creates a frame with at itle around all the widgets contained in the group.
        self._control_group_box.setObjectName(grp_label)

        # Layout
        control_layout = QVBoxLayout(self)

        for label in grp_items_labels:
            control_layout.addLayout(self._init_slider(label, -100, 100))

        self._control_group_box.setLayout(control_layout)

        return self._control_group_box

xform_ctrl = XformControl()