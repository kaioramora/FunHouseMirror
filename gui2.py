# gui2.py
# this is the rewritten and simplified main.py code for the Fun House Mirror Project
# leiani butler 

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QSlider, QLabel, QApplication
)
from PyQt5.QtCore import Qt, QTimer
import sys

# Buttons
# this is all of the buttons that will exist on the tablet screen
# reset, countdown, cartoon filter 

# callback function is passed to call on later 


class TabletGUI(QWidget):
    def __init__(self, 
                 slider_callback=None, 
                 reset_callback=None,
                 countdown_callback=None,
                 cartoon_callback=None):
        super().__init__()

        self.slider_callback = slider_callback
        self.reset_callback = reset_callback
        self.countdown_callback = countdown_callback
        self.cartoon_callback = cartoon_callback


        self.setWindowTitle("Funhouse Mirror Controls (Tablet)")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()
        layout.setSpacing(20)




        # sliders 
        self.s1 = self.create_slider()
        self.s2 = self.create_slider()
        self.s3 = self.create_slider()

        layout.addWidget(self.s1)
        layout.addWidget(self.s2)
        layout.addWidget(self.s3)

        slider_style = ("""
                QSlider::groove:horizontal {
                    height: 14px;
                    background: #666;
                    border-radius: 7px;
                }
                QSlider::handle:horizontal {
                    background: white;
                    width: 30px;
                    border-radius: 7px;
                    margin: -7px 0;
                    border -radius: 15px;
                }
                """)

        self.s1.setStyleSheet(slider_style)
        self.s2.setStyleSheet(slider_style)
        self.s3.setStyleSheet(slider_style)


        # buttons 
        self.reset_btn = QPushButton("reset")
        self.countdown_btn = QPushButton("countdown")
        self.cartoon_btn = QPushButton("cartoon")


        layout.addWidget(self.reset_btn)
        layout.addWidget(self.countdown_btn)
        layout.addWidget(self.cartoon_btn)

        self.setLayout(layout)



        # countdown label
        self.countdown_label = QLabel(" ")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 32px; color: red;")
        layout.addWidget(self.countdown_label)






        # connecting all the buttons
        self.s1.valueChanged.connect(self.emit_slider_values)
        self.s2.valueChanged.connect(self.emit_slider_values)
        self.s3.valueChanged.connect(self.emit_slider_values)

        if self.reset_callback:
            self.reset_btn.clicked.connect(self.handle_reset)

        
        if self.countdown_callback:
            self.countdown_btn.clicked.connect(self.countdown_callback)


        if self.cartoon_callback:
            self.cartoon_btn.clicked.connect(self.cartoon_callback)

        
    def create_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(-15000)
        slider.setMaximum(15000)
        slider.setValue(0)
        return slider
    
    def emit_slider_values(self):
        if self.slider_callback:
            self.slider_callback(
                self.s1.value(),
                self.s2.value(),
                self.s3.value()
            )

    def handle_reset(self):
        self.s1.setValue(0)
        self.s2.setValue(0)
        self.s3.setValue(0)

        if self.reset_callback:
            self.reset_callback()


class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Funhouse Mirror Camera")
        self.setFixedSize(1200,600)

        layout = QVBoxLayout()

        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("background-color: black;")
        layout.addWidget(self.camera_label)

        self.setLayout(layout)




# for running the gui by iteself

if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = TabletGUI()
    panel.show()
    sys.exit(app.exec_())













