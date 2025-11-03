import cv2


class UIHandler:
    def __init__(self):
        self.mouse_start = None
        self.mouse_end = None
        self.drawing = False
        self.current_selection = None
    
    def mouse_callback(self, event, x, y, flags, param):
        """Callback para eventos del mouse"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_start = (x, y)
            self.drawing = True
        
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.mouse_end = (x, y)
        
        elif event == cv2.EVENT_LBUTTONUP:
            self.mouse_end = (x, y)
            self.drawing = False
            
            if self.mouse_start and self.mouse_end:
                x1, y1 = self.mouse_start
                x2, y2 = self.mouse_end
                self.current_selection = (
                    min(x1, x2), min(y1, y2), 
                    abs(x2 - x1), abs(y2 - y1)
                )
    
    def get_selection(self):
        """Obtener selección actual"""
        return self.current_selection
    
    def reset_selection(self):
        """Resetear selección"""
        self.current_selection = None
        self.mouse_start = None
        self.mouse_end = None
    
    def draw_face_boxes(self, frame, face_locations, face_names):
        """Dibujar cajas de caras"""
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            color = (0, 255, 0) if name != "Desconocido" else (0, 0, 255)
            
            # Rectángulo de cara
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Etiqueta de nombre
            cv2.rectangle(frame, (left, bottom - 35), 
                         (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        
        return frame
    
    def draw_selection_box(self, frame, selection_box):
        """Dibujar caja de selección"""
        if self.drawing and self.mouse_start and self.mouse_end:
            cv2.rectangle(frame, self.mouse_start, self.mouse_end, (255, 0, 0), 2)
        elif selection_box:
            x, y, w, h = selection_box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        return frame
    
    def draw_info_panel(self, frame, objects, texts, learning_mode, learning_name):
        """Dibujar panel de información"""
        height, width = frame.shape[:2]
        
        # Panel principal
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
        
        # Controles
        controls = [
            "VOZ: 'esto es taza', 'se llama Juan'",
            "TECLAS: s=guardar, q=salir", 
            f"OBJETOS: {len(objects)} reconocidos",
            f"TEXTO: {len(texts)} detectados"
        ]
        
        for i, text in enumerate(controls):
            cv2.putText(frame, text, (15, 25 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Estado de aprendizaje
        if learning_mode:
            status = f"APRENDIENDO: {learning_name}"
            cv2.putText(frame, status, (10, height - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Mostrar objetos reconocidos
        y_offset = 140
        for obj_name, confidence in objects[:3]:  # Solo primeros 3
            text = f"{obj_name}: {confidence:.2f}"
            cv2.putText(frame, text, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            y_offset += 20
        
        return frame