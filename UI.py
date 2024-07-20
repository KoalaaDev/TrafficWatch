import PySimpleGUI as sg
import cv2
from camera import Camera
from traffic import TrafficMonitor, SpeedTracker
from utils import *

check = b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAIAAAC0Ujn1AAAV7mVYSWZNTQAqAAAACAAKAAsAAgAAACYAAAiSARIAAwAAAAEAAQAAARoABQAAAAEAAAi4ARsABQAAAAEAAAjAASgAAwAAAAEAAgAAATEAAgAAACYAAAjIATIAAgAAABQAAAjuAhMAAwAAAAEAAQAAh2kABAAAAAEAAAkC6hwABwAACAwAAACGAAARhhzqAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAV2luZG93cyBQaG90byBFZGl0b3IgMTAuMC4xMDAxMS4xNjM4NAAAAAEsAAAAAQAAASwAAAABV2luZG93cyBQaG90byBFZGl0b3IgMTAuMC4xMDAxMS4xNjM4NAAyMDI0OjA2OjI1IDIwOjM3OjAxAAAGkAMAAgAAABQAABFckAQAAgAAABQAABFwkpEAAgAAAAM1MwAAkpIAAgAAAAM1MwAAoAEAAwAAAAEAAQAA6hwABwAACAwAAAlQAAAAABzqAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAyNDowNjoyNSAyMDoz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'
uncheck = b'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAIAAAC0Ujn1AAAVVGVYSWZNTQAqAAAACAAKAAsAAgAAACYAAAiSARIAAwAAAAEAAQAAARoABQAAAAEAAAi4ARsABQAAAAEAAAjAASgAAwAAAAEAAgAAATEAAgAAACYAAAjIATIAAgAAABQAAAjuAhMAAwAAAAEAAQAAh2kABAAAAAEAAAkC6hwABwAACAwAAACGAAARhhzqAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAV2luZG93cyBQaG90byBFZGl0b3IgMTAuMC4xMDAxMS4xNjM4NAAAAAEsAAAAAQAAASwAAAABV2luZG93cyBQaG90byBFZGl0b3IgMTAuMC4xMDAxMS4xNjM4NAAyMDI0OjA2OjI1IDIwOjM2OjA1AAAGkAMAAgAAABQAABFckAQAAgAAABQAABFwkpEAAgAAAAM1MwAAkpIAAgAAAAM1MwAAoAEAAwAAAAEAAQAA6hwABwAACAwAAAlQAAAAABzqAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAyNDowNjoyNSAyMDozNTowNgAyMDI0OjA2OjI1IDIwOjM1OjA2AAAAAAYBAwADAAAAAQAGAAABGgAFAAAAAQAAEdQBGwAFAAAAAQAAEdwBKAADAAAAAQACAAACAQAEAAAAAQAAEeQCAgAEAAAAAQAAA28AAAAAAAAAYAAAAAEAAABgAAAAAf/Y/9sAQwAIBgYHBgUIBwcHCQkICgwUDQwLCwwZEhMPFB0aHx4dGhwcICQuJyAiLCMcHCg3KSwwMTQ0NB8nOT04MjwuMzQy/9sAQwEJCQkMCwwYDQ0YMiEcITIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy/8AAEQgAHgAeAwEhAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A1/ht8PfDHjHwPaeIfEOnNqGrX8s8lxcy3EoLsJXXorAdAK6z/hTHw+/6F1P/AAJm/wDi6AD/AIUx8Pv+hdT/AMCZv/i68s+Mfh7TvhydFvPB63OjXF2J4p5LW7lBkUeWQCSx4z6f0FAHp3wR/wCSR6L9bj/0fJXoNABXgv7TH/Hp4b/66XH8o6AO5+CP/JI9F+tx/wCj5K9BoAK8F/aY/wCPTw3/ANdLj+UdAGb4f+La/DHTZPBl5opvptJup4Dcw3OxZP3jHOCvHJNan/DS9n/0LE//AIGD/wCIoAP+Gl7P/oWJ/wDwMH/xFc54j8Q3fx21Kx0rSbCDTJNNhmuXe7uSwcMY1wNqcY4+ue2OQD//2QDC5AwnAAABbUlEQVR4nO2Wsa3CQBBEZ/fOIMu0QEREBaQUQB2UQSc0QEwTiA6QaIAMCQTW3e3+YJADgq9vE34msS2f397OSZ5FSmm1WokIAACj0QgfiJymaS6XS9xsNvv9HsB0Og0hpJRijADcvRdUVc2sqqrz+Xy/32ezGeq6rqpqt9vlnP0DlVLcnZCXB7y0bdstSil9QjezxWIBQNn49XplX+4eY+zrBoCcs6oCKKXcbjdV1fF4DKCua+JKKV0rvcQTYgHW0LZtRSSlJCJmxi2bWV80P4kxqipRGkLgNs2MpywiLNtL/ISmvyB86N4NgL6JZrr7p6Bf9EV/0V/0F/0P0fxZD0isNzH5mDWkqbtz/OAKVhoQuyEEM2Nm5ZxFRFmqaRquYJINaOL5fDL/ALxmgslkAuB4PJpZSsnMGG4D5pBuSGK6y3q93m63pZTlcsmmaA5b+7torKoeDofH41FKQc55Pp/TgQ7Hsn1FNO9Pp9MPnB2U/gRUC0gAAAAASUVORK5CYII='
class UI:
    def __init__(self, stream_urls, model, colours):
        self.cameras = [Camera(url, location) for location, url in stream_urls.items()]
        self.current_stream_index = 0
        self.num_streams = len(stream_urls)
        self.toggle_detector = False
        self.manual_traffic_mode = False
        self.model_confidence = 0.5
        self.model = model
        self.speed_estimator = SpeedTracker(self.model.names)
        self.cap = cv2.VideoCapture(self.cameras[self.current_stream_index].get_camera_url())
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.layout = [
        [sg.Button("Settings"), sg.Button("Add Stream"), sg.Button("Remove Stream"), sg.Button("Events")],
        [sg.Button(image_filename="icons/left.png", key="Previous"), sg.Image(filename="", key="-IMAGE-"), sg.Button(image_filename="icons/right.png", key="Next")],
        [sg.Button("Toggle Detector"), sg.Button("Exit")]
        ]
        self.colours = colours
        self.monitor = TrafficMonitor()
    
    def render_frame(self):
        _, frame = self.cap.read()
        if self.cameras[self.current_stream_index].traffic_rule_coordinates:
            start, end = self.cameras[self.current_stream_index].traffic_rule_coordinates
            frame = cv2.rectangle(frame, start, end, (0, 0, 255), 2)
        if self.cameras[self.current_stream_index].traffic_light_coordinates:
            start, end = self.cameras[self.current_stream_index].traffic_light_coordinates
            frame = cv2.rectangle(frame, start, end, (0, 255, 0), 2)
        if self.cameras[self.current_stream_index].pedestriancross_coordinates:
            start, end = self.cameras[self.current_stream_index].pedestriancross_coordinates
            frame = cv2.rectangle(frame, start, end, (255, 0, 0), 2)
        if self.cameras[self.current_stream_index].speeddetection_line:
            start, end = self.cameras[self.current_stream_index].speeddetection_line
            frame = cv2.line(frame, start, end, (0, 0, 255), 2)
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        return imgbytes
    
    def draw_rules_window(self):
        layout = [[sg.Combo(["Traffic line Rule", "Traffic light", "Pedestrian Crossing", "Speed detection"], size=(20, 1), key="shape", default_value="Traffic line Rule", readonly=True, enable_events=True)],
                [sg.Graph((1280, 720), (0, 0), (1280, 720), background_color='white', key='-GRAPH-', drag_submits=True, enable_events=True)],
                [sg.Button("Save"), sg.Button("Cancel")]]
        settings_window = sg.Window("Edit Rules", layout, modal=True, finalize=True)
        graph = settings_window["-GRAPH-"]
        dragging = False
        start_point = end_point = prior_shape = None
        saved_shape = None
        # image is the video frame on the main window
        imgbytes = self.render_frame()
        settings_window["-GRAPH-"].draw_image(data=imgbytes, location=(0, 720))
        on_shape = "Traffic line Rule"
        while True:
            event, values = settings_window.read()

            if event == sg.WIN_CLOSED or event == "Cancel":
                break  # exit
            
            if event == "shape":
                # when changing shape, save the current shape and refresh to show it
                if saved_shape:
                    _, start_point, end_point = saved_shape
                    if on_shape == "Traffic line Rule":
                        self.cameras[self.current_stream_index].set_traffic_rule_area((start_point, end_point))
                    elif on_shape == "Traffic light":
                        self.cameras[self.current_stream_index].set_traffic_light_area((start_point, end_point))
                    elif on_shape == "Pedestrian Crossing":
                        self.cameras[self.current_stream_index].set_pedestriancross_area((start_point, end_point))
                    elif on_shape == "Speed detection":
                        self.cameras[self.current_stream_index].set_speed_detection_line((start_point, end_point))
                    saved_shape = None
                    imgbytes = self.render_frame()
                    settings_window["-GRAPH-"].draw_image(data=imgbytes, location=(0, 720))
                    on_shape = values["shape"]

            if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse
                x, y = values["-GRAPH-"]
                if not dragging:
                    start_point = [x, y]
                    dragging = True
                else:
                    end_point = [x, y]
                if prior_shape:
                    graph.delete_figure(prior_shape)
                if None not in (start_point, end_point):
                    if values["shape"] == "Speed detection":
                        prior_shape = graph.draw_line(start_point, end_point, color='red')
                    else:
                        prior_shape = graph.draw_rectangle(start_point, end_point, line_color='red')
            
            elif event.endswith('+UP'):  # The drawing has ended because mouse up
                if values["shape"] == "Speed detection":
                    start_point[1] = 720 - start_point[1]
                    end_point[1] = 720 - end_point[1]
                    saved_shape = ("line", start_point, end_point)
                else:
                    start_point[1] = 720 - start_point[1]
                    end_point[1] = 720 - end_point[1]
                    saved_shape = ("rectangle", start_point, end_point)
                start_point, end_point = None, None  # enable grabbing a new shape
                dragging = False
            elif event == "Save":
                if saved_shape:
                    _, start_point, end_point = saved_shape
                    if values["shape"] == "Traffic line Rule":
                        self.cameras[self.current_stream_index].set_traffic_rule_area((start_point, end_point))
                    elif values["shape"] == "Traffic light":
                        self.cameras[self.current_stream_index].set_traffic_light_area((start_point, end_point))
                    elif values["shape"] == "Pedestrian Crossing":
                        self.cameras[self.current_stream_index].set_pedestriancross_area((start_point, end_point))
                    elif values["shape"] == "Speed detection":
                        self.cameras[self.current_stream_index].set_speed_detection_line((start_point, end_point))
                    saved_shape = None
                    break
                else:
                    sg.popup("Please draw a shape before saving!")
            else:
                print("unhandled event", event, values)
        settings_window.close()
    # Function to create and handle settings window
    def open_settings_window(self):
        model_tickbox = check if self.manual_traffic_mode else uncheck
        rules_layout = [[sg.Text("Set Traffic Rules", font=('Helvetica', 16), justification='center')],
                        [sg.Graph((1280, 720), (0, 0), (1280, 720), background_color='white', key='-RULES-')],
                        [sg.Button("Edit Rules")]]
        model_layout = [[sg.Text("Edit Model Parameters", font=('Helvetica', 16), justification='center')],
                  [sg.Text("Confidence Threshold"), sg.Slider((0,1),self.model_confidence,0.01, orientation="horizontal", size=(20, 20), key='-CONFIDENCESLIDER-', enable_events=True),sg.InputText('0', size=(5, 1), key='-CONFIDENCEINPUT-', enable_events=True)],
                  [sg.Text("Overlap Threshold"), sg.Slider((0,1),self.monitor.iou_threshold,0.01, orientation="horizontal", size=(20, 20), key='-IOUSLIDER-', enable_events=True),sg.InputText('0', size=(5, 1), key='-IOUINPUT-', enable_events=True)],
                  [sg.Text("Speed Limit"), sg.Slider((0,300),self.cameras[self.current_stream_index].speedlimit,1, orientation="horizontal", size=(20, 20), key='-SPEEDSLIDER-', enable_events=True),sg.InputText('0', size=(5, 1), key='-SPEEDINPUT-', enable_events=True)],
                  [sg.Text("Enable Manual Traffic Detection"),sg.Image(source=model_tickbox, key="manual_traffic_mode", enable_events=True)]]
        settings_layout = [[sg.TabGroup([[sg.Tab("Rules", rules_layout)], [sg.Tab("Model", model_layout)]])]]
        settings_window = sg.Window("Settings", settings_layout, modal=True, finalize=True)
        
        imgbytes = self.render_frame()
        settings_window["-RULES-"].draw_image(data=imgbytes, location=(0, 720))
        while True:
            event, values = settings_window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Edit Rules":
                settings_window.modal = False
                self.draw_rules_window()
                settings_window.modal = True
                imgbytes = self.render_frame()
                settings_window["-RULES-"].draw_image(data=imgbytes, location=(0, 720))
            # If slider is moved, update input box
            if event == '-CONFIDENCESLIDER-':
                settings_window['-CONFIDENCEINPUT-'].update(value=values['-CONFIDENCESLIDER-'])
                self.model_confidence = values['-CONFIDENCESLIDER-']

            if event == '-IOUSLIDER-':
                settings_window['-CONFIDENCEINPUT-'].update(value=values['-CONFIDENCESLIDER-'])
                self.monitor.iou_threshold = values['-CONFIDENCESLIDER-']

            if event == '-SPEEDSLIDER-':
                settings_window['-CONFIDENCEINPUT-'].update(value=values['-CONFIDENCESLIDER-'])
                self.cameras[self.current_stream_index].speedlimit = values['-CONFIDENCESLIDER-']
            # If input box is changed, update slider
            if event == '-CONFIDENCEINPUT-':
                if values['-CONFIDENCEINPUT-'] == "":  # make sure that the input is not empty
                    pass
                else:
                    new_value = float(values['-CONFIDENCEINPUT-'])
                    if 0 <= new_value <= 1:
                        settings_window['-CONFIDENCESLIDER-'].update(value=new_value)
                        self.model_confidence = new_value

            if event == '-IOUINPUT-':
                if values['-IOUINPUT-'] == "":  # make sure that the input is not empty
                    pass
                else:
                    new_value = float(values['-IOUINPUT-'])
                    if 0 <= new_value <= 1:
                        settings_window['-IOUSLIDER-'].update(value=new_value)
                        self.monitor.iou_threshold = new_value
            if event == '-SPEEDINPUT-':
                if values['-SPEEDINPUT-'] == "":
                    pass
                else:
                    new_value = float(values['-SPEEDINPUT-'])
                    if 0 <= new_value <= 300:
                        settings_window['-SPEEDSLIDER-'].update(value=new_value)
                        self.cameras[self.current_stream_index].speedlimit = new_value

            if event == "manual_traffic_mode":
                self.manual_traffic_mode = not self.manual_traffic_mode
                if self.manual_traffic_mode:
                    settings_window["manual_traffic_mode"].update(source=check)
                else:
                    settings_window["manual_traffic_mode"].update(source=uncheck)
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
        
        elif event == "Events":
            self.events_page()

    def process_video(self, frame):
        # Use YOLO model to predict objects in the frame
        if self.manual_traffic_mode:
            results = self.model.track(source=frame, imgsz=640, conf=self.model_confidence, persist=True, classes=[0,1,5])
        else:
            results = self.model.track(source=frame, imgsz=640, conf=self.model_confidence, persist=True)
        copiedframe = frame.copy() #copy frame for backup
        # Draw bounding boxes on the frame
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.cpu().xyxy.int().numpy().tolist()[0]
                confidence = box.conf.item()
                class_id = box.cls.item()
                if box.id is None:
                    label = f"{self.model.names[class_id]} {confidence:.2f}"
                else:
                    if self.cameras[self.current_stream_index].speeddetection_line and int(box.id.numpy()) in self.speed_estimator.dist_data:
                        label = f"{int(box.id.numpy())}:{self.model.names[class_id]} {confidence:.2f} {self.speed_estimator.dist_data[int(box.id.numpy())]:.2f} km/h"
                    else:
                        label = f"{int(box.id.numpy())}:{self.model.names[class_id]} {confidence:.2f}"
                
                # if self.model.names[class_id] in ["Traffic Light Red", "Traffic-Light-Green", "Traffic-Light-Orange"]:
                #     self.cameras[self.current_stream_index].set_traffic_light_coordinates((x1, y1), (x2, y2))
                box_colour = self.colours.get(self.model.names[class_id], "white")
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), box_colour, 2)
                frame = cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                if self.cameras[self.current_stream_index].traffic_rule_coordinates:
                    start, end = self.cameras[self.current_stream_index].traffic_rule_coordinates
                    if self.monitor.detect_traffic_light_violation(self.monitor.calculate_box_coordinates(start, end),(x1, y1, x2, y2)) and self.cameras[self.current_stream_index].traffic_status == "red":
                        frame = cv2.putText(frame, "Traffic Light Violation", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        if box.id not in self.monitor.get_traffic_light_violators():
                            self.monitor.add_violator(box.id, 0, 0)
                            self.monitor.save_evidence(copiedframe, box, 0)

                    frame = cv2.rectangle(frame, start, end, (0, 0, 255), 2)
                if self.cameras[self.current_stream_index].speedlimit and self.cameras[self.current_stream_index].speeddetection_line:
                    self.speed_estimator.estimate_speed(results)
                    self.monitor.set_speeds(self.speed_estimator.dist_data)
                    for track_id, speed in self.speed_estimator.dist_data.items():
                        if self.monitor.detect_speed_violation(speed, self.cameras[self.current_stream_index].speedlimit):
                            if track_id not in self.monitor.get_speed_violators():
                                self.monitor.add_violator(track_id, speed, 1)
                                violationbox = self.monitor.get_box_from_results(results, track_id)
                                if violationbox:
                                    self.monitor.save_evidence(copiedframe, violationbox, 1)
                                else:
                                    print("WARNING: Box not found for speed violation")
        self.process_traffic_rules(frame, copiedframe.copy(), results)

    def process_traffic_rules(self, frame, copiedframe, results):
        
        if self.manual_traffic_mode:
            if self.cameras[self.current_stream_index].traffic_light_coordinates:
                # manually detect traffic light status using color detection
                start, end = self.cameras[self.current_stream_index].traffic_light_coordinates
                status = self.monitor.detect_red_light(copiedframe, start, end)
                if status is not None:
                    self.cameras[self.current_stream_index].set_traffic_status(status)
                frame = cv2.putText(frame, "STATUS: "+ self.cameras[self.current_stream_index].traffic_status,(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                frame = cv2.rectangle(frame, start, end, (0, 255, 0), 2)
        else:
            # automatically detect traffic light status from the model
            boxes = [box for result in results for box in result.boxes if box.cls.item() == 2 or box.cls.item() == 3 or box.cls.item() == 4]
            if boxes:
                if boxes[0].cls.item() == 2:
                    self.cameras[self.current_stream_index].set_traffic_status("red")
                elif boxes[0].cls.item() == 3:
                    self.cameras[self.current_stream_index].set_traffic_status("green")
                elif boxes[0].cls.item() == 4:
                    self.cameras[self.current_stream_index].set_traffic_status("orange")
            frame = cv2.putText(frame, "STATUS: "+ self.cameras[self.current_stream_index].traffic_status,(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                   
        if self.cameras[self.current_stream_index].pedestriancross_coordinates:
            start, end = self.cameras[self.current_stream_index].pedestriancross_coordinates
            frame = cv2.rectangle(frame, start, end, (255, 0, 0), 2)
        
        if self.cameras[self.current_stream_index].speeddetection_line:
            start, end = self.cameras[self.current_stream_index].speeddetection_line
            frame = cv2.line(frame, start, end, (0, 0, 255), 2)
            self.speed_estimator.reg_pts = [start, end]
            
    def events_page(self):
        violations = self.monitor.violators
        violation_records = self.monitor.fetch_violations()
        # 0 = Traffic Light Violation, 1 = Speed Violation, 2 = Pedestrian Crossing Violation
        table_tab = [
            [sg.Text("Violations", font=('Helvetica', 16), justification='center')],
            [self.monitor.get_violations()]
        ]
        pictures = self.create_gallery_layout("evidence/scenes")
        # gallery tab with buttons to view the next 9 images
        if len(pictures) == 0:
            gallery_tab = [
                [sg.Text("Gallery", font=('Helvetica', 16), justification='center')],
                [sg.Text("No violations recorded", key="-Gallery-", font=('Helvetica', 14), justification='center', expand_x=True)]
            ]
        else:
            gallery_tab = [
                [sg.Text("Gallery", font=('Helvetica', 16), justification='center')],
                [sg.Column(pictures, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(950, 290), justification='center', key="-Gallery-")]
            ]
        analytics_tab = [
            [sg.Text("Analytics", font=('Helvetica', 16), justification='center')],
            [sg.Button("View Analytics")]
        ]
        layout = [[sg.TabGroup([[sg.Tab("Violations", table_tab), sg.Tab("Gallery", gallery_tab, ), sg.Tab("Analytics", analytics_tab)]])]]
        window = sg.Window("Events", layout, finalize=True)
        window['-TABLE-'].expand(True, True)
        window['-Gallery-'].expand(True, True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event in violation_records[2].to_list():
                violation_record = violation_records.loc[violation_records[2] == event]
                self.generate_report_layout(violation_record)
            print(event)
            print(violation_records[2].to_list())
    def create_gallery_layout(self, folder):
        files = get_image_files(folder)
        buttons = []
        for file in files:
            picture = cv2.imread(file.path)
            picture = cv2.resize(picture, (300, 250))
            picture = cv2.imencode(".png", picture)[1].tobytes()
            buttons.append(sg.Button(image_data=picture, key=file.name.strip(".png"), button_color=('white', 'white'), enable_events=True, image_size=(300, 250)))

        cols = split_list(buttons, 3)
        layout = [[sg.Column([column])] for column in cols]
        return layout
    
    def generate_report_layout(self, violation_record):
        # NOTE We still have to figure out a format for the violation record
        layout = [
                    [sg.Text("Traffic Violation Details", size=(30, 1), font=("Helvetica", 25), justification="center")],
                    [sg.HorizontalSeparator()],
                    [sg.Text("Violation Date:", size=(15, 1)), sg.Text(violation_record[1][0], size=(20, 1))],
                    [sg.Text("Vehicle ID:", size=(15, 1)), sg.Text(violation_record[2][0], size=(40, 1))],
                    [sg.Text("Violation Type:", size=(15, 1)), sg.Text(violation_record[3][0], size=(20, 1))],
                    [sg.Text("Speed (km/h):", size=(15, 1)), sg.Text(violation_record[6][0], size=(20, 1))],
                    [sg.HorizontalSeparator()],
                    [sg.Text("Vehicle Picture:", size=(15, 1)), sg.Image(filename=violation_record[4][0], key="VehicleImage")],
                    [sg.HorizontalSeparator()],
                    [sg.Text("Scene Picture:", size=(15, 1)), sg.Image(filename=violation_record[5][0], key="SceneImage", size=(200, 100))],
                    [sg.Button("View Full Size", key="ViewSceneImage")],
                    [sg.HorizontalSeparator()],
                    [sg.Button("Back"), sg.Button("Print")],
                ]
        window = sg.Window("Violation Report", layout, finalize=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Back":
                break
            if event == "ViewVehicleImage":
                cv2.imshow("Vehicle Image", cv2.imread(violation_record[4][0]))
            if event == "ViewSceneImage":
                cv2.imshow("Scene Image", cv2.imread(violation_record[5][0]))
            if event == "Print":
                self.print_report(violation_record)
        window.close()
    # Event loop to handle button clicks and display video streams
    def event_loop(self):
        window = sg.Window("Traffic Watch", self.layout, finalize=True)
        window.Maximize()
        # Event loop to handle button clicks and display video streams
        while True:
            event, _ = window.read(timeout=2)
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