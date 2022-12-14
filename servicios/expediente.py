from core.db import pool

def get_sistema_apoderado(num):
    parametros = num.split('-')
    anio = parametros[1]
    numero = parametros[2]
    repa = parametros[5]
    q = 'SELECT SISTEMA_APODERADO FROM EE_GED.EE_EXPEDIENTE_ELECTRONICO \
        WHERE ANIO = :ANIO AND NUMERO = :NUMERO AND CODIGO_REPARTICION_USUARIO = :REPA'
    con = pool.acquire()
    cur = con.cursor()
    cur.execute(q, (anio, numero, repa,))
    datos = cur.fetchall()
    columnas = [x[0] for x in cur.description]
    resultado = [dict(zip(columnas, fila)) for fila in datos]
    pool.release(con)
    return resultado


def get_info_expediente(num):
    parametros = num.split('-')
    anio = parametros[1]
    numero = parametros[2]

    q = """SELECT  
'EX-'||EE.ANIO||'-'||EE.NUMERO||'- -GDEBA-'||EE.CODIGO_REPARTICION_USUARIO AS NRO_EXPEDIENTE, 
EE.CODIGO_REPARTICION_USUARIO AS COD_REPARTICION_CARATULACION,REP_CARATULA.NOMBRE_REPARTICION AS REPARTICION_CARATULACION, 
MIN_CARATULA.CODIGO_REPARTICION AS COD_ORGANISMO_CARATULACION,MIN_CARATULA.NOMBRE_REPARTICION AS ORGANISMO_CARATULACION, 
TO_CHAR(EE.FECHA_CREACION, 'DD/MM/YYYY') AS FECHA_CARATULACION,TO_CHAR(EE.FECHA_CREACION, 'HH24:MI:SS') AS HORA_CARATULACION,
TRATAS.CODIGO_TRATA,TRATAS.DESCRIPCION AS TRATA,REPLACE(EE.DESCRIPCION, CHR(10), ' ') AS DESCRIPCION,REPLACE(SOLEX.MOTIVO, CHR(10), ' ') AS MOTIVO,EE.ESTADO AS ESTADO_EXPEDIENTE,
NVL(REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 2),'simple') AS TIPO_TRAMITACION,REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1) AS USUARIO_ASIGNADO,
DU.APELLIDO_NOMBRE AS NOMBRE_APELLIDO,COALESCE(REGEXP_SUBSTR(REGEXP_SUBSTR(P.GROUPID_, '[^-]+', 1, 2),'[^.]+', 1, 1),SSI.CODIGO_SECTOR_INTERNO) AS SECTOR_ACTUAL,
REPFIN.CODIGO_REPARTICION AS COD_REPARTICION_ACTUAL,REPFIN.NOMBRE_REPARTICION AS REPARTICION_ACTUAL,MINFIN.CODIGO_REPARTICION AS COD_ORGANISMO_ACTUAL,  
MINFIN.NOMBRE_REPARTICION AS ORGANISMO_ACTUAL,EE.USUARIO_MODIFICACION,TO_CHAR(EE.FECHA_MODIFICACION, 'DD/MM/YYYY') AS FECHA_ULTIMA_MODIFICACION, 
TO_CHAR(EE.FECHA_MODIFICACION, 'HH24:MM:SS') AS HORA_ULTIMA_MODIFICACION,ROUND(SYSDATE - EE.FECHA_CREACION) AS DIAS_ABIERTO
FROM EE_GED.EE_EXPEDIENTE_ELECTRONICO EE LEFT JOIN EE_GED.SOLICITUD_EXPEDIENTE SOLEX ON SOLEX.ID = EE.SOLICITUD_INICIADORA
LEFT JOIN EE_GED.TRATA TRATAS ON TRATAS.ID = EE.ID_TRATA LEFT JOIN EE_GED.JBPM4_TASK T ON T.EXECUTION_ID_ = EE.ID_WORKFLOW
LEFT JOIN EE_GED.JBPM4_PARTICIPATION P ON P.TASK_ = T.DBID_   
--Caratulacion--
LEFT JOIN TRACK_GED.SADE_REPARTICION REP_CARATULA ON EE.CODIGO_REPARTICION_USUARIO = REP_CARATULA.CODIGO_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION MIN_CARATULA ON REP_CARATULA.MINISTERIO = MIN_CARATULA.ID_REPARTICION
--Esta asignado a usuario--
LEFT JOIN TRACK_GED.SADE_SECTOR_USUARIO SU ON REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1) = SU.NOMBRE_USUARIO
AND SU.ID_SECTOR_USUARIO =(SELECT MAX(Z.ID_SECTOR_USUARIO) FROM TRACK_GED.SADE_SECTOR_USUARIO Z 
WHERE Z.NOMBRE_USUARIO = REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1))
LEFT JOIN CO_GED.DATOS_USUARIO DU ON DU.USUARIO = SU.NOMBRE_USUARIO 
LEFT JOIN TRACK_GED.SADE_SECTOR_INTERNO SSI ON SU.ID_SECTOR_INTERNO = SSI.ID_SECTOR_INTERNO
LEFT JOIN TRACK_GED.SADE_REPARTICION SR ON SSI.CODIGO_REPARTICION = SR.ID_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION SR1 ON SR1.ID_REPARTICION = SR.MINISTERIO
--Sin asignar a usuario--
LEFT JOIN TRACK_GED.SADE_REPARTICION REPA ON REGEXP_SUBSTR(P.GROUPID_, '[^-]+', 1, 1) = REPA.CODIGO_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION MINISTERIO ON MINISTERIO.ID_REPARTICION = REPA.MINISTERIO
--Reparticion/Ministerio actual
LEFT JOIN TRACK_GED.SADE_REPARTICION REPFIN ON REPFIN.CODIGO_REPARTICION = COALESCE(SR.CODIGO_REPARTICION, REPA.CODIGO_REPARTICION)
LEFT JOIN TRACK_GED.SADE_REPARTICION MINFIN ON MINFIN.CODIGO_REPARTICION = COALESCE(SR1.CODIGO_REPARTICION, MINISTERIO.CODIGO_REPARTICION)
WHERE EE.ANIO = :ANIO AND EE.NUMERO = :NUMERO"""
    con = pool.acquire()
    cur = con.cursor()
    cur.execute(q, (anio, numero,))
    datos = cur.fetchall()
    columnas = [x[0] for x in cur.description]
    resultado = [dict(zip(columnas, fila)) for fila in datos]
    pool.release(con)
    return resultado


def get_caratulados_repa(anio, repa):
    q = """SELECT  
'EX-'||EE.ANIO||'-'||EE.NUMERO||'- -GDEBA-'||EE.CODIGO_REPARTICION_USUARIO AS NRO_EXPEDIENTE, 
EE.CODIGO_REPARTICION_USUARIO AS COD_REPARTICION_CARATULACION,REP_CARATULA.NOMBRE_REPARTICION AS REPARTICION_CARATULACION, 
MIN_CARATULA.CODIGO_REPARTICION AS COD_ORGANISMO_CARATULACION,MIN_CARATULA.NOMBRE_REPARTICION AS ORGANISMO_CARATULACION, 
TO_CHAR(EE.FECHA_CREACION, 'DD/MM/YYYY') AS FECHA_CARATULACION,TO_CHAR(EE.FECHA_CREACION, 'HH24:MI:SS') AS HORA_CARATULACION,
TRATAS.CODIGO_TRATA,TRATAS.DESCRIPCION AS TRATA,REPLACE(EE.DESCRIPCION, CHR(10), ' ') AS DESCRIPCION,REPLACE(SOLEX.MOTIVO, CHR(10), ' ') AS MOTIVO,EE.ESTADO AS ESTADO_EXPEDIENTE,
NVL(REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 2),'simple') AS TIPO_TRAMITACION,REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1) AS USUARIO_ASIGNADO,
DU.APELLIDO_NOMBRE AS NOMBRE_APELLIDO,COALESCE(REGEXP_SUBSTR(REGEXP_SUBSTR(P.GROUPID_, '[^-]+', 1, 2),'[^.]+', 1, 1),SSI.CODIGO_SECTOR_INTERNO) AS SECTOR_ACTUAL,
REPFIN.CODIGO_REPARTICION AS COD_REPARTICION_ACTUAL,REPFIN.NOMBRE_REPARTICION AS REPARTICION_ACTUAL,MINFIN.CODIGO_REPARTICION AS COD_ORGANISMO_ACTUAL,  
MINFIN.NOMBRE_REPARTICION AS ORGANISMO_ACTUAL,EE.USUARIO_MODIFICACION,TO_CHAR(EE.FECHA_MODIFICACION, 'DD/MM/YYYY') AS FECHA_ULTIMA_MODIFICACION, 
TO_CHAR(EE.FECHA_MODIFICACION, 'HH24:MM:SS') AS HORA_ULTIMA_MODIFICACION,ROUND(SYSDATE - EE.FECHA_CREACION) AS DIAS_ABIERTO
FROM EE_GED.EE_EXPEDIENTE_ELECTRONICO EE LEFT JOIN EE_GED.SOLICITUD_EXPEDIENTE SOLEX ON SOLEX.ID = EE.SOLICITUD_INICIADORA
LEFT JOIN EE_GED.TRATA TRATAS ON TRATAS.ID = EE.ID_TRATA LEFT JOIN EE_GED.JBPM4_TASK T ON T.EXECUTION_ID_ = EE.ID_WORKFLOW
LEFT JOIN EE_GED.JBPM4_PARTICIPATION P ON P.TASK_ = T.DBID_   
--Caratulacion--
LEFT JOIN TRACK_GED.SADE_REPARTICION REP_CARATULA ON EE.CODIGO_REPARTICION_USUARIO = REP_CARATULA.CODIGO_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION MIN_CARATULA ON REP_CARATULA.MINISTERIO = MIN_CARATULA.ID_REPARTICION
--Esta asignado a usuario--
LEFT JOIN TRACK_GED.SADE_SECTOR_USUARIO SU ON REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1) = SU.NOMBRE_USUARIO
AND SU.ID_SECTOR_USUARIO =(SELECT MAX(Z.ID_SECTOR_USUARIO) FROM TRACK_GED.SADE_SECTOR_USUARIO Z 
WHERE Z.NOMBRE_USUARIO = REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1))
LEFT JOIN CO_GED.DATOS_USUARIO DU ON DU.USUARIO = SU.NOMBRE_USUARIO 
LEFT JOIN TRACK_GED.SADE_SECTOR_INTERNO SSI ON SU.ID_SECTOR_INTERNO = SSI.ID_SECTOR_INTERNO
LEFT JOIN TRACK_GED.SADE_REPARTICION SR ON SSI.CODIGO_REPARTICION = SR.ID_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION SR1 ON SR1.ID_REPARTICION = SR.MINISTERIO
--Sin asignar a usuario--
LEFT JOIN TRACK_GED.SADE_REPARTICION REPA ON REGEXP_SUBSTR(P.GROUPID_, '[^-]+', 1, 1) = REPA.CODIGO_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION MINISTERIO ON MINISTERIO.ID_REPARTICION = REPA.MINISTERIO
--Reparticion/Ministerio actual
LEFT JOIN TRACK_GED.SADE_REPARTICION REPFIN ON REPFIN.CODIGO_REPARTICION = COALESCE(SR.CODIGO_REPARTICION, REPA.CODIGO_REPARTICION)
LEFT JOIN TRACK_GED.SADE_REPARTICION MINFIN ON MINFIN.CODIGO_REPARTICION = COALESCE(SR1.CODIGO_REPARTICION, MINISTERIO.CODIGO_REPARTICION)
WHERE EE.ANIO = :ANIO AND EE.CODIGO_REPARTICION_USUARIO = :REPA"""
    con = pool.acquire()
    cur = con.cursor()
    cur.execute(q, (anio, repa,))
    datos = cur.fetchall()
    columnas = [x[0] for x in cur.description]
    resultado = [dict(zip(columnas, fila)) for fila in datos]
    pool.release(con)
    return resultado


def get_caratulados_ministerio(anio, repa):
    q = """SELECT  
'EX-'||EE.ANIO||'-'||EE.NUMERO||'- -GDEBA-'||EE.CODIGO_REPARTICION_USUARIO AS NRO_EXPEDIENTE, 
EE.CODIGO_REPARTICION_USUARIO AS COD_REPARTICION_CARATULACION,REP_CARATULA.NOMBRE_REPARTICION AS REPARTICION_CARATULACION, 
MIN_CARATULA.CODIGO_REPARTICION AS COD_ORGANISMO_CARATULACION,MIN_CARATULA.NOMBRE_REPARTICION AS ORGANISMO_CARATULACION, 
TO_CHAR(EE.FECHA_CREACION, 'DD/MM/YYYY') AS FECHA_CARATULACION,TO_CHAR(EE.FECHA_CREACION, 'HH24:MI:SS') AS HORA_CARATULACION,
TRATAS.CODIGO_TRATA,TRATAS.DESCRIPCION AS TRATA,REPLACE(EE.DESCRIPCION, CHR(10), ' ') AS DESCRIPCION,REPLACE(SOLEX.MOTIVO, CHR(10), ' ') AS MOTIVO,EE.ESTADO AS ESTADO_EXPEDIENTE,
NVL(REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 2),'simple') AS TIPO_TRAMITACION,REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1) AS USUARIO_ASIGNADO,
DU.APELLIDO_NOMBRE AS NOMBRE_APELLIDO,COALESCE(REGEXP_SUBSTR(REGEXP_SUBSTR(P.GROUPID_, '[^-]+', 1, 2),'[^.]+', 1, 1),SSI.CODIGO_SECTOR_INTERNO) AS SECTOR_ACTUAL,
REPFIN.CODIGO_REPARTICION AS COD_REPARTICION_ACTUAL,REPFIN.NOMBRE_REPARTICION AS REPARTICION_ACTUAL,MINFIN.CODIGO_REPARTICION AS COD_ORGANISMO_ACTUAL,  
MINFIN.NOMBRE_REPARTICION AS ORGANISMO_ACTUAL,EE.USUARIO_MODIFICACION,TO_CHAR(EE.FECHA_MODIFICACION, 'DD/MM/YYYY') AS FECHA_ULTIMA_MODIFICACION, 
TO_CHAR(EE.FECHA_MODIFICACION, 'HH24:MM:SS') AS HORA_ULTIMA_MODIFICACION,ROUND(SYSDATE - EE.FECHA_CREACION) AS DIAS_ABIERTO
FROM EE_GED.EE_EXPEDIENTE_ELECTRONICO EE LEFT JOIN EE_GED.SOLICITUD_EXPEDIENTE SOLEX ON SOLEX.ID = EE.SOLICITUD_INICIADORA
LEFT JOIN EE_GED.TRATA TRATAS ON TRATAS.ID = EE.ID_TRATA LEFT JOIN EE_GED.JBPM4_TASK T ON T.EXECUTION_ID_ = EE.ID_WORKFLOW
LEFT JOIN EE_GED.JBPM4_PARTICIPATION P ON P.TASK_ = T.DBID_   
--Caratulacion--
LEFT JOIN TRACK_GED.SADE_REPARTICION REP_CARATULA ON EE.CODIGO_REPARTICION_USUARIO = REP_CARATULA.CODIGO_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION MIN_CARATULA ON REP_CARATULA.MINISTERIO = MIN_CARATULA.ID_REPARTICION
--Esta asignado a usuario--
LEFT JOIN TRACK_GED.SADE_SECTOR_USUARIO SU ON REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1) = SU.NOMBRE_USUARIO
AND SU.ID_SECTOR_USUARIO =(SELECT MAX(Z.ID_SECTOR_USUARIO) FROM TRACK_GED.SADE_SECTOR_USUARIO Z 
WHERE Z.NOMBRE_USUARIO = REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1))
LEFT JOIN CO_GED.DATOS_USUARIO DU ON DU.USUARIO = SU.NOMBRE_USUARIO 
LEFT JOIN TRACK_GED.SADE_SECTOR_INTERNO SSI ON SU.ID_SECTOR_INTERNO = SSI.ID_SECTOR_INTERNO
LEFT JOIN TRACK_GED.SADE_REPARTICION SR ON SSI.CODIGO_REPARTICION = SR.ID_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION SR1 ON SR1.ID_REPARTICION = SR.MINISTERIO
--Sin asignar a usuario--
LEFT JOIN TRACK_GED.SADE_REPARTICION REPA ON REGEXP_SUBSTR(P.GROUPID_, '[^-]+', 1, 1) = REPA.CODIGO_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION MINISTERIO ON MINISTERIO.ID_REPARTICION = REPA.MINISTERIO
--Reparticion/Ministerio actual
LEFT JOIN TRACK_GED.SADE_REPARTICION REPFIN ON REPFIN.CODIGO_REPARTICION = COALESCE(SR.CODIGO_REPARTICION, REPA.CODIGO_REPARTICION)
LEFT JOIN TRACK_GED.SADE_REPARTICION MINFIN ON MINFIN.CODIGO_REPARTICION = COALESCE(SR1.CODIGO_REPARTICION, MINISTERIO.CODIGO_REPARTICION)
WHERE EE.ANIO = :ANIO AND MIN_CARATULA.CODIGO_REPARTICION = :REPA"""
    con = pool.acquire()
    cur = con.cursor()
    cur.execute(q, (anio, repa,))
    datos = cur.fetchall()
    columnas = [x[0] for x in cur.description]
    resultado = [dict(zip(columnas, fila)) for fila in datos]
    pool.release(con)
    return resultado


def get_transito_repa(repa):
    q = """SELECT  
'EX-'||EE.ANIO||'-'||EE.NUMERO||'- -GDEBA-'||EE.CODIGO_REPARTICION_USUARIO AS NRO_EXPEDIENTE, 
EE.CODIGO_REPARTICION_USUARIO AS COD_REPARTICION_CARATULACION,REP_CARATULA.NOMBRE_REPARTICION AS REPARTICION_CARATULACION, 
MIN_CARATULA.CODIGO_REPARTICION AS COD_ORGANISMO_CARATULACION,MIN_CARATULA.NOMBRE_REPARTICION AS ORGANISMO_CARATULACION, 
TO_CHAR(EE.FECHA_CREACION, 'DD/MM/YYYY') AS FECHA_CARATULACION,TO_CHAR(EE.FECHA_CREACION, 'HH24:MI:SS') AS HORA_CARATULACION,
TRATAS.CODIGO_TRATA,TRATAS.DESCRIPCION AS TRATA,REPLACE(EE.DESCRIPCION, CHR(10), ' ') AS DESCRIPCION,REPLACE(SOLEX.MOTIVO, CHR(10), ' ') AS MOTIVO,EE.ESTADO AS ESTADO_EXPEDIENTE,
NVL(REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 2),'simple') AS TIPO_TRAMITACION,REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1) AS USUARIO_ASIGNADO,
DU.APELLIDO_NOMBRE AS NOMBRE_APELLIDO,COALESCE(REGEXP_SUBSTR(REGEXP_SUBSTR(P.GROUPID_, '[^-]+', 1, 2),'[^.]+', 1, 1),SSI.CODIGO_SECTOR_INTERNO) AS SECTOR_ACTUAL,
REPFIN.CODIGO_REPARTICION AS COD_REPARTICION_ACTUAL,REPFIN.NOMBRE_REPARTICION AS REPARTICION_ACTUAL,MINFIN.CODIGO_REPARTICION AS COD_ORGANISMO_ACTUAL,  
MINFIN.NOMBRE_REPARTICION AS ORGANISMO_ACTUAL,EE.USUARIO_MODIFICACION,TO_CHAR(EE.FECHA_MODIFICACION, 'DD/MM/YYYY') AS FECHA_ULTIMA_MODIFICACION, 
TO_CHAR(EE.FECHA_MODIFICACION, 'HH24:MM:SS') AS HORA_ULTIMA_MODIFICACION,ROUND(SYSDATE - EE.FECHA_CREACION) AS DIAS_ABIERTO
FROM EE_GED.EE_EXPEDIENTE_ELECTRONICO EE LEFT JOIN EE_GED.SOLICITUD_EXPEDIENTE SOLEX ON SOLEX.ID = EE.SOLICITUD_INICIADORA
LEFT JOIN EE_GED.TRATA TRATAS ON TRATAS.ID = EE.ID_TRATA LEFT JOIN EE_GED.JBPM4_TASK T ON T.EXECUTION_ID_ = EE.ID_WORKFLOW
LEFT JOIN EE_GED.JBPM4_PARTICIPATION P ON P.TASK_ = T.DBID_   
--Caratulacion--
LEFT JOIN TRACK_GED.SADE_REPARTICION REP_CARATULA ON EE.CODIGO_REPARTICION_USUARIO = REP_CARATULA.CODIGO_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION MIN_CARATULA ON REP_CARATULA.MINISTERIO = MIN_CARATULA.ID_REPARTICION
--Esta asignado a usuario--
LEFT JOIN TRACK_GED.SADE_SECTOR_USUARIO SU ON REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1) = SU.NOMBRE_USUARIO
AND SU.ID_SECTOR_USUARIO =(SELECT MAX(Z.ID_SECTOR_USUARIO) FROM TRACK_GED.SADE_SECTOR_USUARIO Z 
WHERE Z.NOMBRE_USUARIO = REGEXP_SUBSTR(T.ASSIGNEE_, '[^.]+', 1, 1))
LEFT JOIN CO_GED.DATOS_USUARIO DU ON DU.USUARIO = SU.NOMBRE_USUARIO 
LEFT JOIN TRACK_GED.SADE_SECTOR_INTERNO SSI ON SU.ID_SECTOR_INTERNO = SSI.ID_SECTOR_INTERNO
LEFT JOIN TRACK_GED.SADE_REPARTICION SR ON SSI.CODIGO_REPARTICION = SR.ID_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION SR1 ON SR1.ID_REPARTICION = SR.MINISTERIO
--Sin asignar a usuario--
LEFT JOIN TRACK_GED.SADE_REPARTICION REPA ON REGEXP_SUBSTR(P.GROUPID_, '[^-]+', 1, 1) = REPA.CODIGO_REPARTICION
LEFT JOIN TRACK_GED.SADE_REPARTICION MINISTERIO ON MINISTERIO.ID_REPARTICION = REPA.MINISTERIO
--Reparticion/Ministerio actual
LEFT JOIN TRACK_GED.SADE_REPARTICION REPFIN ON REPFIN.CODIGO_REPARTICION = COALESCE(SR.CODIGO_REPARTICION, REPA.CODIGO_REPARTICION)
LEFT JOIN TRACK_GED.SADE_REPARTICION MINFIN ON MINFIN.CODIGO_REPARTICION = COALESCE(SR1.CODIGO_REPARTICION, MINISTERIO.CODIGO_REPARTICION)
WHERE REPFIN.CODIGO_REPARTICION = :REPA AND EE.ESTADO != 'Guarda Temporal'"""
    con = pool.acquire()
    cur = con.cursor()
    cur.execute(q, (repa,))
    datos = cur.fetchall()
    columnas = [x[0] for x in cur.description]
    resultado = [dict(zip(columnas, fila)) for fila in datos]
    pool.release(con)
    return resultado


def get_buzon_usuario(usuario):
    q = """SELECT
'EX-'||EE.ANIO||'-'||EE.NUMERO||'-GDEBA- -'||EE.CODIGO_REPARTICION_USUARIO AS NRO_EXPEDIENTE,
TO_CHAR(EE.FECHA_CREACION,'DD/MM/YYYY') AS FECHA_CARATULACION,
TO_CHAR(EE.FECHA_MODIFICACION,'DD/MM/YYYY') AS ULTIMA_MODIFICACION,
EE.ESTADO FROM EE_GED.JBPM4_TASK T
INNER JOIN EE_GED.EE_EXPEDIENTE_ELECTRONICO EE ON EE.ID_WORKFLOW = T.EXECUTION_ID_
WHERE REGEXP_SUBSTR(ASSIGNEE_, '[^.]+', 1, 1) = :USUARIO"""
    con = pool.acquire()
    cur = con.cursor()
    cur.execute(q, (usuario,))
    datos = cur.fetchall()
    columnas = [x[0] for x in cur.description]
    resultado = [dict(zip(columnas, fila)) for fila in datos]
    pool.release(con)
    return resultado