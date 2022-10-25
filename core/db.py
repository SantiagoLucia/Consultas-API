import cx_Oracle
from config import *

dsn_tns = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE)
pool = cx_Oracle.SessionPool(user=USER, password=PASSWORD, dsn=dsn_tns, encoding='windows-1252',
                        min = 1, max = 6, increment = 1, threaded = True,
                        getmode = cx_Oracle.SPOOL_ATTRVAL_WAIT)