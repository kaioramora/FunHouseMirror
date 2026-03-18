# file: height_detection.py
# author: Leiani Butler

import cv2
import mediapipe as mp
import numpy as np 

mp_pose = mp.solutions.pose

class HeightDetector:
    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5

        )

    def get_height_pixels(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)
        
        # debug to see if the pose is even working / being detected 
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        if not results.pose_landmarks:
            return None

        
        h, w = frame.shape[:2]

        landmarks = results.pose_landmarks.landmark

        head = landmarks[mp_pose.PoseLandmark.NOSE]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]


        head_y = int(head.y * h)
        ankle_y = int(max(left_ankle.y, right_ankle.y) * h)

        height_pixels = abs(ankle_y - head_y)

        return height_pixels