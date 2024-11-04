# README para la API Estimador Nuevo ODS

## Descripción

Esta API proporciona funcionalidades para estimar reservas basadas en fechas y duraciones específicas. Está construida utilizando Python con Flask.

## Instalación

Para instalar y ejecutar esta API en su entorno local, siga estos pasos:

1. Asegúrese de tener Python instalado en su sistema.
2. Clone o descargue el proyecto en su máquina local.
3. Ejecute "iniciar_api_portable.bat" que se encuentra en el directorio raíz del proyecto.
4. En caso de querer hacer la instalación manual, instale las dependencias necesarias ejecutando el siguiente comando en la raíz del proyecto:
   
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

- `fecha`: La fecha para la cual se quiere hacer la estimación (en formato `DD/MM/YYYY`).
- `incremento_previo_meli`: Porcentaje de incremento previo aplicado al forecast de Meli en un rango específico de horarios. Default = 0.
- `incremento_previo_meli_desde`: Intervalo horario desde el cual se aplica el `incremento_previo_meli`. Default = 19. 
- `incremento_previo_meli_hasta`: Intervalo horario hasta el cual se aplica el `incremento_previo_meli`.  Default = 1.5. 
- `incremento_posterior_general`: Porcentaje de incremento aplicado a toda la configuración final. Default = 0.

### Ejemplo de cuerpo de solicitud:

```json
{
    "fecha": "2/10/2024", ##Fecha
    "horaDesde": 8, 
    "horaHasta": 1.5,
    "incremento_previo_meli": 0, 
    "incremento_previo_meli_desde": 0,  
    "incremento_previo_meli_hasta": 0,
    "incremento_posterior_general": 0  
}
```

## Respuesta de la API

La API devolverá una respuesta JSON con los detalles de la estimación realizada. El objeto JSON incluirá:

- `fecha`: La fecha de la estimación.
- `turnos`: Una lista de objetos, donde cada objeto representa un turno y contiene:
  - `horaDesde`: El horario de inicio del turno.
  - `horaHasta`: El horario de fin del turno.
  - `cantidad`: La cantidad de reservas recomendadas para ese turno.

### Ejemplo de respuesta:

```json
{
    "fecha": "02/10/2024",
    "turnos": [
        {
            "horaDesde": "08:00",
            "horaHasta": "11:00",
            "cantidad": 15
            
        },
        {
            "horaDesde": "11:00",
            "horaHasta": "14:00",
            "cantidad": 20
        }
    ]
}
```

Cada turno detalla las recomendaciones de reservas y sus horarios correspondientes.
