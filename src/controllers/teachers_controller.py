from fastapi import APIRouter, Depends
from src.schemas import Teacher
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services import TeachersService

teachers = APIRouter(
    prefix='/profesores',
    tags=['Profesores'],
    include_in_schema=False
)

@teachers.get("", tags=["Profesores"])
def get_teachers(db: Session = Depends(get_db)):
    return TeachersService().get_teachers(db)

@teachers.get("/{id}", tags=["Profesores"])
def get_teacher(id: int, db: Session = Depends(get_db)):
    return TeachersService().get_teacher(id, db)

@teachers.post("", tags=["Profesores"])
def add_teacher(teacher: Teacher, db: Session = Depends(get_db)):
    return TeachersService().add_teacher(teacher, db)

@teachers.put("/{id}", tags=["Profesores"])
def update_teacher(id: int, teacher: Teacher, db: Session = Depends(get_db)):
    return TeachersService().update_teacher(id, teacher, db)

@teachers.delete("/{id}", tags=["Profesores"])
def delete_teacher(id: int, db: Session = Depends(get_db)):
    return TeachersService().delete_teacher(id, db)