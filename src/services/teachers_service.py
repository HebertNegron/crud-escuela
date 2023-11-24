from fastapi import HTTPException, status
from fastapi.params import Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.models.db_tables import DBTeacher
from src.schemas.teacher import Teacher
from src.utils.functions import success_response


class TeachersService:
    
    def get_teachers(self, db: Session) -> list:
        teachers: DBTeacher | None = db.query(DBTeacher).all()
        return teachers
    
    def get_teacher(self, id: int, db: Session) -> DBTeacher:
        teacher: DBTeacher | None = db.query(DBTeacher).filter(DBTeacher.id == id).first()
        if not teacher:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profesor no encontrado"
                )
        return teacher
    
    def add_teacher(self, teacher: Teacher, db: Session) -> int:
        db_teacher: DBTeacher = DBTeacher(**teacher.model_dump())
        db.add(db_teacher)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": db_teacher.id
            }
        )
    
    def update_teacher(self, id: int, teacher: Teacher, db: Session) -> JSONResponse:
        teacher_dict: dict = teacher.model_dump()
        teacher_dict.pop("id", None)
        teacher_update: Query[DBTeacher] = db.query(DBTeacher).filter(DBTeacher.id == id)
        if teacher_update:
            teacher_update.update(teacher_dict)
            db.commit()
            return success_response("Profesor actualizado")
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
                )
    
    def delete_teacher(self, id: int, db: Session) -> JSONResponse:
        teacher: Query[DBTeacher] = TeachersService().get_teacher(id, db)
        if teacher:
            db.delete(teacher)
            db.commit()
            return success_response("Profesor eliminado")
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
                )