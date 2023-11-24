from tempfile import NamedTemporaryFile
import time
import uuid
from fastapi.params import Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.schemas import Student
from src.models import DBStudent
from fastapi import HTTPException, UploadFile, status
from src.utils.aws import publish_message_to_sns, put_item_to_dynamodb, scan_table, update_item_in_dynamodb, upload_file_to_s3
from src.utils.functions import get_random_string, success_response
from os import environ as env
from boto3.dynamodb.conditions import Attr

class StudentsService:

    def get_students(self, db: Session) -> list:
        students: DBStudent | None = db.query(DBStudent).all()
        return students
    
    def get_student(self, id: int, db:Session) -> DBStudent:
        student: DBStudent | None = db.query(DBStudent).filter(DBStudent.id == id).first()
        if not student:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alumno no encontrado"
                )
        return student

    def add_student(self, student: Student, db: Session) -> JSONResponse:
        db_student: DBStudent = DBStudent(**student.model_dump())
        db.add(db_student)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": db_student.id
            }
        )

    def update_student(self, id: int, student: Student, db: Session) -> JSONResponse:
        student_dict: dict = student.model_dump()
        student_dict.pop("id", None)
        student_update: Query[DBStudent] = db.query(DBStudent).filter(DBStudent.id == id)
        if student_update:
            student_update.update(student_dict)
            db.commit()
            return success_response("Alumno actualizado")
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
                )
    
    def delete_student(self, id: int, db: Session) -> JSONResponse:
        student: Query[DBStudent] = StudentsService().get_student(id, db)
        if student:
            db.delete(student)
            db.commit()
            return success_response("Alumno eliminado")
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
                )
    

    def upload_profile_picture(self, id: int, photo: UploadFile, db: Session) -> JSONResponse:
        student: DBStudent = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alumno no encontrado"
                )
        try:
            with NamedTemporaryFile(delete=False) as tmp:
                tmp.write(photo.file.read())
                file = tmp.name
                filename = photo.filename
                upload_file_to_s3(file, filename)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al subir imagen"
            )
        student.fotoPerfilUrl = f"https://{env.get('BUCKET_NAME')}.s3.amazonaws.com/{filename}"
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "fotoPerfilUrl": student.fotoPerfilUrl
            }
        )
            
        
    def send_email(self, id: int, db: Session) -> JSONResponse:
        student: DBStudent = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alumno no encontrado"
                )
        publish_message_to_sns(
            topic_arn=env.get("TOPIC_ARN"),
            message=f"Nombre: {student.nombres}\nApellido: {student.apellidos}\nCalificaciones: {student.promedio}"
        )
        return success_response("Correo enviado")
            
        
    def login(self, id: int, password: str, db: Session) -> JSONResponse:
        student: Query[DBStudent] = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alumno no encontrado"
                )
        if student.password != password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña incorrecta"
            )
        sessionString: str = get_random_string(128)
        put_item_to_dynamodb(
            table_name=env.get('DYNAMODB_TABLE'),
            item={
                'id': str(uuid.uuid4()),
                'fecha': int(time.time()),
                'alumnoId': id,
                'active': True,
                'sessionString': sessionString
            }
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "sessionString": sessionString
            }
        )
            
            
        
    def verify_session(self, id: int, sessionString: str, db: Session) -> JSONResponse:
        student: DBStudent = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        response: list[dict] | list = scan_table(
            table_name=env.get('DYNAMODB_TABLE'),
            filter_expression=Attr('sessionString').eq(sessionString)
        )
        if response:
            is_active = response[0].get('active', False)
        if not response or not is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
        return success_response("Sesión válida")
        
    
    def logout(self, id: int, sessionString: str, db: Session) -> JSONResponse:
        student: DBStudent = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        response: list[dict] = scan_table(
            table_name=env.get('DYNAMODB_TABLE'),
            filter_expression=Attr('sessionString').eq(sessionString)
        )
        id = response[0].get('id', False)
        if not response or not id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
        update_item_in_dynamodb(
            table_name=env.get('DYNAMODB_TABLE'),
            key={
                'id': id
            },
            update_expression='SET active = :active',
            expression_attribute_values={
                ':active': False
            }
        )
        return success_response("Sesión cerrada")
    