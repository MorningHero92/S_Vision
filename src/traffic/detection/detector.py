# Detection only - used to evaluate different YOLO models on different video sources to find best speed/quality ratio

import cv2
from ultralytics import YOLO


def run_prediction(
    model_path,
    video_path,
    output_path,
    tracker_yaml,
    **kwargs
):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (
            width,
            height,
        ),
    )

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(
            frame,
            **kwargs
        )

        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()
