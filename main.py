from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import src.controllers as Controller
import src.migrations.db_tables as db_tables
from src.utils.database import SessionLocal, engine

def test_connection(engine):
    with engine.connect() as connection:
        assert connection.execute("SELECT 1").fetchone()[0] == 1

test_connection(engine)

db_tables.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

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