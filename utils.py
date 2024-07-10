from datetime import datetime
"""
This module contains utility functions for the traffic monitoring system
File storage is used to store the evidence of traffic violations
"""

def get_image_files(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith('.jpg')]

def parse_filename(filename):
    try:
        date_str, vehicle_id, violation_type = filename.rsplit('.', 1)[0].split('-')
        date = datetime.strptime(date_str, '%Y%m%d')
        return date, vehicle_id, violation_type
    except Exception as e:
        print(f"Error parsing filename {filename}: {e}")
        return None, None, None