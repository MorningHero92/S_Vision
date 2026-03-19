import cv2
from traffic.detection.detector import Detector
from traffic.tracking.tracker import Tracker

class Pipeline:
    def __init__(self, video_path, output_path, tracker_yaml=None):
        self.video_path = video_path
        print(video_path)
        self.output_path = output_path
        self.detector = Detector()
        self.tracker = Tracker(tracker_yaml)

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # --- Детекция ---
            det_results = self.detector.detect(frame)

            # --- Трекинг ---
            track_results = self.tracker.track(frame, det_results)

            # --- Аннотированный кадр ---
            annotated_frame = track_results[0].plot()
            out.write(annotated_frame)

        cap.release()
        out.release()
        print("Готово:", self.output_path)
