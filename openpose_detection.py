# height_detection.py

import cv2
import numpy as np
from openpose import pyopenpose as op


class HeightDetector:
    def __init__(self):
        params = {
            "model_folder": "./models/",
            "face": False,
            "hand": False
        }

        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

        # keypoints
        self.NOSE = 0
        self.NECK = 1
        self.R_HIP = 8
        self.L_HIP = 11

    def get_height_pixels(self, frame):
        datum = op.Datum()
        datum.cvInputData = frame
        self.opWrapper.emplaceAndPop([datum])

        keypoints = datum.poseKeypoints

        if keypoints is None or len(keypoints.shape) < 2:
            return None

        person = keypoints[0]

        def get_point(i):
            x, y, c = person[i]
            if c < 0.1:
                return None
            return np.array([x, y])

        nose = get_point(self.NOSE)
        neck = get_point(self.NECK)
        r_hip = get_point(self.R_HIP)
        l_hip = get_point(self.L_HIP)

        if neck is None or r_hip is None or l_hip is None:
            return None

        hip = (r_hip + l_hip) / 2
        head_top = nose if nose is not None else neck

        torso = np.linalg.norm(head_top - hip)
        leg = torso * 1.25

        return torso + leg