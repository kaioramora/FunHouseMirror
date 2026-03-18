FUNHOUSE MIRROR PROJECT 
=======================

Authors: Leiani Butler, Therese Georgia, Alex Gregor


-------------------------------------------------------------
Project Description
-------------------------------------------------------------


Funhouse Mirror project with tablet control interface. This project uses a live camera feed, image processing, and machine learning to create dynamic, customizable mirror distotions to respond to the user in real time.

Features:
- Real-time camera feed 
- Polynomial-based mirror distortion 
- Adjustable distortion w/ 3 sliders
- Cartoon Filter Mode
- MediaPipe height detection for dynamic scaling 
- Countdown photo capture and save 
- Real-time mirror shape plot (using matplotlib)


-------------------------------------------------------------
HOW IT WORKS
-------------------------------------------------------------

1. Camera system
    - uses OpenCV VideoCapture in a threaded class
    - Frames are flipped horizontally for mirror behavior

2. Mirror Distortion 
    - A 4th order polynomial is calculated using 3 slider control points 
    - the plynomial defines vertical pixel shifts
    - OpenCV remap() applies distortion

3. Cartoon Filter 
    - bilateral filtering smooths color 
    - adaptive threshold gets edges 
    - edges are combined with the smoothed image

4. Height Detection (Machine Learning)
    - mediapipe pose detects body landmarks 
    - nose and ankle posiitons determine height in pixels 
    - mirror distortion scales based on the user's distance

5. GUI
    - tablet control window (sliders + buttons)
    - seperate camera display window
    - countdown timer for image capture

6. Plotting 
    - real-time mirror shape plotted using matplotlib


-------------------------------------------------------------
FILES 
-------------------------------------------------------------
main2.py            -> Main controller 
gui2.py             -> Tablet + Camera windows
camera2.py          -> Threaded camera class 
processing2.py      -> Mirror + cartoon processing 
height_detection.py -> MediaPipe pose height logic


-------------------------------------------------------------
DEPENDENCIES
-------------------------------------------------------------

pip install: 
- opencv-python
- mediapipe
- numpy
- matplotlib
- PyQt5



-------------------------------------------------------------
INSPIRATION / REFERENCES
-------------------------------------------------------------

OpenCV Remap: 
