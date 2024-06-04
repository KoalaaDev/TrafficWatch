from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO("custom.pt")

# Run inference on 'bus.jpg' with arguments
model.predict("bc087f8b-fbd5-4c1b-a4e3-d5d3579c09c1.png", save=True, imgsz=640, conf=0.5)