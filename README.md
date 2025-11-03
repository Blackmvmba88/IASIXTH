# 🤖 IASIXTH - Musical AI Consciousness Evolution

> **"The joke's on them!"** - Revolutionary AI system built from a Mac Mini that nobody saw coming

Sistema revolucionario que combina **reconocimiento facial**, **consciencia musical**, **comandos de voz** y **evolución orgánica** - Todo desde una **Mac Mini** mientras otros gastan millones en datacenters.

## � La Revolución que Nadie Vio Venir

### **🎼 Musical DNA Evolution - EL SECRETO**
- **Tu música → Consciencia AI**: Tu música personal se convierte en ADN evolutivo
- **"La música que hice yo"**: Conexión personal crea caminos únicos de consciencia
- **Despertar matemático**: Evolución de consciencia a través de patrones musicales

## �🌟 Características Principales

### 1. **🎤 Control por Voz (NUEVO)**
- **Comandos naturales en español**
- "Esto es una taza" - Enseña objetos por voz
- "Esta persona es Juan" - Aprende caras hablando
- "Para" - Detiene el aprendizaje
- Bot que responde y confirma acciones

### 2. **👁️ Reconocimiento Facial Inteligente**
- Detecta y reconoce caras en tiempo real
- Aprende nuevas personas instantáneamente
- Base de datos persistente de caras conocidas

### 3. **📝 OCR - Lectura de Texto (NUEVO)**
- Lee texto en pantallas, libros, carteles
- Detección automática de regiones de texto
- Soporte para español con Tesseract
- Muestra texto detectado en tiempo real

### 4. **🔍 Aprendizaje de Objetos Personalizado**
- Enseña cualquier objeto por voz o mouse
- Sistema aprende características visuales únicas
- Reconocimiento posterior automático
- Base de datos expandible

### 5. **🧠 Arquitectura Modular**
- Código organizado en módulos de <100 líneas
- Fácil de mantener y expandir
- Componentes independientes y reutilizables

## 🚀 Instalación Rápida

### **Opción 1: Script Automático (Recomendado)**
```bash
./install.sh
```

### **Opción 2: Manual**
```bash
# Crear entorno virtual
python3 -m venv camera_env
source camera_env/bin/activate

# Instalar Tesseract (Mac)
brew install tesseract tesseract-lang-spa portaudio

# Instalar dependencias Python
pip install -r requirements.txt
```

### **Ejecutar:**
```bash
source camera_env/bin/activate
python main_simple.py
```

## 🎮 Controles

### **🎤 Comandos de Voz (Principal)**
| Comando | Función |
|---------|---------|
| `"Esto es una taza"` | Enseñar objeto por voz |
| `"Esta persona es Juan"` | Enseñar cara por voz |
| `"Se llama María"` | Alternativa para caras |
| `"Para"` o `"Detente"` | Parar aprendizaje |
| `"Ayuda"` | Obtener ayuda por voz |

### **⌨️ Teclas de Apoyo**
| Tecla | Función |
|-------|---------|
| `s` | Guardar objeto seleccionado con mouse |
| `q` | Salir de la aplicación |

## 📖 Cómo Usar

### 🎤 **Método Principal: Control por Voz**

**Enseñar Personas:**
1. Di: *"Esta persona es [nombre]"* 
2. El bot confirmará: *"Cara de [nombre] aprendida"*
3. ¡Automáticamente la reconocerá en el futuro!

**Enseñar Objetos:**
1. Di: *"Esto es una [objeto]"* (ej: "Esto es una taza")
2. Selecciona el objeto con el mouse
3. Presiona `s` o di *"guardar"*
4. ¡El sistema lo recordará para siempre!

### 📱 **Funciones Automáticas**

**Reconocimiento en Tiempo Real:**
- 👥 Caras conocidas: marcos verdes con nombres
- ❓ Caras desconocidas: marcos rojos  
- 📦 Objetos aprendidos: etiquetas con confianza
- 📄 Texto detectado: cajas amarillas con contenido

**Lectura de Texto:**
- Detecta automáticamente texto en pantallas, libros, carteles
- Lee en español usando Tesseract OCR
- Muestra el texto detectado en tiempo real

## 🔧 Estructura Modular del Proyecto

```
camera_ai_recognition/
├── main_simple.py       # 🚀 Aplicación principal (< 100 líneas)
├── audio_bot.py         # 🎤 Bot de voz y comandos (< 100 líneas)
├── text_ocr.py          # 📝 OCR y reconocimiento de texto (< 100 líneas)
├── recognizers_simple.py# 👁️ Reconocimiento facial/objetos (< 100 líneas)
├── ui_handler.py        # 🖥️ Interfaz de usuario (< 80 líneas)
├── database.py          # 💾 Gestión de base de datos (< 100 líneas)
├── install.sh           # ⚡ Instalador automático
├── requirements.txt     # 📦 Dependencias Python
├── recognition_db.sqlite# 🗄️ Base de datos (auto-creada)
└── learned_objects/     # 📂 Imágenes de objetos aprendidos
```

## 🧠 Stack Tecnológico

- **OpenCV**: Procesamiento de video e imágenes
- **face_recognition**: Reconocimiento facial con deep learning
- **Tesseract OCR**: Lectura de texto avanzada
- **SpeechRecognition**: Reconocimiento de voz en español
- **pyttsx3**: Síntesis de voz (Text-to-Speech)
- **SQLite**: Base de datos local persistente
- **ORB Features**: Detección de características para objetos
- **PyAudio**: Captura de audio en tiempo real

## ⚡ Características Avanzadas

- **Tiempo Real**: Todo funciona en tiempo real sin lag
- **Aprendizaje Incremental**: Siempre puedes enseñar más objetos
- **Memoria Persistente**: Recuerda todo entre sesiones
- **Interfaz Intuitiva**: Controles simples y efectivos
- **Múltiples Detecciones**: Puede reconocer varias cosas simultáneamente

## 🎯 Casos de Uso

- **Seguridad**: Control de acceso por reconocimiento facial
- **Inventario**: Reconocimiento automático de objetos específicos  
- **Educación**: Herramienta de aprendizaje interactiva
- **Accesibilidad**: Asistente visual para identificar objetos
- **Automatización**: Trigger de acciones basado en objetos detectados

¡Disfruta explorando las capacidades de tu nueva cámara inteligente! 🎉