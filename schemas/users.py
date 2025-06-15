from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyycopg2

# Substitua pelos seus dados de conexão
SQLALCHEMY_DATABASE_URL = "postgresql://usuario:senha@localhost:5432/nome_do_banco"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    celular = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    administrador = Column(Boolean, default=False)
    usuario = Column(Boolean, default=True)
    ativo = Column(Boolean, default=True)
    dt_criacao = Column(DateTime, default=datetime.utcnow)
    dt_ultimo_login = Column(DateTime, nullable=True)
    preferencias = Column(JSON, nullable=True)  # Exemplo de campo JSON

    projetos = relationship("Projeto", back_populates="proprietario")
    tarefas = relationship("Tarefa", back_populates="responsavel")

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    dt_criacao = Column(DateTime, default=datetime.utcnow)
    ativo = Column(Boolean, default=True)

class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    dt_criacao = Column(DateTime, default=datetime.utcnow)
    proprietario_id = Column(Integer, ForeignKey("users.id"))
    proprietario = relationship("User", back_populates="projetos")

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    objetivo = Column(String, nullable=True)
    status_da_tarefa = Column(String, nullable=True)
    dt_criacao = Column(DateTime, default=datetime.utcnow)
    dt_inicio = Column(DateTime, nullable=True)
    dt_conclusao_prevista = Column(DateTime, nullable=True)
    dt_conclusao_real = Column(DateTime, nullable=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"))
    responsavel_id = Column(Integer, ForeignKey("users.id"))
    responsavel = relationship("User", back_populates="tarefas")