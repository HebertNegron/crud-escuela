from fastapi import APIRouter, Depends, HTTPException, status
from src.migrations.db_tables import Alumno as DBAlumno
from src.models import Alumno
from sqlalchemy.orm import Session
from src.utils.database import get_db

alumnos = APIRouter(
    prefix='/alumnos',
    tags=['Alumnos']
)

@alumnos.get("", tags=["Alumnos"])
def get_alumnos(db: Session = Depends(get_db)):
    alumnos = db.query(DBAlumno).all()
    return alumnos

    
@alumnos.get("/{id}", tags=["Alumnos"])
def get_alumno(id: int, db: Session = Depends(get_db)):
    alumno = db.query(DBAlumno).filter(DBAlumno.id == id).first()
    if alumno:
        return alumno
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )

@alumnos.post("", tags=["Alumnos"], status_code=status.HTTP_201_CREATED)
def add_alumno(alumno: Alumno, db: Session = Depends(get_db)):
    db_alumno = DBAlumno(**alumno.model_dump())
    db.add(db_alumno)
    db.commit()
    return status.HTTP_201_CREATED

@alumnos.put("/{id}", tags=["Alumnos"])
def update_alumno(id: int, alumno: Alumno, db: Session = Depends(get_db)):
    alumno_dict = alumno.model_dump()
    alumno_dict.pop("id", None)
    alumno_update = db.query(DBAlumno).filter(DBAlumno.id == id)
    if alumno_update:
        alumno_update.update(alumno_dict)
        db.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
                )

@alumnos.delete("/{id}", tags=["Alumnos"])
def delete_alumno(id: int, db: Session = Depends(get_db)):
    alumno = db.query(DBAlumno).filter(DBAlumno.id == id).first()
    if alumno:
        db.delete(alumno)
        db.commit()
        return status.HTTP_200_OK
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )