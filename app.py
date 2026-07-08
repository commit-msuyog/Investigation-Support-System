import os
import cv2
import time
from ultralytics import YOLO

import face_recognition

# Load YOLO model
model = YOLO("models\yolov8n.pt")

# Pre-trained Model for Face-Detection
#face_cascade = cv2.CascadeClassifier(
#    "models/haarcascade_frontalface_default.xml"
#)



known_encodings = []
known_names = []

image1 = face_recognition.load_image_file(
    "known_faces/suyog.jpeg"
)

encoding1 = face_recognition.face_encodings(image1)[0]

known_encodings.append(encoding1)

known_names.append("Suyog")



image2 = face_recognition.load_image_file(
    "known_faces/shruti.jpeg"
)

encoding2 = face_recognition.face_encodings(image2)[0]

known_encodings.append(encoding2)

known_names.append("Shruti")



# Open webcam
cap = cv2.VideoCapture(0)



# Screenshot Folder (Creates if Not present)
if not os.path.exists("detections"):
    os.makedirs("detections")
first_seen = {}
saved_ids = set()


frame_count = 0

while True:

    
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    frame_count = frame_count + 1

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #if frame_count % 5 == 0:
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #cv2.imshow("RGB Frame", rgb_frame)
    #print(rgb_frame.shape)
    face_locations = face_recognition.face_locations(
        rgb_frame,
        model="hog"
    )
    #print(f"Faces detected: {len(face_locations)}")

    face_encodings = face_recognition.face_encodings(
        rgb_frame,
        face_locations
    )


    for (top, right, bottom, left), face_encoding in zip(
        face_locations,
        face_encodings
    ):
    
        matches = face_recognition.compare_faces(
        known_encodings,
        face_encoding
        )

        name = "Unknown"
        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (255, 0, 255),
            2
        )
        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 255),
            2
        )
            #print(name)
    
    results = model.track(frame, classes=[0], persist = True, verbose=False)

    person_count = 0

    for box in results[0].boxes:

        confidence = box.conf[0]

        if confidence > 0.5:

            if box.id is None or len(box.id) == 0:
                continue
            track_id = int(box.id[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

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
                person_crop = frame[y1:y2, x1:x2]
                cv2.imwrite(filename, person_crop)

                saved_ids.add(track_id) # Save id

                print(f"Saved: {filename}")

            

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