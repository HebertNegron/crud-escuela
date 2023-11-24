from fastapi import APIRouter, Body, Depends, File, UploadFile
from src.schemas import Student
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services import StudentsService


students = APIRouter(
    prefix='/alumnos',
    tags=['Alumnos']
)

@students.get("", tags=["Alumnos"])
def get_students(db: Session = Depends(get_db)):
    return StudentsService().get_students(db)

    
@students.get("/{id}", tags=["Alumnos"])
def get_student(id: int,  db: Session = Depends(get_db)):
    return StudentsService().get_student(id, db)

@students.post("", tags=["Alumnos"])
def add_student(student: Student, db: Session = Depends(get_db)):
    return StudentsService().add_student(student, db)

@students.put("/{id}", tags=["Alumnos"])
def update_student(id: int, student: Student, db: Session = Depends(get_db)):
    return StudentsService().update_student(id, student, db)

@students.delete("/{id}", tags=["Alumnos"])
def delete_student(id: int, db: Session = Depends(get_db)):
    return StudentsService().delete_student(id, db)
    
@students.post("/{id}/fotoPerfil", tags=["Alumnos"])
def upload_foto_perfil(id :int, foto: UploadFile = File(...), db: Session = Depends(get_db)):
    return StudentsService().upload_profile_picture(id, foto, db)

@students.post("/{id}/email", tags=["Alumnos"])
def send_email(id: int, db: Session = Depends(get_db)):
    return StudentsService().send_email(id, db)
    
@students.post("/{id}/session/login", tags=["Alumnos"])
def login(id: int, password: str = Body(embed=True), db: Session = Depends(get_db)):
    return StudentsService().login(id, password, db)
  

@students.post("/{id}/session/verify", tags=["Alumnos"])
def verify(id: int, sessionString:str = Body(embed=True), db: Session = Depends(get_db)):
    return StudentsService().verify_session(id, sessionString, db)
    
@students.post("/{id}/session/logout", tags=["Alumnos"])
def logout(id: int, sessionString: str = Body(embed=True), db: Session = Depends(get_db)):
    return StudentsService().logout(id, sessionString, db)