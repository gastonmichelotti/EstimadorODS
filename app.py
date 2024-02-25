from flask import Flask, request, jsonify
from EstimadorNuevo import Estimar  # Importa tu código aquí

app = Flask(__name__)

@app.route('/estimadorODS', methods=['POST'])
def estimadorODS():
    data = request.get_json()
    fecha = data['fecha']
    incremento_pct = data['incremento_pct']
    incremento_pct_meli = data['incremento_pct_meli']
    inicio_incremento_meli = data['inicio_incremento_meli']

    # Llama a tu función con los parámetros
    resultado = Estimar(fecha,incremento_pct,incremento_pct_meli,inicio_incremento_meli)

    return resultado

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
