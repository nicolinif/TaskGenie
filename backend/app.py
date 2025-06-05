from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid
from openai import OpenAI
from pymongo import MongoClient
import json
from datetime import datetime, timedelta
import re

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# --- MongoDB ---
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["taskgenie"]
tareas_collection = db["tareas"]

# --- OpenAI ---
api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)

# --- Helpers ---
def corregir_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        hoy = datetime.now().date()

        if fecha < hoy:
            # Si la fecha es anterior a hoy, la pasamos al año actual o al próximo
            while fecha < hoy:
                fecha += timedelta(days=7)

        return fecha.strftime("%d/%m/%Y")
    except Exception as e:
        print("⚠️ Error al corregir fecha:", e)
        return ""

# --- Ruta para procesar texto y generar tareas ---
@app.route('/procesar-texto', methods=['POST'])
def procesar_texto():
    datos = request.get_json()
    texto_usuario = datos.get('texto', '')

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Convertí el texto en tareas en formato JSON. Devolvé una lista de objetos con: titulo, descripcion y fecha (YYYY-MM-DD)."
                },
                {
                    "role": "user",
                    "content": texto_usuario
                }
            ]
        )

        raw_response = completion.choices[0].message.content.strip()
        print("📥 Respuesta cruda de OpenAI:")
        print(raw_response)

        json_str = re.search(r'\{.*\}|\[.*\]', raw_response, re.DOTALL)
        if not json_str:
            raise ValueError("JSON no encontrado")

        parsed = json.loads(json_str.group())

        # Soporta distintos formatos
        if isinstance(parsed, dict) and "titulo" in parsed:
            tareas = [parsed]
        elif isinstance(parsed, dict) and "tareas" in parsed:
            tareas = parsed["tareas"]
        elif isinstance(parsed, list):
            tareas = parsed
        else:
            raise ValueError("Formato de tareas no reconocido")

        print("✅ Tareas parseadas:", tareas)

        for tarea in tareas:
            tarea_obj = {
                "id": str(uuid.uuid4()),
                "titulo": tarea.get("titulo", ""),
                "descripcion": tarea.get("descripcion", ""),
                "fecha": corregir_fecha(tarea.get("fecha", "")),
                "completado": False
            }
            print("📤 Insertando en MongoDB:", tarea_obj)
            tareas_collection.insert_one(tarea_obj)

        return jsonify({"tareas": tareas})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({'error': 'Hubo un error al procesar el texto.'}), 500

# --- Ruta para obtener tareas ---
@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    tareas = list(tareas_collection.find({}, {"_id": 0}))
    return jsonify(tareas)

# Marcar tarea como completada
@app.route("/tareas/<id>", methods=["PATCH"])
def completar_tarea(id):
    result = tareas_collection.update_one(
        {"id": id},
        {"$set": {"completado": True}}
    )
    if result.matched_count:
        return jsonify({"mensaje": f"Tarea marcada como completada."})
    else:
        return jsonify({"error": "Tarea no encontrada."}), 404

# Eliminar una tarea
@app.route("/tareas/<id>", methods=["DELETE"])
def eliminar_tarea(id):
    result = tareas_collection.delete_one({"id": id})
    if result.deleted_count:
        return jsonify({"mensaje": f"Tarea eliminada."})
    else:
        return jsonify({"error": "Tarea no encontrada."}), 404

# --- Main ---
if __name__ == "__main__":
    app.run(debug=True)


