import cv2
import PySimpleGUI as sg

# List of stream URLs
stream_urls = [
    "https://trafficwatchcdn.myt.mu/harbour/caudan.stream/playlist.m3u8",
    "https://trafficwatchcdn.myt.mu/harbour/plsouth.stream/playlist.m3u8",
    "https://trafficwatch6.myt.mu/plbyn/pdarmes.stream/playlist.m3u8",
    "https://trafficwatch6.myt.mu/plbyn/lbps2.stream/playlist.m3u8",
    "https://trafficwatch6.myt.mu/ebene/ebenemotorway.stream/playlist.m3u8",
    "https://trafficwatch6.myt.mu/reduit/tamilleague.stream/playlist.m3u8",
    "https://trafficwatch6.myt.mu/terrerouge/terrerougeexch.stream/playlist.m3u8",
    "https://trafficwatch6.myt.mu/curepipe/CurepipeSuisse.stream/playlist.m3u8"
]

# Initialize variables
current_stream_index = 0
num_streams = len(stream_urls)

# Create layout for the GUI
layout = [
    [sg.Button("Settings"), sg.Button("Add Stream"), sg.Button("Remove Stream")],
    [sg.Button(image_filename="icons/left.png", key="Previous"), sg.Image(filename="", key="-IMAGE-"), sg.Button(image_filename="icons/right.png", key="Next"),], 
    [sg.Button("Exit")]
]

# Create the window
window = sg.Window("CCTV Viewer", layout, finalize=True)

# Create video capture object for the first stream
cap = cv2.VideoCapture(stream_urls[current_stream_index])

# Event loop to handle button clicks and display video streams
while True:
    event, values = window.read(timeout=5)

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    # Switch to the next stream if 'Next' button is pressed
    if event == "Next":
        current_stream_index = (current_stream_index + 1) % num_streams
        cap.release()
        cap = cv2.VideoCapture(stream_urls[current_stream_index])

    # Switch to the previous stream if 'Previous' button is pressed
    elif event == "Previous":
        current_stream_index = (current_stream_index - 1) % num_streams
        cap.release()
        cap = cv2.VideoCapture(stream_urls[current_stream_index])
    
    elif event == "Add Stream":
        new_stream_url = sg.popup_get_text("Enter stream URL:")
        if new_stream_url:
            stream_urls.append(new_stream_url)
            num_streams += 1
        current_stream_index = num_streams - 1
        cap.release()
        cap = cv2.VideoCapture(stream_urls[current_stream_index])
    
    elif event == "Remove Stream":
        if num_streams > 1:
            stream_urls.pop(current_stream_index)
            num_streams -= 1
            current_stream_index = 0
            cap.release()
            cap = cv2.VideoCapture(stream_urls[current_stream_index])
        else:
            sg.popup("Cannot remove the last stream!")
    
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to format PySimpleGUI can display
    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
    window["-IMAGE-"].update(data=imgbytes)

window.close()
cap.release()
cv2.destroyAllWindows()
