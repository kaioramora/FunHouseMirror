"""

main2.py 

Main file for the Funhouse Mirror Project

This file: 
- initializes the camera
- initializes the GUI windows 
- applies the mirror distortion 
- applies the cartoon filter
- uses MediaPipe pose detection to scale the distortion
- handles the countdown + image saving 
- displays a Matplotlib mirror shape plot 

"""



import os 

# This is for fixing some Qt plugin errors due to Linux
os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH", None)
os.environ.pop("QT_QPA_FONTDIR", None)


# libraries
import sys
import numpy as np
import time
import cv2
import datetime 
import matplotlib.pyplot as plt 

# all of the PyQt GUI 
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

# project files
import processing2
import gui2
import camera2
from height_detection import HeightDetector

# creating directory for saved images
os.makedirs("saved_images", exist_ok=True)


class AppController:
    """
    Main controller class, connects:
    - camera
    - GUI
    - processing
    - height scaling
    """


    def __init__(self):

        # camera setup
        self.camera = camera2.Camera(0)
        print("Camera initialized")     # check to make sure this prints
        self.slider_values = [0,0,0]    # 3 mirror distortion points
        self.filter_mode = 'mirror'     # "mirror" or "cartoon"
        self.latest_frame = None        # stores the most recent camera frame


        # mediapipe height detection
        self.height_detector = HeightDetector()
        self.base_height = None         # reference height
        self.height_scale = 1.0         # scaling multiplier



        # gui setup
        self.app = QApplication(sys.argv)
        self.gui = gui2.TabletGUI(
            slider_callback=self.set_shape,
            reset_callback=self.reset_all,
            countdown_callback=self.on_countdown,
            cartoon_callback=self.toggle_cartoon
        )
        self.gui.show()

        # camera window 
        self.camera_window = gui2.CameraWindow()
        self.camera_window.show()

        # frame timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(0)

        # mirror plot timer 
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(200)

        # mirror shape plot
        self.fig, self.ax = plt.subplots(figsize=(4,10))
        self.line, = self.ax.plot([], [], 'r-')
        self.ax.set_title("Mirror Shape")
        self.ax.set_xlim(-12000, 12000)
        self.ax.invert_yaxis()
        plt.ion()
        plt.show()


        # countdown
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self._countdown_step)
        self.countdown_value = 0



    # GUI callbacks
    #   - functions connected to signals (signal & slot method)

    def set_shape(self, s1, s2, s3):
        # recieves slider values from GUI
        self.slider_values = [s1,s2,s3]

    def reset_all(self):
        # resets sliders and filter mode
        self.slider_values = [0,0,0]
        self.filter_mode = "mirror"
        print("Sliders and mode reset")

    def toggle_cartoon(self):
        # toggles between mirror and cartoon modes
        self.filter_mode = "cartoon" if self.filter_mode == "mirror" else "mirror"
        print("Filter mode: ", self.filter_mode)



    # countdown logic
    def on_countdown(self):
        # starts 3 sec countdown
        self.countdown_value = 3
        print("Starting countdown...")
        self.countdown_timer.start(1000)

    def _countdown_step(self):
            # countdown step each sec
        if self.countdown_value > 0:
            print(self.countdown_value)
            self.countdown_value -= 1
        else:
            self.countdown_timer.stop()
            self.gui.countdown_label.setText(" ")
            print("Saving picture!")
            self.save_picture()



    # frame logic
    def process_frame(self, frame):
        return processing2.apply_filter(
            frame,
            slider_values=self.slider_values,
            mode=self.filter_mode
        )
    
    def update_frame(self):
        # grabs frame, applies distortion + updates GUI
        frame, fps = self.camera.get_frame()

        if frame is None:
            return
        
        self.latest_frame = frame

        # height scaling logic
        height = self.height_detector.get_height_pixels(frame)

        if height:
            if self.base_height is None: 
                self.base_height = height 

            self.height_scale = height / self.base_height


        scaled_sliders = [int(v * self.height_scale) for v in self.slider_values]
        processed = processing2.apply_filter(
            frame,
            slider_values=scaled_sliders,
            mode=self.filter_mode
        )
        


        # countdown overlay 
        if self.countdown_value > 0:
            cv2.putText(
                processed,
                str(self.countdown_value),
                (processed.shape[1]//2 - 50, processed.shape[0]//2),
                cv2.FONT_HERSHEY_SIMPLEX,
                5,
                (0,0,255),
                10,
                cv2.LINE_AA
            )

        # converting to Qt image
        rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb.shape 
        bytes_per_line = ch * w

        qimg = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        # this should be scaling the pixmap correctly
        pix = QPixmap.fromImage(qimg)
        pix = pix.scaled(
            self.camera_window.camera_label.width(),
            self.camera_window.camera_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.camera_window.camera_label.setPixmap(pix)



    # mirror shape plot 
    def update_plot(self):
        # updates mirror shape plot
        if self.latest_frame is None:
            return

        
        mirror = processing2.calculate_shape(
            self.slider_values,
            length=self.latest_frame.shape[0]
        )

        y = np.arange(len(mirror))
        self.line.set_data(mirror, y)

        self.ax.set_ylim(0, self.latest_frame.shape[0])
        self.ax.set_xlim(-12000, 12000)
        self.ax.invert_yaxis()

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()


    # save image 
    def save_picture(self):
        # saves processed frame to disk
        if  self.latest_frame is None:
            print("No frame to save")
            return
        
        processed = self.process_frame(self.latest_frame)
        if processed is None or processed.size == 0:
            print("Processed frame is empty!")
            return


        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"saved_images/capture_{ts}.png"

        cv2.imwrite(filename, processed)
        print("Saved:", filename)


    def quit(self):
        self.timer.stop()
        self.camera.release()
        self.app.quit()

    def run(self):
        sys.exit(self .app.exec_())


    
if __name__ == "__main__":
    controller = AppController()
    controller.run()