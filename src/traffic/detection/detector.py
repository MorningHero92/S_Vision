# src/traffic/detection/detector.py
from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="yolo26m.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame, conf=0.25, classes=[2, 3, 5, 7])
        results = self.model.predict(frame, conf=conf, classes=classes)
        return results
