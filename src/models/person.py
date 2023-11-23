from pydantic import BaseModel

class Person(BaseModel):
    id: int | None = None
    nombres: str
    apellidos: str