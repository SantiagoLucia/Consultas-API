from fastapi import APIRouter, HTTPException
import servicios.expediente as expediente


router = APIRouter(prefix='/expedientes', tags=['expediente'],)


@router.get('/sistema_apoderado/{numero}')
async def sistema_apoderado(numero: str):
    resp = expediente.get_sistema_apoderado(numero)
    if not resp:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return resp


@router.get('/{numero}')
async def info_expediente(numero: str):
    resp = expediente.get_info_expediente(numero)
    if not resp:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return resp


@router.get('/caratulados_reparticion/{anio}-{repa}')
async def caratulados_por_reparticion(anio: int, repa: str):
    resp = expediente.get_caratulados_repa(anio, repa)
    if not resp:
        raise HTTPException(status_code=404, detail="Expedientes no encontrados")
    return resp


@router.get('/caratulados_ministerio/{anio}-{min}')
async def caratulados_por_ministerio(anio: int, min: str):
    resp = expediente.get_caratulados_ministerio(anio, min)
    if not resp:
        raise HTTPException(status_code=404, detail="Expedientes no encontrados")
    return resp


@router.get('/transito_repa/{repa}')
async def transito_en_reparticion(repa: str):
    resp = expediente.get_transito_repa(repa)
    if not resp:
        raise HTTPException(status_code=404, detail="Expedientes no encontrados")
    return resp


@router.get('/buzon_usuario/{usuario}')
async def buzon_usuario(usuario: str):
    resp = expediente.get_buzon_usuario(usuario)
    if not resp:
        raise HTTPException(status_code=404, detail="Expedientes no encontrados")
    return resp