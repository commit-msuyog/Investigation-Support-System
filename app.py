import os
import cv2
import time
from ultralytics import YOLO
import face_recognition

from database import save_detection
from identity import IdentityManager

FACE_EVERY_N_FRAMES = 5    # try face recognition every 5th frame
MIN_FACE_SIZE = 40         # ignore faces smaller than 40 px
MIN_VISIBLE_SEC = 2        # person must be visible 2 sec before logging
REENTRY_GAP_SEC = 300      # gone for 5 min, then back = logged again (same ID)
DEBUG = True               # prints why face was not found (make False when working)

# Load YOLO model with GPU
model = YOLO("models/yolov8n.pt")
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

    # skip the image if no face found (check before using encodings[0])
    if len(encodings) == 0:
        print(f"No face found in {image_name}")
        continue

    known_encodings.append(encodings[0])

    name = os.path.splitext(image_name)[0]
    known_names.append(name)


# Permanent ID maker (track id -> person id)
ids = IdentityManager(known_names, known_encodings)
print(f"[identity] ready with {len(known_names)} known face(s)")


# Open webcam
cap = cv2.VideoCapture(0)


# Screenshot Folder (Creates if Not present)
if not os.path.exists("detections"):
    os.makedirs("detections")

face_boxes = {}          # track_id -> face position (for pink box)
last_seen_person = {}    # person_id -> last time we saw him
visit_start = {}         # person_id -> when his current visit started
visit_logged = set()     # person_ids already saved in current visit
frame_count = 0


def find_face(frame, x1, y1, x2, y2):

    crop = frame[y1:y2, x1:x2]

    if crop.size == 0:
        return None

    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(
        rgb,
        model="hog"
    )

    if len(locations) == 0:
        if DEBUG:
            print(f"[debug] no face found in person box {x2 - x1}x{y2 - y1}")
        return None

    top, right, bottom, left = locations[0]

    # too small face = bad fingerprint, skip it
    if (bottom - top) < MIN_FACE_SIZE or (right - left) < MIN_FACE_SIZE:
        if DEBUG:
            print(f"[debug] face too small: {right - left}x{bottom - top} px")
        return None

    encodings = face_recognition.face_encodings(
        rgb,
        [locations[0]]
    )

    if len(encodings) == 0:
        if DEBUG:
            print("[debug] face found but encoding failed")
        return None

    return locations[0], encodings[0]


while True:

    
    start_time = time.time()
    frame_count += 1

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Remove it if need for CCTV (dont flip it)
    frame = cv2.flip(frame, 1)

    frame_h, frame_w = frame.shape[:2]

    
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

        # keep box inside the frame
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(frame_w, x2), min(frame_h, y2)

        if x2 <= x1 or y2 <= y1:
            continue

        person_count += 1

        # Face Recognition (only until person is identified)

        person_id = ids.get_identity(track_id)

        if person_id is None and frame_count % FACE_EVERY_N_FRAMES == 0:

            found = find_face(frame, x1, y1, x2, y2)

            if found is not None:

                face_location, face_encoding = found

                person_id, is_known, is_new = ids.resolve(
                    track_id,
                    face_encoding
                )

                face_boxes[track_id] = face_location

                print(f"Track {track_id}: {person_id}")

       
        # Draw Person Box
       
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        label = f"Track {track_id} | {confidence:.2f}"

        if person_id is None:
            label += " | identifying..."

        cv2.putText(
            frame,
            label,
            (x1, max(15, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )


        # Draw Face Box (cached)

        if person_id is not None and track_id in face_boxes:

            top, right, bottom, left = face_boxes[track_id]

            cv2.rectangle(
                frame,
                (x1 + left, y1 + top),
                (x1 + right, y1 + bottom),
                (255,0,255),
                2
            )

            cv2.putText(
                frame,
                person_id,
                (x1 + left, max(15, y1 + top - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,0,255),
                2
            )

        # Save Screenshot with timestamp (once per visit of a person)

        if person_id is not None:

            current_time = time.time()

            previous = last_seen_person.get(person_id)
            last_seen_person[person_id] = current_time

            # new visit starts if never seen before or gone for long time
            if previous is None or current_time - previous >= REENTRY_GAP_SEC:
                visit_start[person_id] = current_time
                visit_logged.discard(person_id)

            if (
                current_time - visit_start[person_id] >= MIN_VISIBLE_SEC
                and person_id not in visit_logged
            ):
                file_timestamp = time.strftime('%Y%m%d_%H%M%S')
                filename = f"detections/person_{person_id}_{file_timestamp}.jpg"


                detect_time = time.strftime('%Y%m%d_%H%M%S')

                cv2.imwrite(
                    filename,
                    frame[y1:y2, x1:x2]
                )

                # unknown people are saved as "Unknown" so dashboard filter works
                if person_id in ids.known:
                    detected_name = person_id
                else:
                    detected_name = "Unknown"

                save_detection(
                    track_id=track_id,
                    name=detected_name,
                    confidence=float(confidence),
                    image_path=filename,
                    detected_time=detect_time,
                    person_id=person_id
                )
                

                visit_logged.add(person_id)

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