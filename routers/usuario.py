from fastapi import APIRouter, HTTPException
import servicios.usuario as usuario

router = APIRouter(prefix='/usuario', tags=['usuario'],)

@router.get('/{nombre}')
async def datos_usuario(nombre: str):
    resp = usuario.get_datos_usuario(nombre)
    if not resp:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return resp


@router.get('/reparticiones_habilitadas/{reparticion}')
async def datos_usuario(reparticion: str):
    resp = usuario.get_usuarios_multireparticion(reparticion)
    if not resp:
        raise HTTPException(status_code=404, detail="No existen usuarios con multirepartición")
    return resp