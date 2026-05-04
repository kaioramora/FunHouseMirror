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
- Height detection for dynamic scaling 
- Countdown photo capture and save 
- Real-time mirror shape plot (using matplotlib)
- Dual-screen GUI (mirror and tablet controls)

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
    - opencv pose detects body landmarks 
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
main2.py                -> Main controller 
gui2.py                 -> Tablet + Camera windows
camera2.py              -> Threaded camera class 
processing2.py          -> Mirror + cartoon processing 
cv_height_detection.py  ->  Height detection logic


-------------------------------------------------------------
DEPENDENCIES
-------------------------------------------------------------

pip install: 
- opencv-python
- numpy
- matplotlib
- PyQt5
- qrcode 
- pillow

-------------------------------------------------------------
RUNNING
-------------------------------------------------------------
python3 main2.py


-------------------------------------------------------------
DUAL SCREEN SETUP 
-------------------------------------------------------------
Display 1 -> Mirror Display 
Display 2 -> Tablet Contorols and Mirror Display
- this screen indices can be modiied in main.py if needed. 


-------------------------------------------------------------
CONTROLS
-------------------------------------------------------------
Sliders control mirror curvature
Buttons: 
- Reset     -> clears fliter and sets sldier values to zero
- Countdown -> saves photos after 3 seconds
- Cartoon   -> toggles filter


-------------------------------------------------------------
IMAGE CAPTURE
-------------------------------------------------------------
1. Press Countdown 
2. Wait 3 Seconds 
3. Image saved automatically
4. QR code is generated (not yet properly linked)

Saved to:

saved_images/capture.png

-------------------------------------------------------------
HEIGHT DETECTION
-------------------------------------------------------------
Uses OpenCV HOG person detector

Height scale = detected height / reference height



-------------------------------------------------------------
CARTOON FILTER
-------------------------------------------------------------
- bilateral filtering 
- adaptive threshold edges 
- edge masking




-------------------------------------------------------------
THREADED CAMERA
-------------------------------------------------------------
Camera runs in background thread for smooth FPS and responsive GUI.


-------------------------------------------------------------
TESTING MODULES
-------------------------------------------------------------
There are tests that can be run for the following files: 

Camera only: python camera2.py 
GUI only: python gui2.py 


-------------------------------------------------------------
LINUX NOTES
-------------------------------------------------------------
If you get a Qt error: 

export QT_QPA_PLATFORM=xcb

-------------------------------------------------------------
KNOW LIMITATIONS
-------------------------------------------------------------
- HOG detection is extremely sensitive and often buggy 
- Needs to be on a dual monitor set-up to work 
- QR code not currently linked


-------------------------------------------------------------
FUTURE IMPROVEMENTS
-------------------------------------------------------------
- Implement mediapipe pose tracking
- Host QR code website
- Add additional filters
- Grid overlayed on mirror display showing distortions


-------------------------------------------------------------
Author 
-------------------------------------------------------------
Leiani Butler, Therese Georgia, Alex Gregor
FunHouseMirror