
from .person import Person

class Alumno(Person):
    matricula: str
    promedio: float
    
    class Config:
        from_attributes = True