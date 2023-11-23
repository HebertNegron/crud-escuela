from fastapi import APIRouter, Depends, HTTPException, status
from src.migrations.db_tables import Profesor
from sqlalchemy.orm import Session
from src.utils.database import get_db

profesores = APIRouter(
    prefix='/profesores',
    tags=['Profesores'],
    include_in_schema=False
)

@profesores.get("", tags=["Profesores"])
def get_profesores(db: Session = Depends(get_db)):
    profesores = db.query(Profesor).all()
    return profesores

@profesores.get("/{id}", tags=["Profesores"])
def get_profesor(id: int, db: Session = Depends(get_db)):
    profesor = db.query(Profesor).filter(Profesor.id == id).first()
    if profesor:
        return profesor
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
            )

@profesores.post("", tags=["Profesores"], status_code=status.HTTP_201_CREATED)
def add_profesor(profesor: Profesor, db: Session = Depends(get_db)):
    db.add(profesor)
    db.commit()
    db.refresh(profesor)
    return status.HTTP_201_CREATED

@profesores.put("/{id}", tags=["Profesores"])
def update_profesor(id: int, profesor: Profesor, db: Session = Depends(get_db)):
    profesor_update = db.query(Profesor).filter(Profesor.id == id).first()
    if profesor_update:
        profesor_update = profesor
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
            )

@profesores.delete("/{id}", tags=["Profesores"])
def delete_profesor(id: int, db: Session = Depends(get_db)):
    profesor = db.query(Profesor).filter(Profesor.id == id).first()
    if profesor:
        db.delete(profesor)
        db.commit()
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
            )