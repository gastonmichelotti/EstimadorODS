## Estimador simple implementado en api
def  estimar_simple_interface(fecha, 
            horario_desde=8, 
            horario_hasta=1.5,
            incremento_previo_meli=0, 
            incremento_previo_meli_desde=0,
            incremento_previo_meli_hasta=0,
            incremento_posterior_general=0):

    from Resources.Global import Reserva, load_credentials, consultaDB, obtener_forecast,calcular_disponibilidad, convertir_horas, estimar_simple
    from Resources.HorariosReservas import horariosReservas

    estimacion, dispoFinal, valoresMeli = estimar_simple(fecha, 
                                                        horario_desde, 
                                                        horario_hasta,
                                                        incremento_previo_meli, 
                                                        incremento_previo_meli_desde,
                                                        incremento_previo_meli_hasta,
                                                        incremento_posterior_general)

    return estimacion

