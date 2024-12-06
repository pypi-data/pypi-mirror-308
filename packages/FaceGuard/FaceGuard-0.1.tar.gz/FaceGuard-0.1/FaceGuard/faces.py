# FaceGuard/faces.py
import os
import cv2

class FaceManager:
    def __init__(self, faces_dir="faces"):
        self.faces_dir = faces_dir
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)

    def add_face(self, name):
        """
        Fügt ein neues Gesicht hinzu, indem ein Bild von der Kamera aufgenommen und gespeichert wird.
        :param name: Der Name der Person, der dem Gesicht zugeordnet wird.
        :return: bool - Erfolg des Vorgangs.
        """
        # Webcam initialisieren und Bild aufnehmen
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print("Kamera konnte nicht geöffnet werden.")
            return False

        ret, frame = video_capture.read()
        video_capture.release()

        if not ret:
            print("Bildaufnahme fehlgeschlagen.")
            return False

        # Bild speichern
        face_path = os.path.join(self.faces_dir, f"{name}.png")
        cv2.imwrite(face_path, frame)
        print(f"Gesicht für {name} erfolgreich hinzugefügt.")
        return True

    def delete_face(self, name):
        """
        Löscht ein vorhandenes Gesicht basierend auf dem angegebenen Namen.
        :param name: Der Name der Person, deren Bild gelöscht werden soll.
        :return: bool - Erfolg des Vorgangs.
        """
        face_path = os.path.join(self.faces_dir, f"{name}.png")
        if os.path.exists(face_path):
            os.remove(face_path)
            print(f"Gesicht für {name} erfolgreich gelöscht.")
            return True
        else:
            print(f"Kein Gesicht für {name} gefunden.")
            return False

    def list_faces(self):
        """
        Gibt eine Liste aller gespeicherten Gesichter zurück.
        :return: Liste der Namen von gespeicherten Gesichtern.
        """
        return [f.split(".")[0] for f in os.listdir(self.faces_dir) if f.endswith(".png")]