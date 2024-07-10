import torch
import cv2
import numpy as np
import torchvision.ops.boxes as box_ops
from ultralytics.solutions import SpeedEstimator
from datetime import datetime
import os

class SpeedTracker(SpeedEstimator):
    # modify the class to store speeds instead of visualizing them
    def __init__(self, model, iou_threshold=0.20, max_hit=3):
        super().__init__(model)
        
    def estimate_speed(self, tracks):
        """
        Estimates the speed of objects based on tracking data.

        Args:
            im0 (ndarray): Image.
            tracks (list): List of tracks obtained from the object tracking process.
            region_color (tuple, optional): Color to use when drawing regions. Defaults to (255, 0, 0).

        Returns:
            (ndarray): Speed data.
        """
        if tracks[0].boxes.id is None:
            return {}

        self.extract_tracks(tracks)
        for box, trk_id, cls in zip(self.boxes, self.trk_ids, self.clss):
            track = self.store_track_info(trk_id, box)

            if trk_id not in self.trk_previous_times:
                self.trk_previous_times[trk_id] = 0
            self.calculate_speed(trk_id, track)

        return self.dist_data
        

class TrafficMonitor():
    def __init__(self, iou_threshold=0.20, max_hit=3):
        self.vehicles_boxes = []
        self.iou_threshold = iou_threshold
        self.max_hit = max_hit
        self.traffic_light_state = ""
        self.speeds = {}
        self.violators = {0: [], 1: [], 2: []}
    
    def iou(self, box1, box2):
        box1 = torch.tensor([box1], dtype=torch.float32)
        box2 = torch.tensor([box2], dtype=torch.float32)
        iou = box_ops.box_iou(box2, box1)
        return iou.item()
    
    def detect_red_light(self, frame, start, end):
        """Detects red light in the box specified"""
        # color range for maximum red and minimum red
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # color range for maximum green and minimum green
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
        
        lower_yellow = np.array([15, 150, 150])
        upper_yellow = np.array([35, 255, 255])
        
        img = frame[start[1]:end[1], start[0]:end[0]]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        maskg = cv2.inRange(hsv, lower_green, upper_green)
        masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
        maskr = cv2.add(mask1, mask2)

        # Hough circle detect
        r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80,
                                    param1=50, param2=10, minRadius=0, maxRadius=30)

        g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60,
                                    param1=50, param2=10, minRadius=0, maxRadius=30)

        y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30,
                                    param1=50, param2=5, minRadius=0, maxRadius=30)

        # Return string of color
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
    
    def detect_speed_violation(self, speed, limit):
        """Detects if the vehicle has violated the speed limit"""
        if speed > limit:
            return True
        return False
    
    def calculate_box_coordinates(self, start, end):
        """Calculate the box coordinates"""
        x1, y1 = start
        x2, y2 = end
        w = x2 - x1
        h = y2 - y1
        return x1, y1, x1+w, y1+h

    def set_speeds(self, speeds):
        self.speeds = speeds

    def save_evidence(self, frame, vehiclebox, violation_type: int):
        """Save evidence of the traffic violation
        Args:
            frame (ndarray): Frame of the video
            vehiclebox (list): Box object of the vehicle
        """
        x1, y1, x2, y2 = vehiclebox.cpu().xyxy.int().numpy().tolist()[0]
        vehicleimg = frame[y1:y2, x1:x2]
        # add the vehicle box to the image
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        if vehiclebox.id:
            vehicleid = vehiclebox.id.numpy()
        else:
            print("WARNING: Vehicle ID not found")
            return
        self.upload_image(vehicleid, vehicleimg, violation_type)
        self.upload_image(vehicleid, frame, violation_type, vehicle=False)
    
    def upload_image(self, vehicleid, image, violation_type: int, vehicle=True):
        """Uploads the image to file storage
        Args:
            vehicleid (int): ID of the vehicle
            image (ndarray): Image of the vehicle
            violation_type (int): Violation type (0 for traffic light, 1 for speed, 2 for pedestrian crossing)
            vehicle (bool): If the image is of a vehicle or the general scene
        """
        # check if evidence folder exists
        # if not create it
        if not os.path.exists("evidence"):
            os.makedirs("evidence")
        
        # check if vehicles folder exists in evidence
        # if not create it
        if not os.path.exists("evidence/vehicles"):
            os.makedirs("evidence/vehicles")
        
        # check if scenes folder exists in evidence
        # if not create it
        if not os.path.exists("evidence/scenes"):
            os.makedirs("evidence/scenes")
        date = datetime.now().strftime("%Y%m%d")
        # save the image to the respective folder based on vehicle or scene
        if vehicle:
            cv2.imwrite(f"evidence/vehicles/{date}-{vehicleid[0]}-{violation_type}.jpg", image)
        else:
            cv2.imwrite(f"evidence/scenes/{date}-{vehicleid[0]}-{violation_type}.jpg", image)

    def add_violator(self, vehiclebox, violation_type: int, speed: int = None):
        """Add the violator to the list of violators"""
        if violation_type == 0:
            self.violators[0].append(vehiclebox)
        elif violation_type == 1:
            self.violators[1].append({vehiclebox: speed})
        elif violation_type == 2:
            self.violators[2].append(vehiclebox)
    
    def get_traffic_light_violators(self):
        return self.violators[0]
    
    def get_speed_violators(self):
        return self.violators[1]
    
    def get_pedestrian_crossing_violators(self):
        return self.violators[2]
    
    def get_box_from_results(self, results, id):
        for result in results:
            for box in result.boxes:
                if box.id is None:
                    continue
                if box.id == id:
                    return box
        

