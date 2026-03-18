# camera2.py


import cv2
from threading import Thread
import numpy as np
import time

class Camera:
    def __init__(self, camera_index=2):
        self.cam = cv2.VideoCapture(camera_index)
        self.fps = 30
        self.frame = np.zeros([100,100,3], dtype=np.uint8)
        self.frame_count = 0
        self.last_time = time.time()

        if not self.cam.isOpened():
            raise Exception("Could not open video device")
        else:
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon = True
            self.thread.start()

    def update(self):
        while True:
            _, frame_hold = self.cam.read()
            #frame_hold = cv2.rotate(frame_hold, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.frame = cv2.flip(frame_hold, 1)
            self.frame_count += 1
            now = time.time()
            if now - self.last_time >= 1.0:
                self.fps = self.frame_count
                self.frame_count = 0
                self.last_time = now

    def get_frame(self):
        return self.frame, self.fps

    def release(self):
        """Safely releases the camera."""
        if self.cam.isOpened():
            self.cam.release()

        



        


 # testing camera.py on its own 

if __name__ == "__main__":
    cam = Camera(camera_index=0)
    
    try:
        while True:
            frame, fps = cam.get_frame()

            

            cv2.imshow("Camera Test", frame)
 
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                print("ESC Key pressed. Closing camera....")
                break

            if key == ord('q'):
                print("Q Key pressed. Closing camera....")
                break

    except KeyboardInterrupt:
        pass

    cam.release()
    cv2.destroyAllWindows()


