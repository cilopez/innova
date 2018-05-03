# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 18:38:26 2018

@author: Hp
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

green = (0,255,255)

def contador():
    i = 0
    while 1:
        yield i
        i += 1

def overlay_mask(mask, image):
    # make the mask rgb
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    # calculates the weightes sum of two arrays. in our case image arrays
    # input, how much to weight each.
    # optional depth value set to 0 no need
    img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
    return img

def show(image):
  # Figure size in inches
  plt.figure(figsize=(10, 10))

  # Show image, with nearest neighbour interpolation
  plt.imshow(image, interpolation='nearest')

def circle_contour(image, contour):
    # Bounding ellipse
    image_c = image.copy()
    # easy function
    rect = cv2.minAreaRect(contour)
    #ellipse = cv2.fitEllipse(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # add it
    cv2.drawContours(image_c,[box],0,(0,0,255),3)
    #cv2.ellipse(image_with_ellipse, ellipse, green, 2, cv2.LINE_AA)
    return image_c

def find_biggest_contour(image):
    # Copy
    image = image.copy()
    # input, gives all the contours, contour approximation compresses horizontal,
    # vertical, and diagonal segments and leaves only their end points. For example,
    # an up-right rectangular contour is encoded with 4 points.
    # Optional output vector, containing information about the image topology.
    # It has as many elements as the number of contours.
    # we dont need it
    image, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST,
                                                  cv2.CHAIN_APPROX_SIMPLE)

    # Isolate largest contour
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in
                     contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
    return biggest_contour, mask

def resize_image(frame):
    frame_gaussian = cv2.GaussianBlur(frame,(7,7),0)
    max_d = max(frame_gaussian.shape)
    scale = 700/max_d
    frame_e = cv2.resize(frame_gaussian,None,fx=scale,fy=scale)
    return frame_e

def contour(mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    # morph the image. closing operation Dilation followed by Erosion.
    # It is useful in closing small holes inside the foreground objects,
    # or small black points on the object.
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # erosion followed by dilation. It is useful in removing noise
    mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
    big_bug_contour, mask_bug = find_biggest_contour(
        255-mask_clean)
    overlay = overlay_mask(mask_clean, frame)
    circled = circle_contour(frame, big_bug_contour)
    return circled,overlay

def scale_image(frame):
    frame_gaussian = cv2.GaussianBlur(frame, (7, 7), 0)
    max_d = max(frame_gaussian.shape)
    scale = 700 / max_d
    frame_o = cv2.resize(frame_gaussian, None, fx=scale, fy=scale)
    return frame_o

def anomaly_contour(mask,frame):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
    big_bug_contour, mask_bug = find_biggest_contour(
        255 - mask_clean)
    overlay = overlay_mask(mask_clean, frame)
    circled = circle_contour(frame, big_bug_contour)
    res = cv2.bitwise_and(frame, frame, mask=mask_clean)
    return res,overlay,circled,mask_clean


def image_processing(path):
    frame_i = cv2.imread(path)
    frame = scale_image(frame_i)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 30, 30])
    upper_green = np.array([140, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green,upper_green)
    mask = green_mask
    a, b, c, d = anomaly_contour(mask,frame)
    cv2.imwrite('mask_{}'.format(path), 255 - d)
    cv2.imwrite('res_{}'.format(path), c)

def video_processing():
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([30, 30, 30])
        upper_green = np.array([140, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = green_mask
        a, b, c, d = anomaly_contour(mask,frame)
        res = cv2.bitwise_and(frame, frame, mask=d)
        cv2.imshow('frame', frame)
        cv2.imshow('res', res)
        k = cv2.waitKey(5) & 0xFF
        if k == 99:
            x = contador()
            cv2.imwrite('mask{}.jpg'.format(next(x)), 255 - d)
            cv2.imwrite('res{}.jpg'.format(next(x)), c)    
        if k == 27:
            break
    cv2.destroyAllWindows()
    del cap


if __name__ == "__main__":
    path = "Lobesia.jpg"
    image_processing(path)
    video_processing()
