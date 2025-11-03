import cv2
import pytesseract
import numpy as np
from database import DatabaseManager
import re


class TextRecognizer:
    def __init__(self):
        self.db = DatabaseManager()

        # Configurar Tesseract (ajusta la ruta según tu instalación)
        # En Mac con Homebrew: /opt/homebrew/bin/tesseract
        pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

        # Configuración para español
        self.config = '--oem 3 --psm 6 -l spa'

    def preprocess_for_ocr(self, frame):
        """Preprocesar imagen para mejorar OCR"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar filtro gaussiano para reducir ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Aplicar threshold adaptativo
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return thresh

    def detect_text_regions(self, frame):
        """Detectar regiones con texto"""
        processed = self.preprocess_for_ocr(frame)

        # Encontrar contornos
        contours, _ = cv2.findContours(
            processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Filtrar por tamaño (probable texto)
            if w > 50 and h > 20 and w < 800 and h < 100:
                aspect_ratio = w / h
                if 2 < aspect_ratio < 15:  # Ratio típico de texto
                    text_regions.append((x, y, w, h))

        return text_regions

    def extract_text(self, frame, region=None):
        """Extraer texto de una región específica o frame completo"""
        if region:
            x, y, w, h = region
            roi = frame[y:y + h, x:x + w]
        else:
            roi = frame

        # Preprocesar
        processed = self.preprocess_for_ocr(roi)

        try:
            # Extraer texto
            text = pytesseract.image_to_string(
                processed, config=self.config
            ).strip()

            # Limpiar texto
            text = re.sub(r'[^\w\sáéíóúñü]', ' ', text, flags=re.IGNORECASE)
            text = ' '.join(text.split())

            return text if len(text) > 2 else None

        except Exception as e:
            print(f"Error en OCR: {e}")
            return None

    def process_frame(self, frame):
        """Procesar frame completo para detectar y extraer texto"""
        text_regions = self.detect_text_regions(frame)
        detected_texts = []

        for region in text_regions:
            text = self.extract_text(frame, region)
            if text:
                detected_texts.append({
                    'text': text,
                    'region': region,
                    'confidence': len(text) / 50.0  # Aproximación simple
                })

                # Registrar en base de datos
                self.db.log_detection("text", text, len(text) / 50.0)

        return detected_texts

    def draw_text_boxes(self, frame, detected_texts):
        """Dibujar cajas alrededor del texto detectado"""
        for item in detected_texts:
            x, y, w, h = item['region']
            text = item['text']

            # Dibujar rectángulo
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

            # Dibujar texto detectado
            font_scale = 0.5
            thickness = 1

            # Calcular posición del texto
            text_size = cv2.getTextSize(text[:30], cv2.FONT_HERSHEY_SIMPLEX,
                                        font_scale, thickness)[0]

            # Fondo para el texto
            cv2.rectangle(frame, (x, y - text_size[1] - 10),
                          (x + text_size[0], y), (255, 255, 0), -1)

            # Texto
            cv2.putText(frame,
                        text[:30],
                        (x,
                         y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale,
                        (0,
                            0,
                            0),
                        thickness)

        return frame
