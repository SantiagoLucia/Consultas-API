from core.db import pool

def get_datos_usuario(nombre):

    q = 'SELECT * FROM CO_GED.DATOS_USUARIO WHERE USUARIO = :USUARIO'
    con = pool.acquire()
    cur = con.cursor()
    cur.execute(q, (nombre,))
    datos = cur.fetchall()
    columnas = [x[0] for x in cur.description]
    
    resultado = [dict(zip(columnas, fila)) for fila in datos]

    pool.release(con)
    return resultado


def get_usuarios_multireparticion(reparticion):

    q = """SELECT
SU.NOMBRE_USUARIO,
DU.APELLIDO_NOMBRE APELLIDO_NOMBRE,
(SELECT LISTAGG(R.CODIGO_REPARTICION, ',') WITHIN GROUP (ORDER BY R.CODIGO_REPARTICION)
FROM TRACK_GED.SADE_USR_REPA_HABILITADA H
INNER JOIN TRACK_GED.SADE_REPARTICION R ON (H.ID_REPARTICION = R.ID_REPARTICION)
WHERE H.NOMBRE_USUARIO = SU.NOMBRE_USUARIO
) AS REPARTICIONES_HABILITADAS    
FROM TRACK_GED.SADE_SECTOR_USUARIO SU 
LEFT JOIN TRACK_GED.SADE_SECTOR_INTERNO SSI ON (SU.ID_SECTOR_INTERNO = SSI.ID_SECTOR_INTERNO) 
LEFT JOIN TRACK_GED.SADE_REPARTICION SR ON (SSI.CODIGO_REPARTICION = SR.ID_REPARTICION) 
LEFT JOIN CO_GED.DATOS_USUARIO DU ON (DU.USUARIO = SU.NOMBRE_USUARIO)
WHERE SU.ESTADO_REGISTRO = 1 AND
SR.CODIGO_REPARTICION = :REPA
ORDER BY SU.NOMBRE_USUARIO"""
    con = pool.acquire()
    cur = con.cursor()
    cur.execute(q, (reparticion,))
    datos = cur.fetchall()
    columnas = [x[0] for x in cur.description]
    resultado = [dict(zip(columnas, fila)) for fila in datos]
    pool.release(con)
    return resultado