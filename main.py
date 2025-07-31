from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from .database import get_session, init_db
from .schemas import UserCreate, Token, ProjectCreate
from .crud import create_user, authenticate_user, create_project, get_projects
from .auth import create_access_token
from .deps import get_current_user, admin_required

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_session)):
    return create_user(db, user.username, user.password, user.role)

@app.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_session)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token}

@app.get("/projects")
def read_projects(db: Session = Depends(get_session), user=Depends(get_current_user)):
    return get_projects(db)

@app.post("/projects")
def create_projects(project: ProjectCreate, db: Session = Depends(get_session), user=Depends(admin_required)):
    return create_project(db, project.name, project.description)
