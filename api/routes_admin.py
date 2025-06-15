from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas import admin as schemas
from app.crud import admin as crud_admin
from app.core.security_auth import get_current_admin
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth import create_access_token, verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Aqui você deve validar o usuário e senha com o banco de dados
    if form_data.username == "admin" and form_data.password == "senha":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    return user

@router.post("/register", response_model=schemas.AdminOut)
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud_admin.create_admin(db, admin)

@router.post("/login", response_model=schemas.Token)
def login_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud_admin.authenticate_admin(db, admin.email, admin.password)

@router.get("/me", response_model=schemas.AdminOut)
def read_admin_me(current_admin=Depends(get_current_admin)):
    return current_admin