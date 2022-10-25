from fastapi import APIRouter, HTTPException
import servicios.estructura as estructura


router = APIRouter(prefix='/estructura', tags=['estructura'],)


@router.get('/{reparticion}')
async def obtener_estructura(reparticion: str):
    resp = estructura.get_estructura(reparticion)
    if not resp:
        raise HTTPException(status_code=404, detail="No existe el código de repartición.")
    return resp