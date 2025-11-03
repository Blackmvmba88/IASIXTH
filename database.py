import sqlite3
import pickle


class DatabaseManager:
    def __init__(self, db_path="recognition_db.sqlite"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar la base de datos con las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
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
        
        conn.commit()
        conn.close()
    
    def add_known_face(self, name, face_encoding):
        """Agregar una cara conocida a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convertir el encoding a bytes para guardarlo
        encoding_bytes = pickle.dumps(face_encoding)
        
        cursor.execute('''
            INSERT INTO known_faces (name, encoding)
            VALUES (?, ?)
        ''', (name, encoding_bytes))
        
        conn.commit()
        conn.close()
        print(f"Cara de {name} agregada a la base de datos")
    
    def get_known_faces(self):
        """Obtener todas las caras conocidas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, encoding FROM known_faces')
        results = cursor.fetchall()
        
        known_names = []
        known_encodings = []
        
        for name, encoding_bytes in results:
            encoding = pickle.loads(encoding_bytes)
            known_names.append(name)
            known_encodings.append(encoding)
        
        conn.close()
        return known_names, known_encodings
    
    def add_learned_object(self, name, features, image_path=None):
        """Agregar un objeto aprendido a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        features_bytes = pickle.dumps(features)
        
        cursor.execute('''
            INSERT INTO learned_objects (name, features, image_path)
            VALUES (?, ?, ?)
        ''', (name, features_bytes, image_path))
        
        conn.commit()
        conn.close()
        print(f"Objeto '{name}' agregado a la base de datos")
    
    def get_learned_objects(self):
        """Obtener todos los objetos aprendidos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, features FROM learned_objects')
        results = cursor.fetchall()
        
        objects = {}
        for name, features_bytes in results:
            features = pickle.loads(features_bytes)
            objects[name] = features
        
        conn.close()
        return objects
    
    def log_detection(self, object_type, object_name, confidence):
        """Registrar una detección en el historial"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO detection_history
            (object_type, object_name, confidence)
            VALUES (?, ?, ?)
        ''', (object_type, object_name, confidence))
        
        conn.commit()
        conn.close()
