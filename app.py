import cv2
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    start_time = time.time()
    ret, frame = cap.read()
    

    if not ret:
        print("Failed to capture frame")
        break

    results = model.track(frame, classes=[0], persist = True, verbose=False)

    person_count = 0

    for box in results[0].boxes:

        confidence = box.conf[0]

        if confidence > 0.5:
            track_id = int(box.id[0])
            person_count = person_count + 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Cofidence score dikhyega 
            cv2.putText(
                frame,
                f"ID :{track_id}|{confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
    end_time = time.time()
    fps = 1/(end_time-start_time)

    # FPS show kr rha hai 
    cv2.putText(
        frame,
        f"FPS: {fps:.2f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # Person Count show kr rha hai 
    cv2.putText(
        frame,
        f"Persons Detected: {person_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.imshow("Investigation Support System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()