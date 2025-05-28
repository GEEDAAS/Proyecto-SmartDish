import os
from flask import Flask, request, jsonify, send_file
import torch
from PIL import Image, UnidentifiedImageError
from datetime import datetime
import requests
import cv2
import numpy as np
from flask_cors import CORS

# Cargar modelo YOLOv5 local
model = torch.hub.load('model/yolov5', 'yolov5s', source='local')
model.conf = 0.5

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # para pruebas

UPLOAD_FOLDER = 'received'
RESULT_FOLDER = 'resultados'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/detectar', methods=['POST'])
def detectar():
    if 'imagen' not in request.files:
        return jsonify({"error": "No se recibió ninguna imagen"}), 400

    imagen = request.files['imagen']
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    input_path = os.path.join(UPLOAD_FOLDER, f"entrada_{timestamp}.jpg")
    output_path = os.path.join(RESULT_FOLDER, f"salida_{timestamp}.jpg")

    try:
        imagen.save(input_path)

        # Validar que se haya guardado correctamente como imagen
        try:
            Image.open(input_path).verify()
        except UnidentifiedImageError:
            return jsonify({"error": "La imagen recibida no es válida"}), 400

        resultados = model(input_path)
        resultados.render()

        img_result = Image.fromarray(np.uint8(resultados.ims[0]))
        img_result.save(output_path)

        clases_detectadas = resultados.pred[0][:, -1].tolist()
        if 16 in clases_detectadas:
            print("Clases detectadas:", clases_detectadas)
            print("Clases disponibles en el modelo:", model.names)
            return jsonify({"resultado": "perro", "nombre": f"salida_{timestamp}.jpg"})
        else:
            return jsonify({"resultado": "no_perro"})

    except Exception as e:
        print("Error en /detectar:", str(e))
        return jsonify({"error": "Error interno al procesar la imagen"}), 500

@app.route('/resultado/<nombre_imagen>')
def resultado(nombre_imagen):
    ruta = os.path.join(RESULT_FOLDER, nombre_imagen)
    if os.path.exists(ruta):
        return send_file(ruta, mimetype='image/jpeg')
    return "Imagen no encontrada", 404

@app.route('/captura_proxy')
def captura_proxy():
    try:
        url_esp32cam = "http://10.0.16.40/captura.jpg"  # <- CORREGIDO
        response = requests.get(url_esp32cam, timeout=5)

        print(">>> Código HTTP:", response.status_code)
        print(">>> Content-Type:", response.headers.get('Content-Type'))
        print(">>> Content-Length:", response.headers.get('Content-Length'))

        if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('image'):
            return response.content, 200, {'Content-Type': 'image/jpeg'}
        else:
            return "La ESP32-CAM no devolvió una imagen válida", 500

    except Exception as e:
        print("Error en captura_proxy:", str(e))
        return "Error al obtener imagen: " + str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
