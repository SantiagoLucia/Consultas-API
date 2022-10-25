from fastapi import APIRouter, HTTPException
import servicios.gedo as gedo

router = APIRouter(prefix='/gedo', tags=['gedo'],)

@router.get('/tareas_por_usuario/{usuario}')
async def tareas(usuario: str):
    resp = gedo.get_tareas_usuario(usuario)
    if not resp:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return resp


@router.get('/gedos_firmados/{anio}-{reparticion}')
async def tareas(anio: int, reparticion: str):
    resp = gedo.get_gedos_firmados(anio, reparticion)
    if not resp:
        raise HTTPException(status_code=404, detail="No se encuentran documentos.")
    return resp