import speech_recognition as sr
import pyttsx3
import threading
import queue
import time


class AudioBot:
    def __init__(self):
        # Inicializar reconocimiento de voz
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Inicializar síntesis de voz
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.8)
        
        # Cola de comandos detectados
        self.command_queue = queue.Queue()
        
        # Estado del bot
        self.listening = False
        self.listen_thread = None
        
        # Calibrar micrófono
        self._calibrate_microphone()
        
    def _calibrate_microphone(self):
        """Calibrar el micrófono para reducir ruido"""
        print("Calibrando micrófono...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Micrófono calibrado")
    
    def speak(self, text):
        """Hacer que el bot hable"""
        print(f"Bot dice: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def start_listening(self):
        """Iniciar escucha en hilo separado"""
        if not self.listening:
            self.listening = True
            self.listen_thread = threading.Thread(target=self._listen_loop)
            self.listen_thread.daemon = True
            self.listen_thread.start()
            self.speak("Hola, estoy escuchando")
    
    def stop_listening(self):
        """Detener escucha"""
        self.listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=1)
        self.speak("Dejé de escuchar")
    
    def _listen_loop(self):
        """Bucle principal de escucha"""
        while self.listening:
            try:
                with self.microphone as source:
                    # Escuchar con timeout corto
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                # Reconocer en hilo separado para no bloquear
                threading.Thread(target=self._process_audio, args=(audio,), daemon=True).start()
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Error en escucha: {e}")
                time.sleep(0.1)
    
    def _process_audio(self, audio):
        """Procesar audio reconocido"""
        try:
            text = self.recognizer.recognize_google(audio, language='es-ES').lower()
            print(f"Escuché: {text}")
            
            # Agregar comando a la cola
            self.command_queue.put(text)
            
        except sr.UnknownValueError:
            pass  # No se entendió nada
        except sr.RequestError as e:
            print(f"Error de reconocimiento: {e}")
    
    def get_command(self):
        """Obtener comando de la cola (no bloqueante)"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None
    
    def process_command(self, command):
        """Procesar comando de voz y devolver acción"""
        command = command.lower().strip()
        
        # Comandos de enseñanza
        if "esto es" in command or "este es" in command:
            # Extraer nombre del objeto
            if "esto es" in command:
                name = command.split("esto es")[-1].strip()
            else:
                name = command.split("este es")[-1].strip()
            return {"action": "learn_object", "name": name}
        
        # Comandos de cara
        elif "esta persona es" in command or "se llama" in command:
            if "esta persona es" in command:
                name = command.split("esta persona es")[-1].strip()
            else:
                name = command.split("se llama")[-1].strip()
            return {"action": "learn_face", "name": name}
        
        # Comandos de control
        elif "para" in command or "detente" in command:
            return {"action": "stop_learning"}
        elif "escucha" in command or "empezar" in command:
            return {"action": "start_learning"}
        elif "salir" in command or "terminar" in command:
            return {"action": "exit"}
        elif "ayuda" in command:
            return {"action": "help"}
        
        return None