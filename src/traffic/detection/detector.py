from ultralytics import YOLO

class Detector:
    def __init__(self):
        self.model = YOLO("yolo26m.pt")

    def track(self, frame, **kwargs):
        return self.model.track(frame, tracker="none", **kwargs)
