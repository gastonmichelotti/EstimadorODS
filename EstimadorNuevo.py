import pandas as pd
import requests
import numpy as np
from scipy.optimize import minimize
import math  # Asegúrate de tener esta importación para math.ceil

def Estimar(fecha, incremento_pct=0, incremento_pct_meli=20, inicio_incremento_meli=22):
    class Reserva:
        def __init__(self, horaDesde, horaHasta):
            self.horaDesde = horaDesde
            self.horaHasta = horaHasta

    horarios = np.arange(10, 24, 0.5)
    # horarioAux = np.arange(10, 25 - duracion, 1)
    # horariosReservas = [(i, i + duracion) for i in horarioAux]

    horariosReservas = [(10,14),(11,15),(12,16),(13,17),(14,18),(15,19),
                        (16,20),(17,21),(18,22),(19,23),(19,22),(19,22.5),
                        (19,21),(19.5,23.5),(19.5,22.5),(19.5,23),(19.5,21.5),
                        (20,24),(20,23),(20,23.5),(20,22),(20.5,24.5),(20.5,23.5),
                        (20.5,24),(20.5,22.5),(21,24),(21,24.5),(21,23),(22,24),(22,24.5)]

    def obtener_valores_por_fecha(fecha):
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqP8Cc8coM8EqPpAHDiRtyX2sxd1gokCUCbR8erhVrs7O9hXXbW0oruGaZIDtXYvLAztNoLG645L0I/pub?output=csv"
        response = requests.get(url)
        assert response.status_code == 200, 'Error al descargar los datos'
        df = pd.read_csv(url)
        
        columna_fecha = None
        for col in df.columns:
            if df[col].iloc[0] == fecha:
                columna_fecha = col
                break
        
        if columna_fecha is None:
            return f"No se encontró la fecha {fecha}"
        
        valoresMeli = [int(valor) for valor in df[columna_fecha].dropna().tolist() if valor.isdigit()]

        valoresMeliIncrementados = [0]*len(valoresMeli)

        # Aplicar incremento a los valores de Meli desde el índice especificado
        for i in range(inicio_incremento_meli, len(valoresMeliIncrementados)):
            valoresMeliIncrementados[i] = math.ceil(valoresMeli[i] + valoresMeli[i] * incremento_pct_meli / 100)

        for i in range(0, inicio_incremento_meli):
            valoresMeliIncrementados[i] = valoresMeli[i]      


        return valoresMeli, valoresMeliIncrementados

    reservasMeli, valoresMeliIncrementados = obtener_valores_por_fecha(fecha)

    def calcular_disponibilidad(configuracion):
        reservas = [Reserva(horariosReservas[i][0], horariosReservas[i][1]) for i, cantidad in enumerate(configuracion) for _ in range(round(cantidad))]
        disponibilidad = [sum(1 for reserva in reservas if reserva.horaDesde <= hora and reserva.horaHasta > hora) for hora in horarios]
        return disponibilidad

    def objetivo(config):
        disponibilidad = calcular_disponibilidad(config)
        if len(valoresMeliIncrementados) != len(disponibilidad):
            raise ValueError("Error: diferentes largos entre listas de disponibilidad meli-rapiboy")
        # return sum((rm - rd)**2 for rm, rd in zip(valoresMeliIncrementados, disponibilidad))##función costo. Acá hay que meter para que no haya mucho repartidor al dope.
        return sum((rm - rd)**2 for rm, rd in zip(valoresMeliIncrementados, disponibilidad)) + sum(config)

    def convertir_horas(value):
        hours = int(value)  # Parte entera para las horas
        minutes = int((value - hours) * 60)  # Parte decimal convertida a minutos
        
        # Formatear como HH:MM
        time_string = f"{hours:02d}:{minutes:02d}"
        
        return time_string


    valores_iniciales = [valoresMeliIncrementados[0]] * len(horariosReservas)
    bounds = [(0, None) for _ in range(len(valores_iniciales))] #Establezco limites de valores para cada turno. Inicio con todos positivos. Nunca reservas negativasd.
    # bounds[0] = (valoresMeliIncrementados[0], None) #Reemplazo el límite del primer horario dado que tengo que arrancar siempre con lo que pide meli, no puedo arrancar con 0 repas.
    # bounds = [(valoresMeliIncrementados[0], None) for _ in range(len(valores_iniciales))]
    resultado_optimizacion = minimize(objetivo, valores_iniciales, method='Powell', bounds=bounds)
    configuracionOptima = [int(x) for x in resultado_optimizacion.x] #convierto valores en enteros.

    if incremento_pct != 0:
        # Aplicar el incremento porcentual y redondear hacia arriba
        configuracionIncrementada = [math.ceil(x + x * incremento_pct / 100) for x in configuracionOptima]
    
    else:
        configuracionIncrementada = configuracionOptima

    Resultados = [{'horaDesde': convertir_horas(horariosReservas[i][0]), 'horaHasta': convertir_horas(horariosReservas[i][1]), 'cantidad': configuracionIncrementada[i]} for i in range(len(horariosReservas))]

    # Calcular la disponibilidad final usando la configuración incrementada
    disponibilidadFinal = calcular_disponibilidad(configuracionIncrementada)

    final = {
        "turnos": Resultados,
        "disponibilidadFinal": disponibilidadFinal,
        "necesidadesMeli": reservasMeli,
        "totalReservas" : sum(configuracionIncrementada)
    }

    return final
