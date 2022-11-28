from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from config.db import Base

class AlumnoM(Base):
    __tablename__ = "Alumnos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(30))
    apellido = Column(String(30))
    edad = Column(Integer)
    sexo = Column(String(1))
    carrera = Column(String(30))
    semestre = Column(Integer)
    cursos = Column(Integer)