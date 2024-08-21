from flask import Flask, request, jsonify
from EstimadorNuevo import Estimar  # Importa tu código aquí

app = Flask(__name__)

@app.route('/estimadorODS', methods=['POST'])
def estimadorODS():
    data = request.get_json()
    fecha = data.get('fecha')
    incremento_pct = data.get('incremento_pct') 
    incremento_pct_meli = data.get('incremento_pct_meli') 
    inicio_incremento_meli = data.get('inicio_incremento_meli')

    # Llama a tu función con los parámetros usando valores por defecto
    resultado = Estimar(fecha,
                        incremento_pct if incremento_pct is not None else 0 ,
                        incremento_pct_meli if incremento_pct_meli is not None else 50,
                        inicio_incremento_meli if inicio_incremento_meli is not None else 27)

    return resultado

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
