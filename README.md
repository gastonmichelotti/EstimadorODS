
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
- `duracion`: La duración (en horas) de las reservas a crear.

Ejemplo de cuerpo de solicitud:

```json
{
    "fecha": "23/12",
    "duracion": 4
}
```

## Respuesta de la API

La API devolverá una respuesta JSON con los detalles de la estimación realizada. Cada objeto del JSON es un turno en el cual se indica la cantidad de reservas que se deben crear y el horarios de inicio y fin de las mismas.
