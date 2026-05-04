import cv2
import numpy as np

class HeightDetector:
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(
            cv2.HOGDescriptor_getDefaultPeopleDetector()
        )

    def get_height_pixels(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        boxes, _ = self.hog.detectMultiScale(
            gray,
            winStride=(8,8),
            padding=(8,8),
            scale=1.05
        )

        if len(boxes) == 0:
            return None

        # choose largest detected person
        x, y, w, h = max(boxes, key=lambda b: b[2]*b[3])

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        return h