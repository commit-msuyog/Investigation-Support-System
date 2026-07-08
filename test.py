import face_recognition

image = face_recognition.load_image_file("known_faces/suyog.jpeg")

locations = face_recognition.face_locations(image)

print(locations)