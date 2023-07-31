# This Method uses YOLOv8 for Object Detection

import cv2
from ultralytics import YOLO
import line_counter as lc
import supervision as sv
import numpy as np
import time


# LINE_START = sv.Point(320, 0)
# LINE_END = sv.Point(320, 480)

LINE_START = sv.Point(0, 200)
LINE_END = sv.Point(1280, 220)


def main():
    line_counter = lc.LineZone(start=LINE_START, end=LINE_END)
    line_annotator = lc.LineZoneAnnotator(thickness=2, text_thickness=1, text_scale=0.5)
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5
    )
    times = []

    model = YOLO("yolov8n.pt")
    start_time = time.time()
    # TODO: classes 2,3,5,7 überprüfen (sollten Auto, Bus, Truck sein)
    for result in model.track(source="../../video_examples/HCPS Beispiel2.mp4", verbose=False, show=False, stream=True, agnostic_nms=True, vid_stride=5, classes=[2, 3, 5, 7]):
        frame = result.orig_img
        detections = sv.Detections.from_yolov8(result)

        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

        # detections = detections[(detections.class_id != 60) & (detections.class_id != 0)]

        labels = [
            f"{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, tracker_id
            in detections
        ]

        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )

        line_counter.trigger(detections=detections)
        line_annotator.annotate(frame=frame, line_counter=line_counter)

        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            break

        print(line_counter.current_cars)

        end_time = time.time()
        times.append(end_time - start_time)
        start_time = time.time()

    with open('../../../demo/test_times/frame_times_method_3.txt', 'w') as file:
        for time_val in times:
            file.write(str(time_val) + '\n')


if __name__ == "__main__":
    main()
