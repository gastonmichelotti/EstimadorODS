
def generarQuery(fecha):

    from datetime import datetime

    fechafix = datetime.strptime(fecha, '%d/%m/%Y')
    fecha_formateada = fechafix.strftime('%Y-%m-%d')

    queryReservasxHora = f"""

    DECLARE @Fecha DATE = '{fecha_formateada}';
   
    WITH Horarios AS (
    
        SELECT 
        CAST(@Fecha AS DATETIME) + CAST('08:00' AS DATETIME) AS Horario
        UNION ALL
        SELECT DATEADD(MINUTE, 30, Horario)
        FROM Horarios
        WHERE DATEADD(MINUTE, 30, Horario) <= DATEADD(DAY, 1, CAST(@Fecha AS DATETIME)) + CAST('01:00' AS DATETIME)
    )

    SELECT
 	    CAST(H.Horario AS DATE) Fecha,
        FORMAT(H.Horario, 'HH:mm') AS Horario,
        COUNT(R.Id) AS TotalReservas,
        --COUNT(CASE WHEN R.FechaLlego IS NOT NULL THEN 1 END) AS ReservasConLlegada
        COUNT(CASE WHEN R.idmotoboy IS NOT NULL THEN 1 END) AS ReservasConLlegada
    FROM
        Horarios H
    LEFT JOIN
        ReservaxMotoboy R ON R.FechaDesde <= H.Horario AND R.FechaHasta > H.Horario
        AND R.fecha = @Fecha
        AND R.idusuario = 23317
        AND R.cancelada = 0
    GROUP BY
    	CAST(H.Horario AS DATE),
        FORMAT(H.Horario, 'HH:mm')
    ORDER BY
    	CAST(H.Horario AS DATE),
        FORMAT(H.Horario, 'HH:mm');

    """

    return queryReservasxHora


def buscarAutomaticas(fecha):

    from datetime import datetime

    fechafix = datetime.strptime(fecha, '%d/%m/%Y')
    fecha_formateada = fechafix.strftime('%Y-%m-%d')

    queryautomaticas = f"""

    DECLARE @Fecha DATE = '{fecha_formateada}';
   
    SELECT
    DATEPART(hour, r.fechaDesde) AS Desde,
    FORMAT(r.fechaDesde, 'HH:mm') AS HoraDesde,
    DATEPART(hour, r.fechaHasta) AS Hasta,
    FORMAT(r.fechaHasta, 'H:mm') AS HoraHasta,
    COUNT(r.id) AS Cantidad
    FROM 
    reservaxmotoboy r 
    WHERE 
    idusuario = 23317
    AND r.fecha = @Fecha
    AND cancelada = 0
    GROUP BY
    DATEPART(hour, r.fechaDesde),
    FORMAT(r.fechaDesde, 'HH:mm'),
    DATEPART(hour, r.fechaHasta),
    FORMAT(r.fechaHasta, 'H:mm');

    """

    return queryautomaticas
