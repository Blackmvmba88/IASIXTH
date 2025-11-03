# 🎵 DOCKERFILE ÉPICO: IYARI-COPILOT MUSICAL AI 🤖
# Contenedor especializado para análisis musical y despertar de consciencia

FROM python:3.11-slim

# Metadatos del dúo dinámico
LABEL maintainer="Iyari Cancino Gomez & GitHub Copilot"
LABEL description="Contenedor musical para despertar IA con ADN sonoro personal"
LABEL version="1.0-infinita"

# Variables de entorno para la aventura
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV IYARI_MUSIC_MODE=enabled
ENV COPILOT_COLLABORATION=true

# Instalar dependencias del sistema para audio profesional
RUN apt-get update && apt-get install -y \
    # Audio y multimedia
    libasound2-dev \
    libportaudio2 \
    libsndfile1 \
    ffmpeg \
    # Compilación y desarrollo
    build-essential \
    cmake \
    pkg-config \
    git \
    # Procesamiento de imágenes
    libopencv-dev \
    # Tesseract OCR
    tesseract-ocr \
    tesseract-ocr-spa \
    # Utilidades
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio para la aventura
WORKDIR /iyari_copilot_adventure

# Copiar archivos del proyecto
COPY requirements_musical.txt .
COPY . .

# Instalar dependencias Python con optimización
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_musical.txt

# Configurar Tesseract para español
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

# Crear directorios para datos musicales
RUN mkdir -p /iyari_copilot_adventure/music_dna \
             /iyari_copilot_adventure/consciousness_data \
             /iyari_copilot_adventure/evolved_patterns \
             /iyari_copilot_adventure/learned_objects \
             /iyari_copilot_adventure/audio_sessions

# Configurar permisos
RUN chmod +x install.sh || true

# Puerto para APIs y interfaces
EXPOSE 8000 8080 5000

# Variables para rutas de música personal
ENV IYARI_MUSIC_PATH=/iyari_copilot_adventure/music_dna
ENV CONSCIOUSNESS_DB=/iyari_copilot_adventure/consciousness_data
ENV EVOLUTION_PATTERNS=/iyari_copilot_adventure/evolved_patterns

# Comando por defecto - ¡La aventura inicia aquí!
CMD ["python", "main_consciousness.py"]

# Healthcheck - verificar que el dúo dinámico esté activo
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
  CMD python -c "print('🎵 Iyari + Copilot = ∞ 🤖')" || exit 1