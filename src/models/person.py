from pydantic import BaseModel

class Person(BaseModel):
    id: int
    nombres: str
    apellidos: str