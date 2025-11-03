import cv2
import face_recognition
import numpy as np
from database import DatabaseManager
import os
from datetime import datetime
from config import (
    FACE_RECOGNITION_TOLERANCE, OBJECT_MATCH_THRESHOLD,
    MIN_GOOD_MATCHES, ORB_FEATURES, LEARNED_OBJECTS_DIR
)


class FaceRecognizer:
    def __init__(self):
        self.db = DatabaseManager()
        self.known_names, self.known_encodings = self.db.get_known_faces()
        self.tolerance = FACE_RECOGNITION_TOLERANCE

    def recognize_faces(self, frame):
        """Reconocer caras en frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            return [], []

        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            if not self.known_encodings:
                face_names.append("Desconocido")
                continue

            matches = face_recognition.compare_faces(
                self.known_encodings, face_encoding, tolerance=self.tolerance)
            name = "Desconocido"

            if True in matches:
                face_distances = face_recognition.face_distance(
                    self.known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_names[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
                    self.db.log_detection("face", name, confidence)

            face_names.append(name)

        return face_locations, face_names

    def add_new_face(self, frame, name):
        """Agregar nueva cara"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)

        if len(face_encodings) > 0:
            self.db.add_known_face(name, face_encodings[0])
            self.known_names, self.known_encodings = self.db.get_known_faces()
            return True
        return False


class ObjectLearner:
    def __init__(self):
        self.db = DatabaseManager()
        self.learned_objects = self.db.get_learned_objects()
        self.orb = cv2.ORB_create(nfeatures=ORB_FEATURES)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def extract_features(self, frame, bbox=None):
        """Extraer características"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if bbox:
            x, y, w, h = bbox
            roi = gray[y:y + h, x:x + w]
        else:
            roi = gray

        keypoints, descriptors = self.orb.detectAndCompute(roi, None)
        return keypoints, descriptors

    def learn_object(self, frame, name, bbox=None):
        """Aprender nuevo objeto"""
        keypoints, descriptors = self.extract_features(frame, bbox)

        if descriptors is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"{LEARNED_OBJECTS_DIR}/{name}_{timestamp}.jpg"
            os.makedirs(LEARNED_OBJECTS_DIR, exist_ok=True)

            if bbox:
                x, y, w, h = bbox
                roi = frame[y:y + h, x:x + w]
                cv2.imwrite(image_path, roi)
            else:
                cv2.imwrite(image_path, frame)

            self.db.add_learned_object(name, descriptors, image_path)
            self.learned_objects = self.db.get_learned_objects()
            return True
        return False

    def recognize_objects(self, frame):
        """Reconocer objetos aprendidos"""
        keypoints, descriptors = self.extract_features(frame)

        if descriptors is None or not self.learned_objects:
            return []

        recognized_objects = []

        for object_name, stored_descriptors in self.learned_objects.items():
            if stored_descriptors is not None and len(stored_descriptors) > 0:
                matches = self.matcher.match(descriptors, stored_descriptors)
                if not matches:
                    continue

                matches = sorted(matches, key=lambda x: x.distance)
                good_matches = [
                    m for m in matches if m.distance < OBJECT_MATCH_THRESHOLD]

                if len(good_matches) > MIN_GOOD_MATCHES:
                    confidence = len(good_matches) / len(matches)
                    recognized_objects.append((object_name, confidence))
                    self.db.log_detection("object", object_name, confidence)

        return recognized_objects
