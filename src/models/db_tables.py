from sqlalchemy import Column, Integer, String, Float
from src.utils.database import Base

class DBStudent(Base):
    __tablename__ = 'alumnos'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    matricula = Column(String(10), nullable=False)
    promedio = Column(Float, nullable=False)
    fotoPerfilUrl = Column(String(100))
    password = Column(String(50), nullable=False)

class DBTeacher(Base):
    __tablename__ = 'profesores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    numeroEmpleado = Column(Integer, unique=True, nullable=False)
    horasClase = Column(Integer)