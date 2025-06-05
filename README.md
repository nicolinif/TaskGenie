# 🧠 TaskGenie – Asistente Inteligente de Tareas

TaskGenie es una aplicación fullstack que permite a los usuarios ingresar texto en lenguaje natural y obtener una lista estructurada de tareas con fecha y prioridad, gracias al poder de la inteligencia artificial.

---

## 🚀 Funcionalidades

- Ingreso de texto libre como:  
  _"Tengo que preparar el TP de NT2 para el viernes y llamar al banco mañana."_
- Generación automática de tareas individuales con:
  - 📌 Título
  - 🗓 Fecha estimada
  - ⚡ Prioridad (alta / media / baja)
- Interfaz responsive con Vue 3 y Bootstrap
- Backend en Flask + integración con OpenAI GPT-4o
- Preparado para futuras funcionalidades: edición, eliminación, persistencia, usuarios, etc.

---

## 🧰 Tecnologías utilizadas

### Frontend
- Vue 3 + Vite
- Axios
- Bootstrap 5

### Backend
- Python 3 + Flask
- OpenAI API (`gpt-4o`)
- Flask-CORS
- Dotenv para manejo de claves

---

## 🛠️ Instalación local

### 1. Clonar el repositorio
```bash
git clone https://github.com/nicolinif/taskgenie.git
cd taskgenie
