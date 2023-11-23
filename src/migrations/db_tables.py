from sqlalchemy import Column, Integer, String, Float
from src.utils.database import Base

class Alumno(Base):
    __tablename__ = 'alumnos'
    # __table_args__ = {'schema': ''}

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    matricula = Column(String(10), unique=True, nullable=False)
    promedio = Column(Float)

class Profesor(Base):
    __tablename__ = 'profesores'
    # __table_args__ = {'schema': ''}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    numeroEmpleado = Column(Integer, unique=True, nullable=False)
    horasClase = Column(Integer)