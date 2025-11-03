import speech_recognition as sr
import threading
import json
from datetime import datetime
import queue
from config import (
    MAX_TRANSCRIPTIONS, AUDIO_TIMEOUT, PHRASE_TIME_LIMIT,
    MIC_CALIBRATION_DURATION, VOICE_LANGUAGE
)


class EarTrainingMode:
    def __init__(self):
        # Reconocimiento de voz
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Estados
        self.is_listening = False
        self.transcription_queue = queue.Queue(maxsize=MAX_TRANSCRIPTIONS)

        # Configuración de speakers
        self.known_voices = {}  # voz_id: {"name": str, "color": str}
        self.current_speaker = "yo"  # Speaker actual

        # Transcripciones en tiempo real
        self.live_transcriptions = []
        self.editing_mode = False

        # Calibrar micrófono
        self._calibrate_mic()

    def _calibrate_mic(self):
        """Calibrar micrófono para el entorno"""
        print("🎧 Calibrando micrófono para modo OÍDO...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(
                source, duration=MIC_CALIBRATION_DURATION)
        print("✅ Micrófono calibrado")

    def start_ear_training(self):
        """Iniciar modo de entrenamiento de oído"""
        print("👂 MODO OÍDO ACTIVADO")
        print("🔴 Grabando y transcribiendo todo...")
        print("📝 Presiona 'e' para editar transcripciones")

        self.is_listening = True

        # Hilo de escucha continua
        listen_thread = threading.Thread(target=self._continuous_listen)
        listen_thread.daemon = True
        listen_thread.start()

        # Hilo de procesamiento de transcripciones
        process_thread = threading.Thread(target=self._process_transcriptions)
        process_thread.daemon = True
        process_thread.start()

        return listen_thread, process_thread

    def _continuous_listen(self):
        """Escucha continua en background"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Escuchar fragmentos cortos para transcripción en tiempo real
                    audio = self.recognizer.listen(
                        source, timeout=AUDIO_TIMEOUT,
                        phrase_time_limit=PHRASE_TIME_LIMIT)

                # Procesar audio en hilo separado
                threading.Thread(
                    target=self._transcribe_audio,
                    args=(audio,),
                    daemon=True
                ).start()

            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"❌ Error en escucha: {e}")

    def _transcribe_audio(self, audio):
        """Transcribir audio a texto"""
        try:
            # Reconocimiento en español
            text = self.recognizer.recognize_google(audio, language=VOICE_LANGUAGE)

            # Detectar speaker (simplificado por ahora)
            speaker_id = self._identify_speaker(audio)

            # Crear transcripción
            transcription = {
                "text": text,
                "speaker": speaker_id,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "confidence": 0.85,  # Aproximación
                "editable": True,
                "audio_data": audio  # Para re-entrenamiento
            }

            self.transcription_queue.put(transcription)

        except sr.UnknownValueError:
            pass  # No se entendió el audio
        except sr.RequestError as e:
            print(f"❌ Error de reconocimiento: {e}")

    def _identify_speaker(self, audio):
        """Identificar quién está hablando (simplificado)"""
        # Por ahora retorna "yo" o "desconocido"
        # Aquí se podría implementar reconocimiento real
        return "yo" if len(
            self.live_transcriptions) % 2 == 0 else "otra_persona"

    def _process_transcriptions(self):
        """Procesar cola de transcripciones"""
        while self.is_listening:
            try:
                transcription = self.transcription_queue.get(timeout=0.1)
                self._display_transcription(transcription)
                self.live_transcriptions.append(transcription)

                # Limitar historial para evitar uso excesivo de memoria
                if len(self.live_transcriptions) > MAX_TRANSCRIPTIONS:
                    self.live_transcriptions = self.live_transcriptions[-MAX_TRANSCRIPTIONS:]

            except queue.Empty:
                continue

    def _display_transcription(self, transcription):
        """Mostrar transcripción con colores por speaker"""
        speaker = transcription["speaker"]
        text = transcription["text"]
        timestamp = transcription["timestamp"]

        # Colores por speaker
        colors = {
            "yo": "\033[92m",  # Verde
            "otra_persona": "\033[94m",  # Azul
            "desconocido": "\033[91m"  # Rojo
        }

        color = colors.get(speaker, "\033[90m")  # Gris por defecto
        reset = "\033[0m"

        # Mostrar con formato
        print(f"{color}[{timestamp}] {speaker.upper()}: {text}{reset}")

    def edit_last_transcription(self, new_text):
        """Editar la última transcripción"""
        if self.live_transcriptions:
            last_transcription = self.live_transcriptions[-1]
            old_text = last_transcription["text"]
            last_transcription["text"] = new_text
            last_transcription["edited"] = True

            print(f"✏️ EDITADO: '{old_text}' → '{new_text}'")
            return True
        return False

    def add_speaker(self, speaker_id, name, color=None):
        """Agregar nuevo speaker conocido"""
        if not color:
            colors = ["\033[93m", "\033[95m", "\033[96m",
                      "\033[97m"]  # Amarillo, Magenta, Cyan, Blanco
            color = colors[len(self.known_voices) % len(colors)]

        self.known_voices[speaker_id] = {"name": name, "color": color}
        print(f"👤 Speaker agregado: {name} ({speaker_id})")

    def save_session(self, filename=None):
        """Guardar sesión de entrenamiento"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ear_training_{timestamp}.json"

        session_data = {
            "timestamp": datetime.now().isoformat(),
            "transcriptions": self.live_transcriptions,
            "known_voices": self.known_voices,
            "total_phrases": len(self.live_transcriptions)
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

        print(f"💾 Sesión guardada: {filename}")
        return filename

    def stop_ear_training(self):
        """Detener modo de entrenamiento"""
        self.is_listening = False
        print("⏹️ Modo OÍDO detenido")

        # Guardar automáticamente
        return self.save_session()
