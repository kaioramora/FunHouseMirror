"""
# file: cv_height_detection.py 
# author: Leiani Butler

# this file is an opencv version of the previous mediapipe height detection code
# There were dependency issues with mediapipe and raspberry pi so decided to just fully switch to opencv


import cv2 
import numpy as np


class HeightDetector: 
    def __init__(self):

        """
         - opencv has its own background subtration technique that I'm using here
         - This is using the MOG2 algorthim, which works better for varying lighting and shadows (basically more accurate then MOG ver 1)
        """
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    def get_height_pixels(self, frame): 
        # applying the the opencv backgorund subtraction
        fg_mask = self.bg_subtractor.apply(frame)

        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)


        """
         - opencv has this thing called morphorlogical operations which are image processing techniques that help process images based on chape
         - the specific operation I use is Closing with cv2.MORPH_CLOSE
         - Closing does dialation then erosion which fills in small gaps in foreground object but still keeps the same shape + size
            - dialation = expanding white foreground shapes
            - erosion = shrinking the white foreground shapes
         - Use: it helps get rid of noise in the image
        """
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        """
         - Once again, using an opencv function using called findContours
         - This function applies a threshold 
        """

        # finding countors 

        """
        - cv2.CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments and just leaves their end points.
        - ex. a rectanlge is encoded with 4 points. 
        - cv2.RETR_EXTERNAL only retrieves the extreme outer contours
        """

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours: 
            return None

        
        # getting the largest contour (assuming this is a person)
        largest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest)

        # drawing a bounding box (kind of like the landmarks from the previous height detection using mediapipe)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # height of the person in pixels = height of bounding box 
        height_pixels = h

        return height_pixels


"""
