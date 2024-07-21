import torch
import cv2
import numpy as np
import torchvision.ops.boxes as box_ops
from ultralytics.solutions import SpeedEstimator
from datetime import datetime
import os
from db import Database
from uuid import uuid1
import pandas as pd
import PySimpleGUI as sg
import matplotlib.pyplot as plt


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
        self.db = Database("Traffic.db")
    
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

    def save_evidence(self, frame, vehiclebox, violation_type: int, speed: int = None):
        """Save evidence of the traffic violation
        Args:
            frame (ndarray): Frame of the video
            vehiclebox (list): Box object of the vehicle
        """
        x1, y1, x2, y2 = vehiclebox.cpu().xyxy.int().numpy().tolist()[0]
        vehicleimg = frame.copy()[y1:y2, x1:x2]
        # add the vehicle box to the image
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        uuid = uuid1()
        if violation_type == 1:
            self.db.insert_violation(datetime.now().strftime("%Y-%m-%d"), str(uuid), violation_type, f"evidence/vehicles/{uuid}.png", f"evidence/scenes/{uuid}.png", speed)
        elif violation_type == 0 or violation_type == 2:
            self.db.insert_violation(datetime.now().strftime("%Y-%m-%d"), str(uuid), violation_type, f"evidence/vehicles/{uuid}.png", f"evidence/scenes/{uuid}.png")
        else:
            print("WARNING: Violation type not recognized")
            return
        self.upload_image(str(uuid), vehicleimg)
        self.upload_image(str(uuid), frame, vehicle=False)
    
    def upload_image(self, uuid, image, vehicle=True):
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
        # save the image to the respective folder based on vehicle or scene
        if vehicle:
            cv2.imwrite(f"evidence/vehicles/{uuid}.png", image)
        else:
            cv2.imwrite(f"evidence/scenes/{uuid}.png", image)

    def add_violator(self, vehiclebox, violation_type: int):
        """Add the violator to the list of violators"""
        if violation_type == 0:
            self.violators[0].append(vehiclebox)
        elif violation_type == 1:
            self.violators[1].append(vehiclebox)
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
        return None

    def get_violations(self, date="All"):
        """Returns the layout for the UI of the violations from the database"""
        violations = self.db.fetch_violations(date)
        if not violations:
            return sg.Text("No violations found", font=('Helvetica', 14), justification='center', expand_x=True, key="-TABLE-")
        violations = pd.DataFrame(violations)
        # change violation values to actual violations 0: traffic light, 1: speed, 2: pedestrian crossing
        violations[3] = violations[3].map({0: "Traffic Light Violation", 1: "Speed Violation", 2: "Pedestrian Crossing Violation"})
        values = violations.to_numpy().tolist()
        headers = self.db.get_headers()
        layout = sg.Table(values=values, headings=headers, key="-TABLE-", display_row_numbers=False, auto_size_columns=True, num_rows=min(25, len(violations)), cols_justification="center", justification="center")
        return layout
    
    def fetch_violations(self):
        """Fetch the violations from the database in a pandas dataframe"""
        violations = self.db.fetch_violations()
        if not violations:
            return pd.DataFrame()
        violations = pd.DataFrame(violations)
        violations[3] = violations[3].map({0: "Traffic Light Violation", 1: "Speed Violation", 2: "Pedestrian Crossing Violation"})
        return violations

    def get_number_of_violations_by_date(self):
        """Returns the number of violations by date"""
        violations = self.db.fetch_violations()
        violations = pd.DataFrame(violations)
        violations[1] = pd.to_datetime(violations[1]).dt.date
        violations = violations.groupby(1).count()
        # return the number of violations by date as a dictionary
        return violations[0].to_dict()
    
    def get_violations_breakdown(self, total=True):
        """Returns the breakdown of violations"""
        if total:
            violations = self.db.fetch_violations()
            violations = pd.DataFrame(violations)
            violations = violations.groupby(3).count()
            # map the violation types to actual violations in the index
            violations.index = violations.index.map({0: "Traffic Light Violation", 1: "Speed Violation", 2: "Pedestrian Crossing Violation"})
            # return the breakdown of violations as a dictionary
            return violations[0].to_dict()
        else:
            violations = self.db.fetch_violations()
            violations = pd.DataFrame(violations)
            # count the number of violations by date
            violations[1] = pd.to_datetime(violations[1]).dt.date
            violations = violations.groupby([1, 3]).count()
            # return the breakdown of violations as a dictionary
            return violations[0].to_dict()
    
    def plot_violations(self):
        """Plots the number of violations by date"""
        violations = self.get_number_of_violations_by_date()
        df = pd.DataFrame(violations, index=[0])
        df = df.transpose()
        df.columns = ["Violations"]
        # convert index to datetime
        df.index = pd.to_datetime(df.index)
        # plot the data in a line chart
        ax = df.plot(kind='line', title='Number of Violations by Date', legend=True)
        ax.set_xticks(df.index)
        ax.set_xticklabels(df.index.strftime('%Y-%m-%d'), rotation=45)
        plt.tight_layout()
        # save the plot
        plt.savefig("violations.png")