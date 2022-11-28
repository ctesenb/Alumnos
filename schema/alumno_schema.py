from typing import Optional
from pydantic import BaseModel

class AlumnoS(BaseModel):
    id: Optional[int]
    nombre: str
    apellido: str
    edad: int
    sexo: str
    carrera: str
    semestre: int
    cursos: Optional[int]

    class Config:
        orm_mode = True

class Respuesta(BaseModel):
    status: str
    data: Optional[AlumnoS]
    message: Optional[str]