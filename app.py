from flask import Flask, request, jsonify
from EstimadorNuevo import Estimar  # Importa tu código aquí

app = Flask(__name__)

@app.route('/estimadorODS', methods=['POST'])
def estimadorODS():
    data = request.get_json()
    duracion = data['duracion']
    fecha = data['fecha']

    # Llama a tu función con los parámetros
    resultado = Estimar(fecha, duracion)

    return resultado

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
