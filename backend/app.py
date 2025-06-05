from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Inicializar cliente OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route('/procesar-texto', methods=['POST'])
def procesar_texto():
    try:
        data = request.json
        texto_usuario = data.get("texto", "")

        prompt = f"""
Convertí el siguiente texto en una lista de tareas con: título, fecha y prioridad (alta/media/baja), y devolvé la respuesta en formato JSON.

Texto: "{texto_usuario}"

Respuesta esperada:
[
  {{"tarea": "Preparar TP de NT2", "fecha": "viernes", "prioridad": "alta"}},
  {{"tarea": "Llamar al banco", "fecha": "mañana", "prioridad": "media"}}
]
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        contenido = response.choices[0].message.content.strip()
        print("Respuesta de OpenAI:", contenido)

        return jsonify({"tareas": contenido})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
