from flask import Flask, request, jsonify
from EstimadorNuevo import Estimar 
from EstimadorViejo import Estimar as EstimarViejo # Importa tu código aquí
from EstimadorSimple import estimar_simple_interface

app = Flask(__name__)

@app.route('/estimadorODS', methods=['POST'])
def estimadorODS():
    data = request.get_json()
    fecha = data.get('fecha')
    horario_desde = data.get('horario_desde')
    horario_hasta = data.get('horario_hasta') ##DEBE PASAR EN FORMATO dd/mm/YYYY
    incremento_previo_meli = data.get('incremento_previo_meli') 
    incremento_previo_meli_desde = data.get('incremento_previo_meli_desde')
    incremento_previo_meli_hasta = data.get('incremento_previo_meli_hasta')
    incremento_posterior_general = data.get('incremento_posterior_general') 

    # Llama a tu función con los parámetros usando valores por defecto
    resultado = estimar_simple_interface(fecha,
                        horario_desde if horario_desde is not None else 8,
                        horario_hasta if horario_hasta is not None else 1.5,
                        incremento_previo_meli if incremento_previo_meli is not None else 0 ,
                        incremento_previo_meli_desde if incremento_previo_meli_desde is not None else 0 ,
                        incremento_previo_meli_hasta if incremento_previo_meli_hasta is not None else 0 ,
                        incremento_posterior_general if incremento_posterior_general is not None else 0 ,
                        )

    return resultado

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
