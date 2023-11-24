import logging
from tempfile import NamedTemporaryFile
import time
import uuid
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from src.migrations.db_tables import Alumno as DBAlumno
from src.models import Alumno
from sqlalchemy.orm import Session
from src.utils.database import get_db
import boto3
from os import environ as env
from src.utils.functions import get_random_string
from boto3.dynamodb.conditions import Attr


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

@alumnos.post("", tags=["Alumnos"])
def add_alumno(alumno: Alumno, db: Session = Depends(get_db)):
    db_alumno = DBAlumno(**alumno.model_dump())
    db.add(db_alumno)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"id": db_alumno.id}
    )

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
    
@alumnos.post("/{id}/fotoPerfil", tags=["Alumnos"])
async def upload_foto_perfil(id :int, foto: UploadFile = File(...), db: Session = Depends(get_db)):
    alumno = db.query(DBAlumno).filter(DBAlumno.id == id).first()
    if alumno:
        s3 = boto3.client('s3',
        aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=env.get("AWS_SESSION_TOKEN"),
    )
        try:
            with NamedTemporaryFile(delete=False) as tmp:
                tmp.write(foto.file.read())
                name = tmp.name
                filename = foto.filename
                s3.upload_file(
                    name,
                    env.get('BUCKET_NAME'),
                    filename,
                    ExtraArgs={
                        "ACL": "public-read",
                        "ContentType": 'multipart/form-data'
                    }
                )
        except Exception as e:
            logging.error(e)
            return status.HTTP_400_BAD_REQUEST
        alumno.fotoPerfilUrl = f"https://{env.get('BUCKET_NAME')}.s3.amazonaws.com/{filename}"
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"fotoPerfilUrl": alumno.fotoPerfilUrl}
        )
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )

@alumnos.post("/{id}/email", tags=["Alumnos"])
def send_email(id: int, db: Session = Depends(get_db)):
    alumno = db.query(DBAlumno).filter(DBAlumno.id == id).first()
    if alumno:
        sns = boto3.client('sns',
            aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=env.get("AWS_SESSION_TOKEN"),
            region_name=env.get("REGION_NAME")
        )
        sns.publish(
            TopicArn=env.get("TOPIC_ARN"),
            Message=f"Nombre: {alumno.nombres}\nApellido: {alumno.apellidos}\nCalificaciones: {alumno.promedio}"
        )
        return status.HTTP_200_OK
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
    
@alumnos.post("/{id}/session/login", tags=["Alumnos"])
def login(id: int, password: str = Body(embed=True), db: Session = Depends(get_db)):
    alumno = db.query(DBAlumno).filter(DBAlumno.id == id).first()
    if alumno:
        if alumno.password == password:
            dynamodb = boto3.resource('dynamodb',
                aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
                aws_session_token=env.get("AWS_SESSION_TOKEN"),
                region_name=env.get("REGION_NAME")
            )
            table = dynamodb.Table(env.get('DYNAMODB_TABLE'))
            sessionString = get_random_string(128)
            table.put_item(
                Item={
                    'id': str(uuid.uuid4()),
                    'fecha': int(time.time()),
                    'alumnoId': id,
                    'active': True,
                    'sessionString': sessionString
                },
                ReturnValues='ALL_OLD'
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"sessionString": sessionString}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña incorrecta"
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )

@alumnos.post("/{id}/session/verify", tags=["Alumnos"])
def verify(id: int, sessionString:str = Body(embed=True), db: Session = Depends(get_db)):
    if not sessionString:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sesión inválida"
        )
    alumno = db.query(DBAlumno).filter(DBAlumno.id == id).first()
    if alumno:
        dynamodb = boto3.resource('dynamodb',
            aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=env.get("AWS_SESSION_TOKEN"),
            region_name=env.get("REGION_NAME")
        )
        table = dynamodb.Table(env.get('DYNAMODB_TABLE'))
        response = table.scan(
            FilterExpression=Attr('sessionString').eq(sessionString)
        )
        if not response['Items']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
        is_active = response.get('Items', [])[0].get('active', False)
        if is_active:
            return status.HTTP_200_OK
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
    
@alumnos.post("/{id}/session/logout", tags=["Alumnos"])
def logout(id: int, sessionString: str = Body(embed=True), db: Session = Depends(get_db)):
    alumno = db.query(DBAlumno).filter(DBAlumno.id == id).first()
    if alumno:
        dynamodb = boto3.resource('dynamodb',
            aws_access_key_id=env.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=env.get("AWS_SESSION_TOKEN"),
            region_name=env.get("REGION_NAME")
        )
        table = dynamodb.Table(env.get('DYNAMODB_TABLE'))
        response = table.scan(
            FilterExpression=Attr('sessionString').eq(sessionString)
        )
        id = response.get('Items', [])[0].get('id', False)
        if id:
            table.update_item(
                Key={
                    'id': id
                },
                UpdateExpression='SET active = :val1',
                ExpressionAttributeValues={
                    ':val1': False
                }
            )
            return status.HTTP_200_OK
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )