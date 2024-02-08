import pandas as pd
import requests
import numpy as np
from scipy.optimize import minimize
import math  # Asegúrate de tener esta importación para math.ceil

#parametros default hasta que javi modifique api y front para poder pasar estos nuevos params
def Estimar(fecha, duracion=4, incremento_pct=10, incremento_pct_meli=35, inicio_incremento_meli=21):
    class Reserva:
        def __init__(self, horaDesde, horaHasta):
            self.horaDesde = horaDesde
            self.horaHasta = horaHasta

    horarios = np.arange(10, 24, 0.5)
    horarioAux = np.arange(10, 25 - duracion, 1)
    horariosReservas = [(i, i + duracion) for i in horarioAux]

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
        return sum((rm - rd)**2 for rm, rd in zip(valoresMeliIncrementados, disponibilidad))

    valores_iniciales = [valoresMeliIncrementados[0]] * len(horariosReservas)
    bounds = [(valoresMeliIncrementados[0], None) for _ in range(len(valores_iniciales))]
    resultado_optimizacion = minimize(objetivo, valores_iniciales, method='Powell', bounds=bounds)
    configuracionOptima = [int(x) for x in resultado_optimizacion.x]

    # Aplicar el incremento porcentual y redondear hacia arriba
    configuracionIncrementada = [math.ceil(x + x * incremento_pct / 100) for x in configuracionOptima]

    Resultados = [{'horaDesde': f"{horariosReservas[i][0]:02d}:00", 'horaHasta': f"{horariosReservas[i][1]:02d}:00", 'cantidad': configuracionIncrementada[i]} for i in range(len(horariosReservas))]
    
    # Calcular la disponibilidad final usando la configuración incrementada
    disponibilidadFinal = calcular_disponibilidad(configuracionIncrementada)

    final = {
        "turnos": Resultados
        
    }

    return final
