import cv2
from detection.detector import Detector

class Pipeline:
    def __init__(self, video_path, output_path, tracker_yaml=None):
        self.video_path = video_path
        print(video_path)
        self.output_path = output_path
        self.detector = Detector()

    def run(self, **kwargs):
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

            results = self.detector.track(frame, tracker=self.tracker_yaml, **kwargs)

            annotated_frame = results[0].plot()
            out.write(annotated_frame)

        cap.release()
        out.release()
        print("Готово:", self.output_path)
