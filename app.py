import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Check if frame captured correctly
    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Investigation Support System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()