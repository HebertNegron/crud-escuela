from .person import Person
from pydantic import Field

class Alumno(Person):
    matricula: str = Field('')
    promedio: float = Field(0)
    fotoPerfilUrl: str | None = None
    password: str = Field('')
    
    class Config:
        from_attributes = True