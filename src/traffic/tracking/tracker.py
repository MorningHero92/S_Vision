# tracking.py

import cv2
from ultralytics import YOLO


def run_tracking(
    model_path,
    video_path,
    output_path,
    tracker_yaml,
    **kwargs
):
    model = YOLO(model_path)

    cap = cv2.VideoCapture(video_path)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        output_path,
        fourcc,
        cap.get(cv2.CAP_PROP_FPS),
        (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        ),
    )

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(
            frame,
            tracker=tracker_yaml
        )

        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()
