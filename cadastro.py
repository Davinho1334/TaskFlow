from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, RoleEnum
from database import Base

engine = create_engine('postgresql://usuario:senha@localhost:5432/taskflow')
Session = sessionmaker(bind=engine)
session = Session()

def cadastrar_usuario(username, senha, role=RoleEnum.user):
    if session.query(User).filter_by(username=username).first():
        print("Usuário já existe.")
        return
    novo_usuario = User(
        username=username,
        hashed_password=senha,
        role=role
    )
    session.add(novo_usuario)
    session.commit()
    print(f"Usuário '{username}' cadastrado como '{role.value}'.")

def cadastrar_admin(username, senha):
    cadastrar_usuario(username, senha, role=RoleEnum.admin)

def cadastrar_root(username, senha):
    cadastrar_usuario(username, senha, role=RoleEnum.root)