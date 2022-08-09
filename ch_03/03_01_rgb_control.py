# 02_01_rgb_control.py
# GOAL: Createa a RGB slider control.
from PySide2.QtWidgets import (QApplication, QWidget, QGroupBox, QLabel, QSpinBox, QComboBox,
                                QSlider, QHBoxLayout, QVBoxLayout, QStackedLayout)
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QColor, QPalette
import sys


class ColorControl(QWidget):
    """
    Set of label, sliders and spinbox widgets to manipulate RGB values
    """
    def __init__(self, parent=None):
        super(ColorControl,self).__init__(parent, Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Color")
        self.setMinimumWidth(256)

        # Widgets
        self.color = QLabel()
        self.color.setMinimumHeight(96)

        self.p = QPalette()
        self.p.setColor(QPalette.Window, Qt.black)
        self.color.setAutoFillBackground(True)
        self.color.setPalette(self.p)
        self.color.update()
        
        # Layout and slider controls
        rgb_page = self._init_same_range_slider_grp('RGB:', ['R', 'G', 'B'], 0, 255)

        self._hue_slider = self._init_slider('H', 0, 359,)
        self._saturation_slider = self._init_slider('S', 0, 255)
        self._value_slider = self._init_slider('V', 0, 255)

        hsv_page = QGroupBox('HSV', self) 
        hsv_page.setObjectName('HSV')

        hsv_layout = QVBoxLayout()
        hsv_layout.addLayout(self._hue_slider)
        hsv_layout.addLayout(self._saturation_slider)
        hsv_layout.addLayout(self._value_slider)

        hsv_page.setLayout(hsv_layout)

        color_layout = QStackedLayout()
        color_layout.addWidget(rgb_page)
        color_layout.addWidget(hsv_page)

        self.color_cb = QComboBox()
        self.color_cb.addItem("RGB")
        self.color_cb.addItem("HSV")
        self.color_cb.activated.connect(color_layout.setCurrentIndex)  # changes the color_layout displayed page o r widget
        self.color_cb.activated.connect(lambda: self.update_slider_values(self.p.color(QPalette.Window)))  # updates the sliders values depending on the current color 

        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.color)
        main_layout.addWidget(self.color_cb)
        main_layout.addLayout(color_layout)

        self.setLayout(main_layout)
        self.show()

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
        self._control_label = QLabel(label)

        self._control_slider = QSlider(orientation=Qt.Horizontal)
        self._control_slider.setRange(range_min, range_max)
        self._control_slider.setSingleStep(step/range_max)
        self._control_slider.setTickInterval(range_max / interval)
        self._control_slider.setTickPosition(QSlider.TicksAbove)
        self._control_slider.setObjectName(self._control_label.text())
        
        self._control_spinbox = QSpinBox()
        self._control_spinbox.setObjectName(self._control_label.text().lower())
        self._control_spinbox.setRange(range_min,range_max)
        self._control_spinbox.setSingleStep(step)

        # Connections
        self._control_slider.sliderMoved.connect(self._control_spinbox.setValue)
        self._control_slider.sliderMoved.connect(self.update_color)
        self._control_spinbox.valueChanged.connect(self._control_slider.setValue)
        self._control_spinbox.valueChanged.connect(self.update_color)

        # Layout
        group_layout = QHBoxLayout()

        self._control_label.setParent(group_layout)
        self._control_slider.setParent(group_layout)
        self._control_spinbox.setParent(group_layout)

        group_layout.addWidget(self._control_label)
        group_layout.addWidget(self._control_slider)
        group_layout.addWidget(self._control_spinbox)

        return group_layout

    def _init_same_range_slider_grp(self, grp_label:str, sliders_list:list=['X', 'Y', 'Z'], range_min  = 0, range_max = 100) -> QGroupBox:
        """
        Initialize a set of n sliders with the same range per group. Returns the group box containing all the needed sliders.
        @param grp_label: Label that will appear on top of the group frame.
        @param grp_items_label: List of labels used to create the total amount of sliders. Defaults to 3: 'X', 'Y', and 'Z'.
        """
        # Widgets
        self._control_group_box = QGroupBox(grp_label, self)  # Creates a frame with at itle around all the widgets contained in the group.
        self._control_group_box.setObjectName(grp_label)

        # Layout
        control_layout = QVBoxLayout()

        for label in sliders_list:
            control_layout.addLayout(self._init_slider(label, range_min, range_max))

        self._control_group_box.setLayout(control_layout)

        return self._control_group_box

    @Slot()
    def update_color(self):
        sender = self.sender() # can be slider or spinbox

        current_color = self.p.color(QPalette.Window).getRgb()
        new_color = QColor(*current_color)

        if self.color_cb.currentIndex() == 0:  # RGB
            if sender.objectName() == 'R' or sender.objectName() == 'r':
                new_color.setRed(sender.value())
            elif sender.objectName() == 'G' or sender.objectName() == 'g':
                new_color.setGreen(sender.value())
            elif sender.objectName() == 'B' or sender.objectName() == 'b':
                new_color.setBlue(sender.value())
        elif self.color_cb.currentIndex() == 1: # HSL
            hue = self.findChild(QSlider, 'H').value() or self.findChild(QSpinBox, 'h').value()
            saturation = self.findChild(QSlider, 'S').value() or self.findChild(QSpinBox, 's').value()
            value = self.findChild(QSlider, 'V').value() or self.findChild(QSpinBox, 'v').value()
            
            new_color.setHsv(hue, saturation, value)
        
        if new_color.isValid():
            self.p.setColor(QPalette.Window, new_color)
            self.color.setAutoFillBackground(True)
            self.color.setPalette(self.p)
            self.color.update()

    @Slot()
    def update_slider_values(self, color=QColor):
        """
        Matches widgets color values to color parameter
        @param color: QColor to match color component values from.
        """
        if self.color_cb.currentIndex() == 0:  # RGB
            r_slider = self.findChild(QSlider, 'R')
            r_spin_box = self.findChild(QSpinBox, 'r')
            r_slider.setValue(color.red())
            r_spin_box.setValue(color.red())

            g_slider = self.findChild(QSlider, 'G')
            g_spin_box = self.findChild(QSpinBox, 'g')
            g_slider.setValue(color.green())
            g_spin_box.setValue(color.green())

            b_slider = self.findChild(QSlider, 'B')
            b_spin_box = self.findChild(QSpinBox, 'b')
            b_slider.setValue(color.blue())
            b_spin_box.setValue(color.blue())
        elif self.color_cb.currentIndex() == 1:  # HSV
            h_slider = self.findChild(QSlider, 'H')
            h_spin_box = self.findChild(QSpinBox, 'h')
            h_slider.setValue(color.hue())
            h_spin_box.setValue(color.hue())

            s_slider = self.findChild(QSlider, 'S')
            s_spin_box = self.findChild(QSpinBox, 's')
            s_slider.setValue(color.saturation())
            s_spin_box.setValue(color.saturation())

            v_slider = self.findChild(QSlider, 'V')
            v_spin_box = self.findChild(QSpinBox, 'v')
            v_slider.setValue(color.value())
            v_spin_box.setValue(color.value())

    
app = QApplication(sys.argv)
xform_ctrl = ColorControl()
sys.exit(app.exec_())