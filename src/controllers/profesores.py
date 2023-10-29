from fastapi import APIRouter, HTTPException, status
from src.models import Profesor

profesores = APIRouter(
    prefix='/profesores',
    tags=['Profesores'],
    include_in_schema=False
)

lista_profesores: list[Profesor] = []

@profesores.get("", tags=["Profesores"])
def get_profesores():
    return lista_profesores

@profesores.get("/{id}", tags=["Profesores"])
def get_profesor(id: int):
    for profesor in lista_profesores:
        if profesor.id == id:
            return profesor
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )

@profesores.post("", tags=["Profesores"], status_code=status.HTTP_201_CREATED)
def add_profesor(profesor: Profesor):
    lista_profesores.append(profesor)
    return status.HTTP_201_CREATED

@profesores.put("/{id}", tags=["Profesores"])   
def update_profesor(id: int, profesor: Profesor):
    for i in range(len(lista_profesores)):
        if lista_profesores[i].id == id:
            lista_profesores[i] = profesor
            return status.HTTP_201_CREATED
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )

@profesores.delete("/{id}", tags=["Profesores"])
def delete_profesor(id: int):
    for i in range(len(lista_profesores)):
        if lista_profesores[i].id == id:
            lista_profesores.pop(i)
            return status.HTTP_201_CREATED
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )