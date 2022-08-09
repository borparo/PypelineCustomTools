from email.charset import QP
from PySide2.QtWidgets import QApplication, QWidget, QLabel
from PySide2.QtGui import (QPainter, QPaintEvent, QColor, QConicalGradient, QPainterPath,
                            QLinearGradient, QRadialGradient, QPen, QRegion)
from PySide2.QtCore import Qt, QPointF, Slot
import sys


class ColorWheel(QWidget):
    def __init__(self, parent=None):
        super(ColorWheel,self).__init__()
        self.setFixedSize(256, 256)

        self.show()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.translate(self.width() / 2, self.height() / 2 )
        painter.setRenderHint(QPainter.Antialiasing)

        wheel_gradient = QConicalGradient(0, 0, 0)
        wheel_gradient.setColorAt(0.0, QColor('#f00'))
        wheel_gradient.setColorAt(0.15, QColor('#ff0'))
        wheel_gradient.setColorAt(0.3, QColor('#0f0'))
        wheel_gradient.setColorAt(0.45, QColor('#0ff'))
        wheel_gradient.setColorAt(0.6, QColor('#00f'))
        wheel_gradient.setColorAt(0.75, QColor('#f0f'))
        wheel_gradient.setColorAt(0.999, QColor('#f00'))

        lum_gradient  = QLinearGradient(-(self.width() * 0.5) * 0.5, -(self.height() * 0.5)* 0.5, -(self.width() * 0.5) * 0.5, self.height() * 0.5)
        lum_gradient.setColorAt(0.01, QColor(255, 255, 255))
        lum_gradient.setColorAt(0.7, QColor(0, 0, 0))

        value_gradient = QRadialGradient((-self.width() * 0.5) * 0.5, 0, 128)
        value_gradient.setColorAt(0.1, QColor(255, 0, 0, 255))
        value_gradient.setColorAt(0.8, QColor(255, 0, 0, 0))

        ring = QPainterPath()
        ring.addEllipse(-self.width() * 0.5, -self.height() * 0.5 , self.width(), self.height())
        ring.addEllipse(-(self.width() * 0.8) * 0.5, -(self.height() * 0.8)* 0.5, self.width() * 0.8, self.height() * 0.8)
        
        painter.setBrush(wheel_gradient)
        painter.drawPath(ring)

        painter.setBrush(lum_gradient)
        painter.drawRect(-(self.width() * 0.5) * 0.5, -(self.height() * 0.5)* 0.5, self.width() * 0.5, self.height() * 0.5)

        painter.translate(QPointF(self.width() * 0.5, 0))
        painter.setBrush(value_gradient)
        painter.setPen(QColor(0,0,0,0))
        painter.drawEllipse(-self.width()* 0.5, -(self.height() * 0.5)* 0.5, 128, 128)
        painter.setClipRegion(QRegion(-(self.width() * 0.5) * 0.5, -(self.height() * 0.5)* 0.5, self.width() * 0.5, self.height() * 0.5))

        painter.end()


app = QApplication(sys.argv)
wheel = ColorWheel()
sys.exit(app.exec_()) 