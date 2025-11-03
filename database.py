import sqlite3
import pickle
from contextlib import contextmanager
from config import DETECTION_HISTORY_LIMIT


class DatabaseManager:
    def __init__(self, db_path="recognition_db.sqlite"):
        self.db_path = db_path
        self._detection_count = 0  # Track insertions for batch cleanup
        self.init_database()

    @contextmanager
    def _get_connection(self):
        """Context manager para conexiones de base de datos"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_database(self):
        """Inicializar la base de datos con las tablas necesarias"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Tabla para personas conocidas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS known_faces (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    encoding BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabla para objetos aprendidos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learned_objects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    features BLOB NOT NULL,
                    image_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabla para historial de detecciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detection_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    object_type TEXT NOT NULL,
                    object_name TEXT,
                    confidence REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def add_known_face(self, name, face_encoding):
        """Agregar una cara conocida a la base de datos"""
        encoding_bytes = pickle.dumps(face_encoding)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO known_faces (name, encoding)
                VALUES (?, ?)
            ''', (name, encoding_bytes))

        print(f"Cara de {name} agregada a la base de datos")

    def get_known_faces(self):
        """Obtener todas las caras conocidas"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, encoding FROM known_faces')
            results = cursor.fetchall()

        known_names = []
        known_encodings = []

        for name, encoding_bytes in results:
            encoding = pickle.loads(encoding_bytes)
            known_names.append(name)
            known_encodings.append(encoding)

        return known_names, known_encodings

    def add_learned_object(self, name, features, image_path=None):
        """Agregar un objeto aprendido a la base de datos"""
        features_bytes = pickle.dumps(features)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learned_objects (name, features, image_path)
                VALUES (?, ?, ?)
            ''', (name, features_bytes, image_path))

        print(f"Objeto '{name}' agregado a la base de datos")

    def get_learned_objects(self):
        """Obtener todos los objetos aprendidos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, features FROM learned_objects')
            results = cursor.fetchall()

        objects = {}
        for name, features_bytes in results:
            features = pickle.loads(features_bytes)
            objects[name] = features

        return objects

    def log_detection(self, object_type, object_name, confidence):
        """Registrar una detección en el historial"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO detection_history
                (object_type, object_name, confidence)
                VALUES (?, ?, ?)
            ''', (object_type, object_name, confidence))

            # Incrementar contador y limpiar cada 100 inserciones (batch cleanup)
            self._detection_count += 1
            if self._detection_count >= 100:
                cursor.execute('''
                    DELETE FROM detection_history
                    WHERE id NOT IN (
                        SELECT id FROM detection_history
                        ORDER BY timestamp DESC
                        LIMIT ?
                    )
                ''', (DETECTION_HISTORY_LIMIT,))
                self._detection_count = 0
