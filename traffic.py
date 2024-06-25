import torch
import cv2
import numpy as np

class TrafficMonitor():
    def __init__(self, iou_threshold=0.5, max_hit=3):
        self.vehicles_boxes = []
        self.iou_threshold = iou_threshold
        self.max_hit = max_hit
        self.traffic_light_state = ""
    
    def iou(self, box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        x1, y1, x2, y2 = x1 - w1 / 2, y1 - h1 / 2, x2 - w2 / 2, y2 - h2 / 2
        x1, y1, x2, y2 = max(x1, x2), max(y1, y2), min(x1 + w1, x2 + w2), min(y1 + h1, y2 + h2)
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        union = w1 * h1 + w2 * h2 - intersection
        return intersection / union
    
    def detect_red_light(self, frame, start, end):
        """Detects red light in the box specified"""
        # color range
        lower_red1 = np.array([0,100,100])
        upper_red1 = np.array([10,255,255])
        lower_red2 = np.array([160,100,100])
        upper_red2 = np.array([180,255,255])
        lower_green = np.array([40,50,50])
        upper_green = np.array([90,255,255])
        # lower_yellow = np.array([15,100,100])
        # upper_yellow = np.array([35,255,255])
        img = frame[start[1]:end[1], start[0]:end[0]]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([15,150,150])
        upper_yellow = np.array([35,255,255])
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        maskg = cv2.inRange(hsv, lower_green, upper_green)
        masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
        maskr = cv2.add(mask1, mask2)
        # print size

        # hough circle detect
        r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80,
                                param1=50, param2=10, minRadius=0, maxRadius=30)

        g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60,
                                    param1=50, param2=10, minRadius=0, maxRadius=30)

        y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30,
                                    param1=50, param2=5, minRadius=0, maxRadius=30)

        # return string of color
        if r_circles is not None:
            return "red"
        elif g_circles is not None:
            return "green"
        elif y_circles is not None:
            return "yellow"
        
    def set_traffic_light_state(self, frame, start, end):
        """Set the traffic light state"""
        self.traffic_light_state = self.detect_red_light(frame, start, end)
    
    def detect_traffic_light_violation(self, vehiclebox, rulebox):
        """Detects if the vehicle has violated the traffic light"""
        if self.iou(vehiclebox, rulebox) > self.iou_threshold:
            return True
        return False