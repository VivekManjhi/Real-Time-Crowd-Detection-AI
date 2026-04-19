import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def get_crowd_data():
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return {"gate1": 0, "gate2": 0, "gate3": 0, "gate4": 0}

    results = model(frame, verbose=False)

    count = 0

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                count += 1

    # simulate 4 gates split
    return {
        "gate1": count // 4,
        "gate2": count // 4,
        "gate3": count // 4,
        "gate4": count - (count // 4 * 3)
    }