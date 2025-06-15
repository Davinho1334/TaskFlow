from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas import user as schemas
from app.crud import user as crud_user
from app.core.security_auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth import create_access_token, verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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