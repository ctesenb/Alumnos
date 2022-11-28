from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi import Request, Depends, Request, Form
from config.db import SessionLocal, engine
import model.alumno_model
from sqlalchemy.orm import Session
from model.alumno_model import AlumnoM

model.alumno_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/alumno/{id}", response_class=HTMLResponse)
def get_alumno_id(request: Request, id: int, db: Session = Depends(get_database_session)):
    alumno = db.query(AlumnoM).filter(AlumnoM.id == id).first()
    return templates.TemplateResponse("view_alumno.html", {"request": request, "alumno": alumno})

@app.get("/alumno", response_class=HTMLResponse)
def get_alumno_all(request: Request, db: Session = Depends(get_database_session)):
    alumnos = db.query(AlumnoM).all()
    return templates.TemplateResponse("list_alumno.html", {"request": request, "alumno_list": alumnos})

@app.get("/create_alumno_ui", response_class=HTMLResponse)
async def create_alumno_ui(request: Request):
    return templates.TemplateResponse("create_alumno.html", {"request": request})

@app.post("/create_alumno/", response_class=HTMLResponse)
def create_alumno(nombre: str = Form(...), apellido: str = Form(...), edad: int = Form(...), sexo: str = Form(...), carrera: str = Form(...), semestre: int  = Form(...), db: Session = Depends(get_database_session)):
    alumno = AlumnoM(nombre=nombre, apellido=apellido, edad=edad, sexo=sexo, carrera=carrera, semestre=semestre)
    db.add(alumno)
    db.commit()
    return RedirectResponse(url="/alumno", status_code=303)


@app.get("/alumno/delete/{id}", response_class=HTMLResponse)
def delete_alumno(id: int, db: Session = Depends(get_database_session)):
    db.query(AlumnoM).filter(AlumnoM.id == id).delete()
    db.commit()
    return RedirectResponse(url="/alumno", status_code=303)

@app.get("/alumno/update/{id}", response_class=HTMLResponse)
def update_alumno(id: int, request: Request, db: Session = Depends(get_database_session)):
    print('Alumno update: ' + str(id))
    result = db.query(AlumnoM).filter(AlumnoM.id == id).first()
    return templates.TemplateResponse("update_alumno.html", {"request": request, "alumno": result})

@app.post("/update_alumno", response_class=HTMLResponse)
def update_alumno(request: Request, id: int = Form(...), carrera: str = Form(...), semestre: int  = Form(...), db: Session = Depends(get_database_session)):
    db.query(AlumnoM).filter(AlumnoM.id == id).update({AlumnoM.carrera: carrera, AlumnoM.semestre: semestre})
    db.commit()
    return RedirectResponse(url="/alumno", status_code=303)