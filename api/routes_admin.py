from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas import admin as schemas
from app.crud import admin as crud_admin
from app.core.security_auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.AdminOut)
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud_admin.create_admin(db, admin)

@router.post("/login", response_model=schemas.Token)
def login_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud_admin.authenticate_admin(db, admin.email, admin.password)

@router.get("/me", response_model=schemas.AdminOut)
def read_admin_me(current_admin=Depends(get_current_admin)):
    return current_admin