import cv2
from recognizers import FaceRecognizer, ObjectLearner
from audio_bot import AudioBot
from text_ocr import TextRecognizer
from ui_handler import UIHandler


class CameraAI:
    def __init__(self):
        # Inicializar cámara
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Inicializar componentes
        self.face_recognizer = FaceRecognizer()
        self.object_learner = ObjectLearner()
        self.audio_bot = AudioBot()
        self.text_recognizer = TextRecognizer()
        self.ui = UIHandler()
        
        # Estados
        self.learning_mode = False
        self.learning_object_name = ""
        self.selection_box = None
        
        # Configurar ventana
        cv2.namedWindow('Cámara AI - Reconocimiento Inteligente')
        cv2.setMouseCallback('Cámara AI - Reconocimiento Inteligente', 
                           self.ui.mouse_callback)
    
    def process_voice_commands(self):
        """Procesar comandos de voz"""
        command_text = self.audio_bot.get_command()
        if command_text:
            command = self.audio_bot.process_command(command_text)
            
            if command:
                action = command.get('action')
                
                if action == 'learn_object':
                    name = command.get('name')
                    if name:
                        self.learning_mode = True
                        self.learning_object_name = name
                        self.audio_bot.speak(f"Selecciona el objeto {name}")
                
                elif action == 'learn_face':
                    name = command.get('name')
                    if name:
                        success = self.face_recognizer.add_new_face(
                            self.current_frame, name
                        )
                        if success:
                            self.audio_bot.speak(f"Cara de {name} aprendida")
                        else:
                            self.audio_bot.speak("No veo ninguna cara")
                
                elif action == 'stop_learning':
                    self.learning_mode = False
                    self.audio_bot.speak("Modo aprendizaje desactivado")
                
                elif action == 'help':
                    self.audio_bot.speak("Puedes decir: esto es una taza, "
                                       "esta persona es Juan, para, ayuda")
    
    def process_frame(self, frame):
        """Procesar frame principal"""
        self.current_frame = frame.copy()
        
        # Reconocimiento facial
        face_locations, face_names = self.face_recognizer.recognize_faces(frame)
        
        # Reconocimiento de objetos
        recognized_objects = self.object_learner.recognize_objects(frame)
        
        # OCR - Reconocimiento de texto
        detected_texts = self.text_recognizer.process_frame(frame)
        
        # Dibujar resultados
        frame = self.ui.draw_face_boxes(frame, face_locations, face_names)
        frame = self.text_recognizer.draw_text_boxes(frame, detected_texts)
        frame = self.ui.draw_info_panel(frame, recognized_objects, 
                                      detected_texts, self.learning_mode, 
                                      self.learning_object_name)
        frame = self.ui.draw_selection_box(frame, self.selection_box)
        
        return frame
    
    def run(self):
        """Ejecutar aplicación principal"""
        print("=== CÁMARA AI CON VOZ Y OCR ===")
        print("Di 'ayuda' para comandos de voz")
        
        # Iniciar bot de voz
        self.audio_bot.start_listening()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Voltear para efecto espejo
                frame = cv2.flip(frame, 1)
                
                # Procesar comandos de voz
                self.process_voice_commands()
                
                # Obtener selección del mouse
                self.selection_box = self.ui.get_selection()
                
                # Procesar frame
                processed_frame = self.process_frame(frame)
                
                # Mostrar
                cv2.imshow('Cámara AI - Reconocimiento Inteligente', 
                         processed_frame)
                
                # Manejar teclas
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s') and self.learning_mode and self.selection_box:
                    # Guardar objeto seleccionado
                    success = self.object_learner.learn_object(
                        frame, self.learning_object_name, self.selection_box
                    )
                    if success:
                        self.audio_bot.speak("Objeto aprendido")
                        self.learning_mode = False
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpiar recursos"""
        self.audio_bot.stop_listening()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = CameraAI()
    app.run()