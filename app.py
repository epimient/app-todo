from flask import Flask, request, jsonify
from flask_cors import CORS
from peewee import *
import os

# manejo de base de datos
DATABASE_URL = "postgresql://tareas_db_yaxw_user:9S1fXo9yWI6ejhUWGgIFE5qBNBgdqW9Y@dpg-d0vvmdu3jp1c739g1big-a/tareas_db_yaxw"
db = PostgresqlDatabase(
    'tareas_db_yaxw',
    user='tareas_db_yaxw_user',
    password='9S1fXo9yWI6ejhUWGgIFE5qBNBgdqW9Y',
    host='dpg-d0vvmdu3jp1c739g1big-a',
    port=5432
)

#modelo de la base de datos
class BaseModel(Model):
    class Meta:
        database = db

class Tarea(BaseModel):
    titulo = CharField()
    descripcion = TextField()
    completada = BooleanField(default=False)

db.connect()
db.create_tables([Tarea], safe=True)

# Inicialización de la aplicación Flask
app = Flask(__name__)
CORS(app)

# Rutas
@app.route("/")
def health_check():
    return {"status": "ok", "message": "API is running"}

#rutas crud
@app.route("/tareas", methods=["POST"])
def crear_tarea():
    data = request.get_json()
    tarea = Tarea.create(
        titulo=data["titulo"],
        descripcion=data["descripcion"],
        completada=data.get("completada", False)
    )
    return jsonify({"id": tarea.id, "titulo": tarea.titulo, "descripcion": tarea.descripcion, "completada": tarea.completada}), 201

@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    tareas = Tarea.select()
    return jsonify([{"id": tarea.id, "titulo": tarea.titulo, "descripcion": tarea.descripcion, "completada": tarea.completada} for tarea in tareas]), 200

@app.route("/tareas/<int:id>", methods=["GET"])
def obtener_tarea(id):
    tarea = Tarea.get_or_none(Tarea.id == id)
    if tarea:
        return jsonify({"id": tarea.id, "titulo": tarea.titulo, "descripcion": tarea.descripcion, "completada": tarea.completada}), 200
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route("/tareas/<int:id>", methods=["PUT"])
def actualizar_tarea(id):
    data = request.get_json()
    tarea = Tarea.get_or_none(Tarea.id == id)
    if tarea:
        tarea.titulo = data.get("titulo", tarea.titulo)
        tarea.descripcion = data.get("descripcion", tarea.descripcion)
        tarea.completada = data.get("completada", tarea.completada)
        tarea.save()
        return jsonify({"id": tarea.id, "titulo": tarea.titulo, "descripcion": tarea.descripcion, "completada": tarea.completada}), 200
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route("/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    tarea = Tarea.get_or_none(Tarea.id == id)
    if tarea:
        tarea.delete_instance()
        return jsonify({"message": "Tarea eliminada"}), 204
    return jsonify({"error": "Tarea no encontrada"}), 404

def modelo_a_diccionario(tarea):
    return {
        "id": tarea.id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "completada": tarea.completada
    }

if __name__ == "__main__":
    app.run(debug=True)