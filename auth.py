from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "segredo-super-seguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plain, senha_hashed):
    return pwd_context.verify(senha_plain, senha_hashed)

def gerar_hash_senha(senha):
    return pwd_context.hash(senha)

def criar_token_acesso(data: dict, tempo_expira: timedelta = None):
    to_encode = data.copy()
    expira = datetime.utcnow() + (tempo_expira or timedelta(minutes=15))
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None