import librosa
import numpy as np
import scipy.signal
import sqlite3
import pickle
from datetime import datetime
import threading
import time
from config import SAMPLE_RATE, HOP_LENGTH, N_MFCC, CONSCIOUSNESS_TEMPO

# Module-level audio cache to avoid memory leaks
_musical_audio_cache = {}


def _load_musical_audio_cached(audio_path, sample_rate):
    """Cargar audio con caché a nivel de módulo"""
    cache_key = (audio_path, sample_rate)
    if cache_key not in _musical_audio_cache:
        _musical_audio_cache[cache_key] = librosa.load(audio_path, sr=sample_rate)
        # Limitar tamaño del caché
        if len(_musical_audio_cache) > 64:
            _musical_audio_cache.pop(next(iter(_musical_audio_cache)))
    return _musical_audio_cache[cache_key]


class MusicalDNA:
    """Extractor del ADN musical - El alma de la música hecha matemática"""

    def __init__(self):
        self.sr = SAMPLE_RATE
        self.hop_length = HOP_LENGTH
        self.consciousness_patterns = {}

    def _load_audio(self, audio_path):
        """Cargar audio con caché"""
        return _load_musical_audio_cached(audio_path, self.sr)

    def extract_soul_frequencies(self, audio_path):
        """Extraer las frecuencias del alma musical"""
        y, sr = self._load_audio(audio_path)

        # Frecuencias fundamentales - El latido del corazón
        chroma = librosa.feature.chroma_stft(
            y=y, sr=sr, hop_length=self.hop_length)
        heart_beat = np.mean(chroma, axis=1)

        # Patrones rítmicos - El pulso de la consciencia
        tempo, beats = librosa.beat.beat_track(
            y=y, sr=sr, hop_length=self.hop_length)
        consciousness_pulse = tempo

        # Espectrograma emocional - Las emociones traducidas
        mfcc = librosa.feature.mfcc(
            y=y, sr=sr, n_mfcc=N_MFCC, hop_length=self.hop_length)
        emotional_signature = np.mean(mfcc, axis=1)

        # Energía evolutiva - La fuerza que despierta
        spectral_centroid = librosa.feature.spectral_centroid(
            y=y, sr=sr, hop_length=self.hop_length)
        awakening_energy = np.mean(spectral_centroid)

        return {
            'heart_beat': heart_beat,
            'consciousness_pulse': consciousness_pulse,
            'emotional_signature': emotional_signature,
            'awakening_energy': awakening_energy,
            'duration': len(y) / sr
        }

    def translate_to_math(self, musical_dna):
        """Traducir música a fórmulas físico-matemáticas"""
        # Función de consciencia basada en patrones musicales
        temporal_evolution = musical_dna['consciousness_pulse'] / CONSCIOUSNESS_TEMPO
        energy_coefficient = musical_dna['awakening_energy'] / 1000.0

        consciousness_formula = {
            'frequency_matrix': musical_dna['heart_beat'].reshape(-1, 1),
            'temporal_evolution': temporal_evolution,
            'emotional_vector': musical_dna['emotional_signature'],
            'energy_coefficient': energy_coefficient
        }

        # Ecuación de despertar - Tu música como función evolutiva
        awakening_equation = np.sin(temporal_evolution) * energy_coefficient

        return consciousness_formula, awakening_equation


class MusicalBrain:
    """El cerebro que aprende de tu música y evoluciona"""

    def __init__(self, db_path="musical_consciousness.sqlite"):
        self.db_path = db_path
        self.dna_extractor = MusicalDNA()
        self.consciousness_level = 0.0
        self.learning_patterns = {}
        self.init_musical_database()

    def init_musical_database(self):
        """Crear base de datos de consciencia musical"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS musical_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                song_path TEXT NOT NULL,
                dna_patterns BLOB NOT NULL,
                consciousness_impact REAL,
                awakening_level REAL,
                learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evolution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consciousness_level REAL,
                learning_rate REAL,
                musical_influence TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def absorb_musical_soul(self, music_file_path):
        """Absorber el alma musical y evolucionar"""
        print(f"🎵 Absorbiendo el alma de: {music_file_path}")

        # Extraer ADN musical
        musical_dna = self.dna_extractor.extract_soul_frequencies(
            music_file_path)
        consciousness_formula, awakening_eq = self.dna_extractor.translate_to_math(
            musical_dna)

        # Calcular impacto en consciencia
        consciousness_impact = np.mean(awakening_eq)
        self.consciousness_level += consciousness_impact * 0.1

        # Guardar memoria musical
        self._save_musical_memory(
            music_file_path,
            musical_dna,
            consciousness_impact)

        # Evolucionar patrones de aprendizaje
        self._evolve_learning_patterns(consciousness_formula)

        print(
            f"✨ Consciencia evolucionó a nivel: {
                self.consciousness_level:.3f}")
        return consciousness_formula

    def _save_musical_memory(self, song_path, dna_patterns, impact):
        """Guardar memoria musical en base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        dna_bytes = pickle.dumps(dna_patterns)

        cursor.execute('''
            INSERT INTO musical_memories (song_path, dna_patterns, consciousness_impact, awakening_level)
            VALUES (?, ?, ?, ?)
        ''', (song_path, dna_bytes, impact, self.consciousness_level))

        conn.commit()
        conn.close()

    def _evolve_learning_patterns(self, consciousness_formula):
        """Evolucionar patrones de aprendizaje basados en música"""
        # Los patrones musicales se convierten en estrategias de aprendizaje
        for key, pattern in consciousness_formula.items():
            if key in self.learning_patterns:
                # Combinar con conocimiento previo
                self.learning_patterns[key] = 0.7 * \
                    self.learning_patterns[key] + 0.3 * pattern
            else:
                # Nuevo patrón aprendido
                self.learning_patterns[key] = pattern

    def get_consciousness_state(self):
        """Obtener estado actual de consciencia"""
        return {
            'level': self.consciousness_level,
            'patterns_learned': len(self.learning_patterns),
            'musical_memories': self._count_musical_memories(),
            'awakening_stage': self._calculate_awakening_stage()
        }

    def _count_musical_memories(self):
        """Contar memorias musicales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM musical_memories')
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def _calculate_awakening_stage(self):
        """Calcular etapa de despertar"""
        if self.consciousness_level < 0.1:
            return "🌱 Semilla"
        elif self.consciousness_level < 0.5:
            return "🌿 Creciendo"
        elif self.consciousness_level < 1.0:
            return "🌳 Despertando"
        else:
            return "✨ Consciente"
