import os
import cv2
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Screenshot Folder (Creates if Not present)
if not os.path.exists("detections"):
    os.makedirs("detections")
first_seen = {}
saved_ids = set()

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
            
            # Appear hone ke 2 sec baad click karega !! 
            current_time = time.time()
            if track_id not in first_seen:
                first_seen[track_id] = current_time
            
            # Ye Image ko save karega ID ko check krke !! 
            if (current_time - first_seen[track_id] >= 2
                and track_id not in saved_ids):
                timestamp = time.strftime("%Y%m%d_%H%M%S")

                filename = f"detections/person_{track_id}_{timestamp}.jpg"

                cv2.imwrite(filename, frame)

                saved_ids.add(track_id) # Save id

                print(f"Saved: {filename}")

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