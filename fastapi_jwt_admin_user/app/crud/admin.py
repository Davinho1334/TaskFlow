from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db import models
from app.schemas import admin as schemas
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings

def create_admin(db: Session, admin: schemas.AdminCreate):
    if db.query(models.Admin).filter(models.Admin.email == admin.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    hashed_password = get_password_hash(admin.password)
    db_admin = models.Admin(username=admin.username, email=admin.email, hashed_password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def authenticate_admin(db: Session, email: str, password: str):
    admin = db.query(models.Admin).filter(models.Admin.email == email).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": admin.email}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}