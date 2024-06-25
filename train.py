from ultralytics import YOLO

# Load a model
if __name__ == '__main__':
    model = YOLO("yolov8m.pt")  # load a pretrained model (recommended for training)


    # Train the model
    results = model.train(data="data.yaml", epochs=100, imgsz=640, batch=-1, cache=True)