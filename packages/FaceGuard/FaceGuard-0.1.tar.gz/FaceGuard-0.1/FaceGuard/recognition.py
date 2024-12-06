import os
import sys
import cv2
import numpy as np
import face_recognition
import math



def face_confidence(face_distance, face_match_threshold=0.6):
    """Calculate the confidence based on the face distance."""
    range = (1.0 - face_match_threshold)
    linear_value = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_value * 100, 2)) + "%"
    else:
        value = (linear_value + ((1.0 - linear_value) * math.pow((linear_value - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + "%"


class FaceRecognition:
        
    def __init__(self, faces_dir="faces"):
        """Initialize the face recognition system and encode faces."""
        self.faces_dir = faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        
        self.encode_faces()

    def encode_faces(self):
        """Load and encode known faces from the specified directory."""
        files = 0
        for image in os.listdir(self.faces_dir):
            
            face_image = face_recognition.load_image_file(f"{self.faces_dir}/{image}")
            face_encoding = face_recognition.face_encodings(face_image, model="small")[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image.split(".")[0])
            files+= 1
        if files == 0:
            print("No faces in the selected directory!")
            sys.exit()


    def recognize_faces(self):
        """Perform face recognition in a video stream."""

        process_current_frame = True

        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            raise Exception("Video source not found...")

        while True:
            ret, frame = video_capture.read()

            if process_current_frame:
                small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Find faces in the current frame
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = "Unknown"

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    face_names.append(f"{name} ({confidence})")
            process_current_frame = not process_current_frame

            # Annotate the frame with rectangles and names
            for (top, right, bottom, left), name in zip(reversed(face_locations), reversed(face_names)):
                top *= 4
                bottom *= 4
                right *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) == ord("q"):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def login(self, required_confidence=85.0):
        """
        Capture a frame and check if any face matches a known face for login.
        :param required_confidence: The confidence threshold for successful login.
        :return: (bool, str) True if login is successful (recognized face), otherwise False; name of the recognized user.
        """
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            raise Exception("Video source not found...")

        ret, frame = video_capture.read()
        video_capture.release()

        if not ret:
            print("Failed to capture image.")
            return False, "No Image Captured"

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                confidence = float(face_confidence(face_distances[best_match_index]).replace("%", ""))

                if confidence >= required_confidence:
                    print(f"Login successful for {name} with confidence: {confidence}%")
                    return True, name
                else:
                    print(f"Recognition confidence for {name} is below the required threshold.")
                    return False, "Unknown or Low Confidence"

        return False, "Face Not Recognized"
