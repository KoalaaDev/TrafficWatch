from ultralytics import YOLO
if __name__ == "__main__":
    # Load the model
    model = YOLO("yolov8m.pt")  # build from YAML and transfer weights

    # Train the model
    results = model.train(data="data.yaml", epochs=100, imgsz=640)