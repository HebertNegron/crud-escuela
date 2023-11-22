from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nombres = Column(String(50))
    apellidos = Column(String(50))
    matricula = Column(String(10), unique=True)
    promedio = Column(Float)

class Profesor(Base):
    __tablename__ = 'profesores'

    id = Column(Integer, primary_key=True)
    nombres = Column(String(50))
    apellidos = Column(String(50))
    numeroEmpleado = Column(Integer, unique=True)
    horasClase = Column(Integer)