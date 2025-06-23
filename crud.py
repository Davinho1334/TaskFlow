from sqlalchemy.orm import Session
import models, auth

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str, role: str = "user"):
    hashed = auth.gerar_hash_senha(password)
    user = models.User(username=username, hashed_password=hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not auth.verificar_senha(password, user.hashed_password):
        return None
    return user