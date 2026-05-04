# height_detection.py

import cv2
import numpy as np


class HeightDetector:

    def __init__(self):

        self.proto = "models/pose_deploy_linevec.prototxt"
        self.weights = "models/pose_iter_160000.caffemodel"

        print("Loading pose model...")
        self.net = cv2.dnn.readNetFromCaffe(self.proto, self.weights)
        print("Pose model loaded")

        self.input_width = 256
        self.input_height = 256

        self.threshold = 0.2

        self.HEAD = 0
        self.R_ANKLE = 10
        self.L_ANKLE = 13

        self.POSE_PAIRS = [
            (0, 1),
            (1, 2), (2, 3),
            (1, 5), (5, 6), (6, 7),
            (1, 8), (8, 9), (9, 10),
            (1, 11), (11, 12), (12, 13)
        ]

    def get_height_pixels(self, frame):

        frame_h, frame_w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            frame,
            scalefactor=1.0 / 255,
            size=(self.input_width, self.input_height),
            mean=(0, 0, 0),
            swapRB=False,
            crop=False
        )

        self.net.setInput(blob)
        output = self.net.forward()

        H = output.shape[2]
        W = output.shape[3]

        points = []

        
        # landmark detection
        for i in range(15):

            prob_map = output[0, i, :, :]
            _, prob, _, point = cv2.minMaxLoc(prob_map)

            x = int(frame_w * point[0] / W)
            y = int(frame_h * point[1] / H)

            if prob > self.threshold:
                points.append((x, y))

                # drawing landmark
                cv2.circle(frame, (x, y), 5, (0, 255, 255), -1)
            else:
                points.append(None)

     
        for a, b in self.POSE_PAIRS:
            if points[a] and points[b]:
                cv2.line(frame, points[a], points[b], (0, 255, 0), 2)


        # height calculation
        head = points[self.HEAD]
        r_ankle = points[self.R_ANKLE]
        l_ankle = points[self.L_ANKLE]

        if head is None:
            return None

        # choose choosing lowest ankle
        ankle = None
        if r_ankle and l_ankle:
            ankle = r_ankle if r_ankle[1] > l_ankle[1] else l_ankle
        else:
            ankle = r_ankle or l_ankle

        if ankle is None:
            return None

        # draw height line
        cv2.line(frame, head, ankle, (255, 0, 0), 3)

        height_pixels = abs(ankle[1] - head[1])

        return height_pixels