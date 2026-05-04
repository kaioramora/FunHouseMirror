# gui2.py
# this is the rewritten and simplified gui.py code for the Fun House Mirror Project
# leiani butler 

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QSlider, QLabel, QApplication
)
from PyQt5.QtCore import Qt, QTimer
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# Buttons
# this is all of the buttons that will exist on the tablet screen
# reset, countdown, cartoon filter 

# callback function is passed to call on later 

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy



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

        self.setAttribute(Qt.WA_AcceptTouchEvents, True)


        


        self.setWindowTitle("Funhouse Mirror Controls (Tablet)")
        #self.setFixedSize(400, 500)

        layout = QVBoxLayout()
        layout.setSpacing(20)


        # qr code stuff 
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.qr_label)

        from matplotlib.figure import Figure

        self.figure = Figure(figsize=(4, 6))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_title("Mirror Shape")
        self.ax.set_xlim(-12000, 12000)
        self.ax.invert_yaxis()

        layout.addWidget(self.canvas)


        # sliders 
        self.s1 = self.create_slider()
        self.s2 = self.create_slider()
        self.s3 = self.create_slider()


        self.s1.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.s2.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.s3.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self.s1.setFocusPolicy(Qt.StrongFocus)
        self.s2.setFocusPolicy(Qt.StrongFocus)
        self.s3.setFocusPolicy(Qt.StrongFocus)


        layout.addWidget(self.s1)
        layout.addWidget(self.s2)
        layout.addWidget(self.s3)


        self.s1.setTracking(True)
        self.s2.setTracking(True)
        self.s3.setTracking(True)

        #self.canvas.setAttribute(Qt.WA_TransparentForMouseEvents, True)



        slider_style = """
        QSlider::groove:horizontal {
            height: 30px;
            background: #444;
            border-radius: 15px;
        }

        QSlider::handle:horizontal {
            background: white;
            width: 50px;
            height: 50px;
            margin: -10px 0;
            border-radius: 25px;
        }
        """


        self.s1.setStyleSheet(slider_style)
        self.s2.setStyleSheet(slider_style)
        self.s3.setStyleSheet(slider_style)


        # buttons 
        self.reset_btn = QPushButton("reset")
        self.countdown_btn = QPushButton("countdown")
        self.cartoon_btn = QPushButton("cartoon")



        button_style = """
        QPushButton {
            background-color: #222;
            color: white;
            font-size: 24px;
            border-radius: 25px;
            padding: 20px;
        }

        QPushButton:pressed {
            background-color: #555;
        }
        """

        self.reset_btn.setStyleSheet(button_style)
        self.countdown_btn.setStyleSheet(button_style)
        self.cartoon_btn.setStyleSheet(button_style)









        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.countdown_btn)
        button_layout.addWidget(self.cartoon_btn)

        layout.addLayout(button_layout)

        for btn in [self.reset_btn, self.countdown_btn, self.cartoon_btn]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        """
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.countdown_btn)
        layout.addWidget(self.cartoon_btn)
        """

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

    """
    def create_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(-15000)
        slider.setMaximum(15000)
        slider.setValue(0)
        return slider
    """

    def create_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(-15000)
        slider.setMaximum(15000)
        slider.setValue(0)

        slider.setTracking(True)  

        slider.setAttribute(Qt.WA_AcceptTouchEvents, True)
        slider.setFocusPolicy(Qt.StrongFocus)

        #slider.mousePressEvent = lambda event, s=slider: self.slider_jump(event, s)

        return slider


    """
    def update_qr(self, url):
        # generate QR as PNG bytes
        png_bytes = make_qr(
            url,
            box_size=10,
            border=4,
            ecc="H"
        ).to_png_bytes()

        # convert bytes → QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(png_bytes)

        self.qr_label.setPixmap(
            pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    """


    def slider_jump(self, event, slider):
        if event.button() == Qt.LeftButton:
            pos = event.pos().x()
            width = slider.width()

            value = slider.minimum() + (slider.maximum() - slider.minimum()) * (pos / width)
            slider.setValue(int(value))


    
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

    
    # qr code stuff
    def show_qr(self, pixmap):
        self.qr_label.setPixmap(
            pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )


    


class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Funhouse Mirror Camera")
        # self.setFixedSize(1200,600)

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













