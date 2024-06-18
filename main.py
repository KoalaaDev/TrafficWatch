from ultralytics import YOLO
from UI import UI

model = YOLO("custom.pt")
colours = {
    "Vehicle": (0,0,255),
    "Pedestrian": (255,86,255),
    "Pedestrian-Crossing": (86, 255,255),
    "Traffic Light Red": (0,0,255),
    "Traffic-Light-Green": (0, 255, 0),
    "Traffic-Light-Orange": (0, 255, 255),
}

# List of stream URLs
stream_urls_dict = {
    "caudan": "https://trafficwatchcdn.myt.mu/harbour/caudan.stream/playlist.m3u8",
    "plsouth": "https://trafficwatchcdn.myt.mu/harbour/plsouth.stream/playlist.m3u8",
    "pdarmes": "https://trafficwatch6.myt.mu/plbyn/pdarmes.stream/playlist.m3u8",
    "lbps2": "https://trafficwatch6.myt.mu/plbyn/lbps2.stream/playlist.m3u8",
    "ebenemotorway": "https://trafficwatch6.myt.mu/ebene/ebenemotorway.stream/playlist.m3u8",
    "tamilleague": "https://trafficwatch6.myt.mu/reduit/tamilleague.stream/playlist.m3u8",
    "terrerougeexch": "https://trafficwatch6.myt.mu/terrerouge/terrerougeexch.stream/playlist.m3u8",
    "CurepipeSuisse": "https://trafficwatch6.myt.mu/curepipe/CurepipeSuisse.stream/playlist.m3u8"
}


ui = UI(stream_urls_dict, model, colours)
ui.event_loop()