
# README para la API Estimador Nuevo ODS

## Descripción

Esta API proporciona funcionalidades para estimar reservas basadas en fechas y duraciones específicas. Está construida utilizando Python con Flask.

## Instalación

Para instalar y ejecutar esta API en su entorno local, siga estos pasos:

1. Asegúrese de tener Python instalado en su sistema.
2. Clone o descargue el proyecto en su máquina local.
3. Ejecutar "iniciar_api_portable.bat" que se encuentra en el directorio raíz del proyecto.
4. En caso de querer hacer la instalacion manual, instale las dependencias necesarias ejecutando el siguiente comando en la raíz del proyecto:
   
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar la API, utilice el siguiente comando en el directorio del proyecto:

```bash
python app.py
```

Esto iniciará el servidor Flask y la API estará disponible en `http://localhost:5001`.

## Uso de la API

Para hacer solicitudes a la API, envíe una solicitud POST a `http://localhost:5001/estimadorODS` con un cuerpo JSON que contenga los siguientes parámetros:

- `fecha`: La fecha para la cual se quiere hacer la estimación (en formato `DD/MM`).
- `duracion`: La duración (en horas) de las reservas a crear. Default = 4.
- `incremento_pct`: Incremento porcentual de la estimación al final de todo. Es el un margen de seguridad. Default = 5.
Ej: incremento_pct = 10, implica que para todos los horarios se tomara una estimación 10% mayor a la estimación estandar. 
- `incremento_pct_meli`: Incremento porcentual para aplicar de manera parcial en un rango de horarios. El incremento se aplica desde el intervalo horario que se indica en el parámetro `incremento_pct_meli`. Este incremento se toma desde origen, es decir que se simula que el forecaste de meli es un % mayor en ciertos horarios para corregir la estimación estandar. Luego, de esto se plaica el 'incremento_pct' en caso de ser != 0.
Default = 25
- `inicio_incremento_meli`: Intervalo horario desde el cual se palica el `incremento_pct_meli`. Este incremento se aplicará desde el valor parametrizado hasta el final del día. 
Default = 23.
NOTA: los intervalos van desde las 10:00 hasta las 24:00 en intervalos de 00:30. Por lo que por que, por ejemplo, el intervalo 21 corresponde a las 20:00 hs. 

Ejemplo de cuerpo de solicitud:

```json
{
    "fecha": "23/12",
    "duracion": 4,
    "incremento_pct": 10,
    "incremento_pct_meli": 25,
    "inicio_incremento_meli": 23
}
```

## Respuesta de la API

La API devolverá una respuesta JSON con los detalles de la estimación realizada. Cada objeto del JSON es un turno en el cual se indica la cantidad de reservas que se deben crear y el horarios de inicio y fin de las mismas.
