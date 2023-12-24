import pandas as pd
import requests
import numpy as np
from scipy.optimize import minimize
import json

def Estimar(fecha, duracion = 4):

    #Utilidades Estáticas
    class Reserva:
        # Constructor de la clase
        def __init__(self, horaDesde, horaHasta):
            # Atributo de la clase
            self.horaDesde = horaDesde
            self.horaHasta = horaHasta

    # Estos valores son parámetros que algun dia se pueden querer tocar
    horarios = np.arange(10, 24, 0.5)
    # horariosReservas = [(10,14), (12,16), (14.5, 18.5), (17, 20), (19,23), (20.5, 24)]  

    # Probando con todos los turnos posibles de 4 hs
    horarioAux = np.arange(10, 25 - duracion, 1)

    horariosReservas = []

    for i in range(len(horarioAux)):
        horariosReservas.append((horarioAux[i], horarioAux[i] + duracion))



    def obtener_valores_por_fecha(fecha):
        """Obtiene los valores de repas activos por hora que necesita Meli - desde un google sheets nuestro"""

        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqP8Cc8coM8EqPpAHDiRtyX2sxd1gokCUCbR8erhVrs7O9hXXbW0oruGaZIDtXYvLAztNoLG645L0I/pub?output=csv"
        response = requests.get(url)
        assert response.status_code == 200, 'Error al descargar los datos'
        df = pd.read_csv(url)
        
        # Encontrar la columna con la fecha dada
        columna_fecha = None
        for col in df.columns:
            if df[col].iloc[0] == fecha:
                columna_fecha = col
                break
        
        if columna_fecha is None:
            return f"No se encontró la fecha {fecha}"
        
        # Obtener los valores no nulos de esa columna
        valoresMeli = df[columna_fecha].dropna().tolist()

        # Convertir valores de string a integer
        valoresMeli = [int(valor) for valor in valoresMeli if valor.isdigit()]

        return valoresMeli  # Excluimos las primeras dos filas que son encabezados

    def calcular_disponibilidad(configuracion):
        """En Base a la cantidad de reservas por turno pre armado, calcula la disponibilidad de repas"""   

        if duracion == 4:
            [A, B, C, D, E, F, G, H, I, J, K]= configuracion        
        else: 
            #ASUME 3 HS
            [A, B, C, D, E, F, G, H, I, J, K, L ]= configuracion   

        
        reservas = []

        for i in range(len(configuracion)):

            cantidad = round(configuracion[i])

            for j in range(cantidad):
                reservas.append(Reserva(horariosReservas[i][0], horariosReservas[i][1]))

        disponibilidad = []

        for i in horarios:
            contador = 0

            for reserva in reservas:
                if reserva.horaDesde <= i and reserva.horaHasta > i:
                    contador += 1
            
            disponibilidad.append(contador)
                
        return disponibilidad
            

    reservasMeli = obtener_valores_por_fecha(fecha)

    # Función objetivo para la optimización
    def objetivo(config):

        disponibilidad = calcular_disponibilidad(config)
        
        if len(reservasMeli) != len(disponibilidad):
            raise ValueError("Error: diferentes largos entre listas de disponibilidad meli-rapiboy")
        
        diferencia = sum((rm - rd)**2 for rm, rd in zip(reservasMeli, disponibilidad))
        
        # diferencia = 0

        # for i in range(len(reservasMeli)):
        #     diferencia += (reservasMeli[i] -  disponibilidad[i])**2
        
        return diferencia  


    # Valores iniciales para los precios
    # valores_iniciales = [reservasMeli[0], reservasMeli[8],reservasMeli[13], reservasMeli[18], reservasMeli[22], reservasMeli[23]]
    valores_iniciales = [reservasMeli[0]]* len(horariosReservas)

    # Definir los límites para cada parámetro en config
    # (0, None) significa que el valor puede variar de 0 a infinito
    bounds = [(reservasMeli[0], None) for _ in range(len(valores_iniciales))]

    # Llamada a minimize con opciones adicionales
    resultado_optimizacion = minimize(objetivo, valores_iniciales, method='Powell', bounds=bounds)

    # Resultados óptimos
    configuracionOptima = resultado_optimizacion.x   

    Resultados = []

    for i in range(len(horariosReservas)):
        configuracionOptima[i] = int(configuracionOptima[i])

        # resultado = (f"{horariosReservas[i][0]:02d}:00", f"{horariosReservas[i][1]:02d}:00", int(configuracionOptima[i]))
        # Resultados.append(resultado)

        Resultados.append({
        'horaDesde': f"{horariosReservas[i][0]:02d}:00", 
        'horaHasta': f"{horariosReservas[i][1]:02d}:00", 
        'cantidad': int(configuracionOptima[i])})

    final = {"turnos" : Resultados}

    return final

