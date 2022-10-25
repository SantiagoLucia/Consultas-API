from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import usuario, expediente, estructura, gedo

app = FastAPI()

app.mount("/archivos", StaticFiles(directory="archivos"), name="archivos")

app.include_router(usuario.router)
app.include_router(expediente.router)
app.include_router(estructura.router)
app.include_router(gedo.router)

@app.get("/")
async def root():
    return {"API": "CONSULTAS BD"}


@app.get("/xlsx/{nombre}")
async def archivo(nombre: str):
    return FileResponse(f'./archivos/{nombre}.xlsx')