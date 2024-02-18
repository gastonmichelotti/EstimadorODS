
def generarQuery(fecha):

    from datetime import datetime

    fechafix = datetime.strptime(fecha + '/' + '2024', '%d/%m/%Y')
    fecha_formateada = fechafix.strftime('%Y-%m-%d')

    queryReservasxHora = f"""

    DECLARE @Fecha DATE = '{fecha_formateada}';

    WITH Horarios AS (
        SELECT CAST(@Fecha AS DATETIME) + CAST('10:00' AS DATETIME) AS Horario
        UNION ALL
        SELECT DATEADD(MINUTE, 30, Horario)
        FROM Horarios
        WHERE DATEADD(MINUTE, 30, Horario) <= CAST(@Fecha AS DATETIME) + CAST('23:30' AS DATETIME)
    )

    SELECT
        FORMAT(H.Horario, 'HH:mm') AS Horario,  -- Aquí se aplica el formato deseado
        COUNT(R.Id) AS TotalReservas,
        COUNT(CASE WHEN R.FechaLlego IS NOT NULL THEN 1 END) AS ReservasConLlegada
    FROM
        Horarios H
    LEFT JOIN
        ReservaxMotoboy R ON R.FechaDesde <= H.Horario AND R.FechaHasta > H.Horario
        AND R.fecha = @Fecha  -- Asegúrate de que este filtro se aplique correctamente
        AND R.idusuario = 23317
        AND R.cancelada = 0
    GROUP BY
        FORMAT(H.Horario, 'HH:mm')  -- Es necesario agrupar por el valor formateado también


    """

    return queryReservasxHora
