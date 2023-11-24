from pydantic import Field
from .person import Person

class Teacher(Person):
    numeroEmpleado: int = Field("")
    horasClase: int = Field("")

    class Config:
        from_attributes = True