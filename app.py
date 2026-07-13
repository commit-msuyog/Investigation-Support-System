import os
import cv2
import time
from ultralytics import YOLO
import face_recognition

from database import save_detection

# Load YOLO model with GPU
model = YOLO("models\yolov8n.pt")
model.to("cuda")




known_encodings = []
known_names = []

# Manually Uploading 

known_faces_folder = "known_faces"

face_images = os.listdir(known_faces_folder)

for image_name in face_images:
    if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    
    image_path = os.path.join(
    known_faces_folder,
    image_name
)

    image = face_recognition.load_image_file(image_path)

    encodings = face_recognition.face_encodings(image)
    known_encodings.append(encodings[0])

    name = os.path.splitext(image_name)[0]
    known_names.append(name)

    if len(encodings) == 0:
        print(f"No face found in {image_name}")
        continue


# Open webcam
cap = cv2.VideoCapture(0)


# Screenshot Folder (Creates if Not present)
if not os.path.exists("detections"):
    os.makedirs("detections")

first_seen = {}
saved_ids = set()
recognized_tracks = {} 


while True:

    
    start_time = time.time()
    ret, frame = cap.read()

    # Remove it if need for CCTV (dont flip it)
    frame = cv2.flip(frame, 1)
    
    if not ret:
        print("Failed to capture frame")
        break


    
    
    results = model.track(
        frame,
        classes=[0],
        persist=True,
        verbose=False
    )

    person_count = 0
    for box in results[0].boxes:

        confidence = float(box.conf[0])

        if confidence <= 0.5:
            continue

        if box.id is None:
            continue

        track_id = int(box.id[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        person_count += 1

        # Face Recognition (only once)
        
        if track_id not in recognized_tracks:

            person_crop = frame[y1:y2, x1:x2]

            rgb_crop = cv2.cvtColor(
                person_crop,
                cv2.COLOR_BGR2RGB
            )

            face_locations = face_recognition.face_locations(
                rgb_crop,
                model="hog"
            )

            if len(face_locations) > 0:

                face_encodings = face_recognition.face_encodings(
                    rgb_crop,
                    face_locations
                )

                matches = face_recognition.compare_faces(
                    known_encodings,
                    face_encodings[0]
                )

                name = "Unknown"

                if True in matches:
                    match_index = matches.index(True)
                    name = known_names[match_index]

                recognized_tracks[track_id] = {
                    "name": name,
                    "face": face_locations[0]
                }

                print(f"Track {track_id}: {name}")

       
        # Draw Person Box
       
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"ID:{track_id} | {confidence:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )


        # Draw Face Box (cached)

        if track_id in recognized_tracks:

            info = recognized_tracks[track_id]

            name = info["name"]

            top, right, bottom, left = info["face"]

            cv2.rectangle(
                frame,
                (x1 + left, y1 + top),
                (x1 + right, y1 + bottom),
                (255,0,255),
                2
            )

            cv2.putText(
                frame,
                name,
                (x1 + left, y1 + top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,0,255),
                2
            )

        # Save Screenshot with timestamp

        current_time = time.time()

        if track_id not in first_seen:
            first_seen[track_id] = current_time

        if (
            current_time - first_seen[track_id] >= 2
            and track_id not in saved_ids
        ):
            file_timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"detections/person_{track_id}_{file_timestamp}.jpg"


            detect_time = time.strftime('%Y%m%d_%H%M%S')

            cv2.imwrite(
                filename,
                frame[y1:y2, x1:x2]
            )
            if track_id in recognized_tracks:
                detected_name = recognized_tracks[track_id]["name"]
            else:
                detected_name = "Unknown"

            save_detection(
                track_id=track_id,
                name=detected_name,
                confidence=float(confidence),
                image_path=filename,
                detected_time=detect_time
            )
            

            saved_ids.add(track_id)

            print("Saved:", filename)


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