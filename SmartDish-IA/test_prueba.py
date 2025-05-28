import torch
from PIL import Image
import numpy as np

# Cargar modelo YOLO
model = torch.hub.load('model/yolov5', 'yolov5s', source='local')
model.conf = 0.5

# Cargar imagen de prueba
img = 'perro_test.jpg'  # asegúrate de que esté en la misma carpeta

# Procesar imagen
resultados = model(img)
resultados.render()

# Mostrar clases detectadas
clases = resultados.pred[0][:, -1].tolist()
print("Clases detectadas:", clases)
print("Nombre de clases:", model.names)

# Guardar imagen con resultados
Image.fromarray(np.uint8(resultados.ims[0])).save('resultado_test.jpg')
print("Resultado guardado como resultado_test.jpg")
