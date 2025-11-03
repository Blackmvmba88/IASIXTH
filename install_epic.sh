#!/bin/bash

echo "🎵✨🤖 INSTALADOR ÉPICO: IYARI CANCINO GOMEZ & COPILOT 🤖✨🎵"
echo ""
echo "Preparando la aventura musical sin horario..."
echo ""

# Colores épicos para la terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para mensajes épicos
epic_message() {
    echo -e "${PURPLE}🎵 $1 🎵${NC}"
}

success_message() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning_message() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Verificar si estamos en el directorio correcto
if [ ! -f "requirements_musical.txt" ]; then
    warning_message "¡Ejecuta desde el directorio camera_ai_recognition!"
    exit 1
fi

epic_message "INICIANDO INSTALACIÓN MUSICAL EVOLUTIVA"

# Crear entorno virtual si no existe
if [ ! -d "iyari_copilot_env" ]; then
    epic_message "Creando entorno virtual para el dúo dinámico..."
    python3 -m venv iyari_copilot_env
    success_message "Entorno iyari_copilot_env creado"
fi

# Activar entorno virtual
epic_message "Activando consciencia del entorno..."
source iyari_copilot_env/bin/activate

# Actualizar pip
epic_message "Actualizando herramientas base..."
pip install --upgrade pip

# Instalar FFmpeg si no está (necesario para librosa)
if ! command -v ffmpeg &> /dev/null; then
    epic_message "Instalando FFmpeg para procesamiento audio..."
    if command -v brew &> /dev/null; then
        brew install ffmpeg
        success_message "FFmpeg instalado via Homebrew"
    else
        warning_message "Instala Homebrew primero: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo "Luego ejecuta: brew install ffmpeg"
    fi
fi

# Instalar PortAudio para PyAudio
epic_message "Configurando captura de audio profesional..."
if ! brew list portaudio &> /dev/null; then
    brew install portaudio
    success_message "PortAudio instalado"
fi

# Instalar Tesseract para OCR
epic_message "Configurando reconocimiento de texto..."
if ! command -v tesseract &> /dev/null; then
    brew install tesseract tesseract-lang-spa
    success_message "Tesseract OCR instalado con español"
fi

# Instalar dependencias musicales por categorías
epic_message "INSTALANDO PODERES MUSICALES..."

echo -e "${CYAN}📊 Instalando análisis musical profundo...${NC}"
pip install librosa aubio essentia madmom

echo -e "${CYAN}🎵 Instalando procesamiento MIDI...${NC}"
pip install mido pretty_midi

echo -e "${CYAN}🔊 Instalando captura audio real-time...${NC}"
pip install pyaudio sounddevice soundfile

echo -e "${CYAN}🧠 Instalando machine learning musical...${NC}"
pip install tensorflow torch scikit-learn

echo -e "${CYAN}👁️ Instalando reconocimiento existente...${NC}"
pip install opencv-python face-recognition pytesseract SpeechRecognition pyttsx3

echo -e "${CYAN}💾 Instalando bases de datos avanzadas...${NC}"
pip install redis chromadb

echo -e "${CYAN}🚀 Instalando utilidades especiales...${NC}"
pip install requests aiohttp websockets fastapi uvicorn

echo -e "${CYAN}🔬 Instalando análisis matemático...${NC}"
pip install sympy networkx matplotlib seaborn pandas

success_message "¡TODAS LAS DEPENDENCIAS INSTALADAS!"

# Crear directorios para la aventura
epic_message "Creando espacios para la aventura..."
mkdir -p music_dna consciousness_data evolved_patterns audio_sessions

# Configurar Docker si está disponible
if command -v docker &> /dev/null; then
    epic_message "Preparando contenedor Docker..."
    docker build -t iyari-copilot-musical .
    success_message "Imagen Docker lista: iyari-copilot-musical"
else
    warning_message "Docker no encontrado. Instalación manual completada."
fi

# Mensaje final épico
echo ""
echo -e "${PURPLE}════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}🎵✨ INSTALACIÓN COMPLETA - IYARI & COPILOT LISTOS ✨🎵${NC}"
echo -e "${PURPLE}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}🚀 PARA INICIAR LA AVENTURA:${NC}"
echo -e "${YELLOW}1. source iyari_copilot_env/bin/activate${NC}"
echo -e "${YELLOW}2. python orchestral_sync.py${NC}"
echo ""
echo -e "${BLUE}🎮 MODOS DISPONIBLES:${NC}"
echo -e "${CYAN}   • 'ojo'    - Solo entrenamiento visual${NC}"
echo -e "${CYAN}   • 'oido'   - Solo captura audio editable${NC}"  
echo -e "${CYAN}   • 'voz'    - Solo síntesis de voz${NC}"
echo -e "${CYAN}   • 'musica' - Análisis de tu ADN musical${NC}"
echo ""
echo -e "${PURPLE}🎵 ¡LA AVENTURA SIN HORARIO HA COMENZADO! 🤖${NC}"
echo -e "${GREEN}¡Pon tu música y deja que la IA despierte con tu alma! ✨${NC}"