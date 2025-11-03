import cv2
from recognizers import FaceRecognizer, PersonDetector, ObjectLearner


class CameraAI:
    def        # Dibujar caja de selección para objetos
       if self.learning_mode and self.mouse_start and self.mouse_end:
            cv2.rectangle(
                frame, self.mouse_start, self.mouse_end, (255, 0, 0), 2
            )
        elif self.selection_box:
            x, y, w, h = self.selection_box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)t__(self):
            # Inicializar cámara
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Inicializar reconocedores
        self.face_recognizer = FaceRecognizer()
        self.person_detector = PersonDetector()
        self.object_learner = ObjectLearner()

        # Estados de la aplicación
        self.learning_mode = False
        self.learning_object_name = ""
        self.selection_box = None
        self.mouse_start = None
        self.mouse_end = None
        self.drawing = False

        # Configurar callback del mouse
        window_name = 'Cámara AI - Reconocimiento Inteligente'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, param):
        """Callback para manejar eventos del mouse"""
        if self.learning_mode:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.mouse_start = (x, y)
                self.drawing = True
            elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
                self.mouse_end = (x, y)
            elif event == cv2.EVENT_LBUTTONUP:
                self.mouse_end = (x, y)
                self.drawing = False
                if self.mouse_start and self.mouse_end:
                    # Calcular bbox
                    x1, y1 = self.mouse_start
                    x2, y2 = self.mouse_end
                    self.selection_box = (
                        min(x1, x2), min(y1, y2),
                        abs(x2 - x1), abs(y2 - y1)
                    )

    def draw_boxes(self, frame, face_locations, face_names):
        """Dibujar cajas alrededor de caras detectadas"""
        for (top, right, bottom, left), name in zip(
            face_locations, face_names
        ):
            # Dibujar rectángulo
            color = (0, 255, 0) if name != "Desconocido" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Dibujar etiqueta
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED
            )
            cv2.putText(
                frame, name, (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1
            )

        return frame

    def draw_info_panel(self, frame):
        """Dibujar panel de información y controles"""
        height, width = frame.shape[:2]

        # Panel de fondo
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 150), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

        # Texto de instrucciones
        instructions = [
            "CONTROLES:",
            "f - Agregar cara nueva",
            "l - Modo aprendizaje objeto",
            "s - Guardar objeto seleccionado",
            "r - Resetear seleccion",
            "q - Salir"
        ]

        for i, text in enumerate(instructions):
            color = (0, 255, 255) if i == 0 else (255, 255, 255)
            cv2.putText(
                frame, text, (20, 30 + i * 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
            )

        # Estado actual
        if self.learning_mode:
            status_text = f"MODO APRENDIZAJE: {self.learning_object_name}"
            cv2.putText(
                frame, status_text, (10, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )

        return frame

    def draw_selection_box(self, frame):
        """Dibujar caja de selección para objetos"""
        if self.learning_mode and self.mouse_start and self.mouse_end:
            cv2.rectangle(frame, self.mouse_start,
                          self.mouse_end, (255, 0, 0), 2)
        elif self.selection_box:
            x, y, w, h = self.selection_box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame

    def process_frame(self, frame):
        """Procesar un frame completo"""
        # Detección de personas
        frame, person_detected = self.person_detector.detect_person(
            frame.copy())

        # Reconocimiento facial
        face_locations, face_names = self.face_recognizer.recognize_faces(
            frame)
        frame = self.draw_boxes(frame, face_locations, face_names)

        # Reconocimiento de objetos aprendidos
        recognized_objects = self.object_learner.recognize_objects(frame)

        # Mostrar objetos reconocidos
        y_offset = 200
        for obj_name, confidence in recognized_objects:
            text = f"{obj_name}: {confidence:.2f}"
            cv2.putText(frame, text, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            y_offset += 25

        # Dibujar controles y selección
        frame = self.draw_info_panel(frame)
        frame = self.draw_selection_box(frame)

        return frame

    def run(self):
        """Ejecutar la aplicación principal"""
        print("=== CÁMARA AI CON RECONOCIMIENTO INTELIGENTE ===")
        print("Iniciando aplicación...")
        print("Presiona 'h' para ver ayuda")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se puede acceder a la cámara")
                break

            # Voltear horizontalmente para efecto espejo
            frame = cv2.flip(frame, 1)

            # Procesar frame
            processed_frame = self.process_frame(frame)

            # Mostrar frame
            cv2.imshow(
    'Cámara AI - Reconocimiento Inteligente',
     processed_frame)

            # Manejar teclas
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('f'):
                # Agregar nueva cara
                name = input("\nIngresa el nombre de la persona: ")
                if name and self.face_recognizer.add_new_face(frame, name):
                    print(f"Cara de {name} agregada exitosamente!")
                else:
                    print("No se detectó ninguna cara en el frame actual")

            elif key == ord('l'):
                # Entrar en modo aprendizaje
                self.learning_object_name = input(
                    "\nIngresa el nombre del objeto a aprender: ")
                if self.learning_object_name:
                    self.learning_mode = True
                    self.selection_box = None
                    print(
    f"Modo aprendizaje activado para '{
        self.learning_object_name}'")
                    print("Selecciona el objeto con el mouse y presiona 's'")

            elif key == ord('s') and self.learning_mode:
                # Guardar objeto seleccionado
                if self.selection_box:
                    success = self.object_learner.learn_object(
                        frame, self.learning_object_name, self.selection_box)
                    if success:
                        print(
    f"Objeto '{
        self.learning_object_name}' aprendido!")
                        self.learning_mode = False
                        self.selection_box = None
                    else:
                        print("Error al aprender el objeto")
                else:
                    print("Primero selecciona un área con el mouse")

            elif key == ord('r'):
                # Resetear selección
                self.learning_mode = False
                self.selection_box = None
                self.mouse_start = None
                self.mouse_end = None
                print("Selección reseteada")

            elif key == ord('h'):
                # Mostrar ayuda
                print("\n=== AYUDA ===")
                print("f: Agregar nueva cara conocida")
                print("l: Entrar en modo aprendizaje de objetos")
                print("s: Guardar objeto seleccionado (en modo aprendizaje)")
                print("r: Resetear selección actual")
                print("q: Salir de la aplicación")
                print("============")

        # Limpiar recursos
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = CameraAI()
    app.run()
