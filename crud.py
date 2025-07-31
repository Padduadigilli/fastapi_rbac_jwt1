from .models import User, Project
from sqlmodel import Session, select
from .auth import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str):
    return db.exec(select(User).where(User.username == username)).first()

def create_user(db: Session, username: str, password: str, role: str):
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_project(db: Session, name: str, description: str):
    project = Project(name=name, description=description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_projects(db: Session):
    return db.exec(select(Project)).all()
