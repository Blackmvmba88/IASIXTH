import cv2
import face_recognition
import mediapipe as mp
import numpy as np
from database import DatabaseManager
import os
from datetime import datetime


class FaceRecognizer:
    def __init__(self):
        self.db = DatabaseManager()
        self.known_names, self.known_encodings = self.db.get_known_faces()

    def recognize_faces(self, frame):
        """Reconocer caras en un frame"""
        # Convertir BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Encontrar ubicaciones y encodings de caras
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_encodings, face_encoding)
            name = "Desconocido"

            if True in matches:
                # Encontrar la mejor coincidencia
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
        """Agregar una nueva cara a la base de datos"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)

        if len(face_encodings) > 0:
            self.db.add_known_face(name, face_encodings[0])
            # Recargar las caras conocidas
            self.known_names, self.known_encodings = self.db.get_known_faces()
            return True
        return False


class PersonDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.db = DatabaseManager()

    def detect_person(self, frame):
        """Detectar personas usando MediaPipe"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        person_detected = False
        if results.pose_landmarks:
            person_detected = True
            self.db.log_detection("person", "persona_detectada", 0.9)

            # Dibujar landmarks de la pose
            self.mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return frame, person_detected


class ObjectLearner:
    def __init__(self):
        self.db = DatabaseManager()
        self.learned_objects = self.db.get_learned_objects()

        # Inicializar detector de características
        self.orb = cv2.ORB_create(nfeatures=1000)

    def extract_features(self, frame, bbox=None):
        """Extraer características de un objeto en el frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if bbox:
            x, y, w, h = bbox
            roi = gray[y:y + h, x:x + w]
        else:
            roi = gray

        keypoints, descriptors = self.orb.detectAndCompute(roi, None)
        return keypoints, descriptors

    def learn_object(self, frame, name, bbox=None):
        """Aprender un nuevo objeto"""
        keypoints, descriptors = self.extract_features(frame, bbox)

        if descriptors is not None:
            # Guardar imagen de referencia
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"learned_objects/{name}_{timestamp}.jpg"
            os.makedirs("learned_objects", exist_ok=True)

            if bbox:
                x, y, w, h = bbox
                roi = frame[y:y + h, x:x + w]
                cv2.imwrite(image_path, roi)
            else:
                cv2.imwrite(image_path, frame)

            # Guardar características en la base de datos
            self.db.add_learned_object(name, descriptors, image_path)
            self.learned_objects = self.db.get_learned_objects()
            return True
        return False

    def recognize_objects(self, frame):
        """Reconocer objetos aprendidos en el frame"""
        keypoints, descriptors = self.extract_features(frame)

        if descriptors is None:
            return []

        recognized_objects = []
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        for object_name, stored_descriptors in self.learned_objects.items():
            if stored_descriptors is not None:
                matches = matcher.match(descriptors, stored_descriptors)
                matches = sorted(matches, key=lambda x: x.distance)

                # Si hay suficientes matches buenos, considerarlo reconocido
                good_matches = [m for m in matches if m.distance < 50]
                if len(good_matches) > 10:
                    confidence = len(good_matches) / len(matches)
                    recognized_objects.append((object_name, confidence))
                    self.db.log_detection("object", object_name, confidence)

        return recognized_objects
