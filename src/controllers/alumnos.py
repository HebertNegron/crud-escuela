from fastapi import APIRouter, HTTPException, status
from src.models import Alumno

alumnos = APIRouter(
    prefix='/alumnos',
    tags=['Alumnos']
)

lista_alumnos: list[Alumno] = []

@alumnos.get("", tags=["Alumnos"])
def get_alumnos():
    return lista_alumnos

@alumnos.get("/{id}", tags=["Alumnos"])
def get_alumno(id: int):
    for alumno in lista_alumnos:
        if alumno.id == id:
            return alumno
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )

@alumnos.post("", tags=["Alumnos"], status_code=status.HTTP_201_CREATED)
def add_alumno(alumno: Alumno):
    lista_alumnos.append(alumno)
    return status.HTTP_201_CREATED

@alumnos.put("/{id}", tags=["Alumnos"])
def update_alumno(id: int, alumno: Alumno):
    for i in range(len(lista_alumnos)):
        if lista_alumnos[i].id == id:
            lista_alumnos[i] = alumno
            return status.HTTP_201_CREATED
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )

@alumnos.delete("/{id}", tags=["Alumnos"])
def delete_alumno(id: int):
    for i in range(len(lista_alumnos)):
        if lista_alumnos[i].id == id:
            lista_alumnos.pop(i)
            return status.HTTP_201_CREATED
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )