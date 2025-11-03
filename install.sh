#!/bin/bash

echo "=== INSTALADOR CÁMARA AI CON VOZ Y OCR ==="
echo ""

# Crear entorno virtual si no existe
if [ ! -d "camera_env" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv camera_env
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source camera_env/bin/activate

# Instalar Tesseract si no está instalado (Mac)
if ! command -v tesseract &> /dev/null; then
    echo "Instalando Tesseract..."
    if command -v brew &> /dev/null; then
        brew install tesseract tesseract-lang-spa
    else
        echo "Por favor instala Homebrew y luego ejecuta:"
        echo "brew install tesseract tesseract-lang-spa"
        exit 1
    fi
fi

# Instalar PortAudio para pyaudio (Mac)
if ! brew list portaudio &> /dev/null; then
    echo "Instalando PortAudio..."
    brew install portaudio
fi

# Instalar dependencias Python básicas primero
echo "Instalando OpenCV y NumPy..."
pip install opencv-python numpy Pillow

echo "Instalando reconocimiento facial..."
pip install face-recognition

echo "Instalando dependencias de audio..."
pip install SpeechRecognition pyttsx3

# Instalar pyaudio (puede ser problemático)
echo "Instalando PyAudio..."
pip install pyaudio

echo "Instalando OCR..."
pip install pytesseract

echo "Instalando utilidades..."
pip install scikit-learn imutils

echo ""
echo "✅ INSTALACIÓN COMPLETADA"
echo ""
echo "Para ejecutar la aplicación:"
echo "1. source camera_env/bin/activate"
echo "2. python main_simple.py"
echo ""
echo "Comandos de voz disponibles:"
echo "- 'Esto es una taza' (para enseñar objetos)"
echo "- 'Esta persona es Juan' (para enseñar caras)"
echo "- 'Para' (detener aprendizaje)"
echo "- 'Ayuda' (obtener ayuda)"