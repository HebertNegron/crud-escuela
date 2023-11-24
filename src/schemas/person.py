from pydantic import BaseModel, Field

class Person(BaseModel):
    id: int | None = None
    nombres: str = Field('')
    apellidos: str = Field('')