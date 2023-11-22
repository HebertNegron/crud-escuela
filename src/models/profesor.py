from .person import Person

class Profesor(Person):
    numeroEmpleado: int
    horasClase: int

    class Config:
        from_attributes = True