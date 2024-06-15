import PySimpleGUI as sg
import cv2
from camera import Camera

class UI:
    def __init__(self, stream_urls, model, colours):
        self.cameras = [Camera(url, location) for location, url in stream_urls.items()]
        self.current_stream_index = 0
        self.num_streams = len(stream_urls)
        self.toggle_detector = False
        self.model = model
        self.cap = cv2.VideoCapture(self.cameras[self.current_stream_index].get_camera_url())
        self.layout = [
        [sg.Button("Settings"), sg.Button("Add Stream"), sg.Button("Remove Stream")],
        [sg.Button(image_filename="icons/left.png", key="Previous"), sg.Image(filename="", key="-IMAGE-"), sg.Button(image_filename="icons/right.png", key="Next")],
        [sg.Button("Toggle Detector"), sg.Button("Exit")]
        ]
        self.colours = colours
    
    def render_frame(self):
        _, frame = self.cap.read()
        frame = cv2.resize(frame, (800, 400))
        if self.cameras[self.current_stream_index].traffic_rule_coordinates:
            start, end = self.cameras[self.current_stream_index].traffic_rule_coordinates
            frame = cv2.rectangle(frame, start, end, (0, 0, 255), 2)
        if self.cameras[self.current_stream_index].traffic_light_coordinates:
            start, end = self.cameras[self.current_stream_index].traffic_light_coordinates
            frame = cv2.rectangle(frame, start, end, (0, 255, 0), 2)
        if self.cameras[self.current_stream_index].pedestriancross_coordinates:
            start, end = self.cameras[self.current_stream_index].pedestriancross_coordinates
            frame = cv2.rectangle(frame, start, end, (255, 0, 0), 2)
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        return imgbytes
    
    def draw_rules_window(self):
        layout = [[sg.Combo(["Traffic line Rule", "Traffic light", "Pedestrian Crossing"], size = (20, 1), key="shape", default_value="Traffic line Rule", readonly=True),],
                           [sg.Graph((800, 400), (0, 0), (800, 400), background_color='white', key='-GRAPH-', drag_submits=True, enable_events=True)],
                           [sg.Button("Save"), sg.Button("Cancel")]]
        settings_window = sg.Window("Edit Rules", layout, modal=True, finalize=True)
        graph = settings_window["-GRAPH-"]
        dragging = False
        start_point = end_point = prior_rect = None
        # image is the video frame on the main window
        imgbytes = self.render_frame()
        settings_window["-GRAPH-"].draw_image(data=imgbytes, location=(0, 400))
        while True:
            event, values = settings_window.read()

            if event == sg.WIN_CLOSED or event == "Cancel":
                break  # exit
            
            if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse
                x, y = values["-GRAPH-"]
                if not dragging:
                    start_point = [x, y]
                    dragging = True
                else:
                    end_point = [x, y]
                if prior_rect:
                    graph.delete_figure(prior_rect)
                if None not in (start_point, end_point):
                    prior_rect = graph.draw_rectangle(start_point, end_point, line_color='red')
                
            elif event.endswith('+UP'):  # The drawing has ended because mouse up
                start_point[1] = 400 - start_point[1]
                end_point[1] = 400 - end_point[1]
                saved_rect = (start_point, end_point)
                print("MOUSE UP", values, start_point, end_point)
                start_point, end_point = None, None  # enable grabbing a new rect
                dragging = False
            elif event == "Save":
                if saved_rect:
                    if values["shape"] == "Traffic line Rule":
                        # mirror the x and y coordinates
                        self.cameras[self.current_stream_index].set_traffic_rule_area(saved_rect)
                    elif values["shape"] == "Traffic light":
                        self.cameras[self.current_stream_index].set_traffic_light_area(saved_rect)
                    elif values["shape"] == "Pedestrian Crossing":
                        self.cameras[self.current_stream_index].set_pedestriancross_area(saved_rect)
                    saved_rect = None
                    break
                else:
                    sg.popup("Please draw a shape before saving!")

            else:
                print("unhandled event", event, values)
        settings_window.close()
    # Function to create and handle settings window
    def open_settings_window(self):
        rules_layout = [[sg.Text("Set Traffic Rules")],
                        [sg.Graph((800, 400), (0, 0), (800, 400), background_color='white', key='-RULES-')],
                        [sg.Button("Edit Rules")]]
        settings_layout = [[sg.TabGroup([[sg.Tab("Rules", rules_layout)]])]]
        settings_window = sg.Window("Settings", settings_layout, modal=True, finalize=True)
        
        imgbytes = self.render_frame()
        settings_window["-RULES-"].draw_image(data=imgbytes, location=(0, 400))
        while True:
            event, values = settings_window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Edit Rules":
                settings_window.modal = False
                self.draw_rules_window()
                settings_window.modal = True
                imgbytes = self.render_frame()
                settings_window["-RULES-"].draw_image(data=imgbytes, location=(0, 400))
        settings_window.close()
    def open_add_stream_window(self):
        layout = [[sg.Text("Enter Location Name:"), sg.InputText()],
                  [sg.Text("Enter Stream URL:"), sg.InputText()],
                  [sg.Button("Add"), sg.Button("Cancel")]]
        window = sg.Window("Add Stream", layout)
        
        while True:
            event, values = window.read()
            print(event, values)
            if event == sg.WIN_CLOSED or event == "Cancel":
                break
            if event == "Add":
                if values[0] == "" or values[1] == "":
                    sg.popup("Please enter both location name and stream URL!")
                    continue
                location = values[0]
                url = values[1]
                self.cameras.append(Camera(url, location))
                self.num_streams += 1
                break
        window.close()
        
    def handle_button_clicks(self, event):
        if event == sg.WINDOW_CLOSED or event == "Exit":
            return True
            
        if event == "Settings":
            self.open_settings_window()
        
        if event == "Toggle Detector":
            self.toggle_detector = not self.toggle_detector
        # Switch to the next stream if 'Next' button is pressed
        if event == "Next":
            self.current_stream_index = (self.current_stream_index + 1) % self.num_streams
            
            self.cap.release()
            self.cap = cv2.VideoCapture(self.cameras[self.current_stream_index].get_camera_url())

        # Switch to the previous stream if 'Previous' button is pressed
        elif event == "Previous":
            self.current_stream_index = (self.current_stream_index - 1) % self.num_streams
            self.cap.release()
            self.cap = cv2.VideoCapture(self.cameras[self.current_stream_index].get_camera_url())
        
        elif event == "Add Stream":
            self.open_add_stream_window()
        
        elif event == "Remove Stream":
            if self.num_streams > 1:
                self.cameras.pop(self.current_stream_index)
                self.num_streams -= 1
                self.current_stream_index = 0
                self.cap.release()
                self.cap = cv2.VideoCapture(self.cameras[self.current_stream_index])
            else:
                sg.popup("Cannot remove the last stream!")

    def process_video(self, frame):
        # Use YOLO model to predict objects in the frame
        results = self.model.track(source=frame, imgsz=640, conf=0.5, persist=True)

        # Draw bounding boxes on the frame
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.cpu().xyxy.int().numpy().tolist()[0]
                confidence = box.conf.item()
                class_id = box.cls.item()
                if box.id is None:
                    label = f"{self.model.names[class_id]} {confidence:.2f}"
                else:
                    label = f"{int(box.id.numpy())}:{self.model.names[class_id]} {confidence:.2f}"
                box_colour = self.colours.get(self.model.names[class_id], "white")
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), box_colour, 2)
                
                frame = cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Event loop to handle button clicks and display video streams
    def event_loop(self):
        window = sg.Window("Traffic Watch", self.layout, finalize=True)
        # Event loop to handle button clicks and display video streams
        while True:
            event, _ = window.read(timeout=4)
            done = self.handle_button_clicks(event)
            if done:
                break
            ret, frame = self.cap.read()
            if not ret:
                break
            
            if self.toggle_detector:
                self.process_video(frame)
            # Convert frame to format PySimpleGUI can display
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes)

        window.close()
        self.cap.release()
        cv2.destroyAllWindows()