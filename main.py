from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import src.controllers as Controller

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

@app.get("/")
def read_root():
    return {"Proyecto Final": "API de escuela"}


app.include_router(
    Controller.alumnos
)
app.include_router(
    Controller.profesores
)