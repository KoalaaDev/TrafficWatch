class Camera:
    def __init__(self, url, location):
        self.url =  url
        self.location = location
        self.traffic_light_coordinates = []
        self.traffic_rule_coordinates = []
        self.pedestriancross_coordinates = []

    def set_traffic_light_area(self, coordinates):
        self.traffic_light_coordinates = coordinates

    def set_traffic_rule_area(self, coordinates):
        self.traffic_rule_coordinates = coordinates

    def set_pedestriancross_area(self, coordinates):
        self.pedestriancross_coordinates = coordinates

    def get_camera_url(self):
        return self.url
    
    def get_location(self):
        return self.location
