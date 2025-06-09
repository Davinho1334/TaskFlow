from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.core.config import settings
from app.schemas.admin import TokenData as AdminTokenData
from app.schemas.user import TokenData as UserTokenData
from app.db.database import SessionLocal
from app.db.models import Admin, User
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = AdminTokenData(username=email)
    except JWTError:
        raise credentials_exception
    admin = db.query(Admin).filter(Admin.email == token_data.username).first()
    if admin is None:
        raise credentials_exception
    return admin

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = UserTokenData(username=email)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user