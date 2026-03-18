# file: processing2.py 

import numpy as np
import cv2

def apply_kernel(kernel_list, src):
    rows, cols = src.shape[:2]

    # create maps to use in remap
    map_x = np.tile(np.arange(cols, dtype = np.float32), (rows, 1))
    map_y = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows - 1):
        # get translation for this row from kernel list
        dy = kernel_list[i]

        # apply shift to the entire row
        map_y[i, :] = i + dy

    dst = cv2.remap(
        src,
        map_x, map_y,
        interpolation = cv2.INTER_LINEAR,
        borderMode = cv2.BORDER_REPLICATE
    )

    return dst      

def create_kernel_list(equation):
    kernel_list = []
    slopes = np.diff(equation)
    for slope in slopes:
        kernel_list.append(-slope)
    return kernel_list




def calculate_shape(points,length=1081):
    b = np.array([0, points[0], points[1], points[2], 0])
    A = np.vander([0,length/4,length/2,length*3/4,length], N=5, increasing=True)
    coeffs = np.linalg.solve(A, b)
    x_axis = np.arange(0,length+2,1)
    mirror = np.polyval(coeffs[::-1], x_axis)
    return mirror




def get_grid(h, w):
    y, x = np.indices((h, w))
    cx, cy = w // 2, h // 2
    dx = x - cx
    dy = y - cy
    r = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)
    return (dx.astype(np.float32), dy.astype(np.float32),
            r.astype(np.float32), theta.astype(np.float32), cx, cy)


def apply_filter(frame, slider_values=[0,0,0], mode="mirror"):
    
    h, w = frame.shape[:2]
    mirror = calculate_shape(slider_values, h)
    kernel_list = create_kernel_list(mirror)
    frame = apply_kernel(kernel_list, frame)


    if mode == "cartoon":
        return cartoon_filter(frame)
    
    

    return frame



def cartoon_filter(frame):

    color = cv2.bilateralFilter(frame, 9, 150, 150)

    # edge detection 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    edges = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        11,
        5
    )

    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    cartoon = cv2.bitwise_and(color, edges)
    
    return cartoon
