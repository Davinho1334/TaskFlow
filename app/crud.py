from sqlalchemy.orm import Session
from models import User
from auth import gerar_hash_senha, verificar_senha

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str):
    hashed = gerar_hash_senha(password)
    user = User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verificar_senha(password, user.hashed_password):
        return None
    return user
