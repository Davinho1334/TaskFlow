from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas import user as schemas
from app.crud import user as crud_user
from app.core.security_auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud_user.authenticate_user(db, user.email, user.password)

@router.get("/me", response_model=schemas.UserOut)
def read_user_me(current_user=Depends(get_current_user)):
    return current_user