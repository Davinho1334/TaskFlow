from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class RoleEnum(str, enum.Enum):
    root = "root"
    admin = "admin"
    user = "user"

class TaskStatusEnum(str, enum.Enum):
    aberto = "aberto"
    andamento = "andamento"
    pendente = "pendente"
    concluido = "concluido"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)

    tasks_responsavel = relationship("Task", back_populates="responsavel")
    tasks_colaborador = relationship("TaskColaboradores", back_populates="colaborador")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    tarefas = relationship("Task", back_populates="projeto")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    descricao = Column(String)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.aberto)

    responsavel_id = Column(Integer, ForeignKey("users.id"))
    projeto_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    responsavel = relationship("User", back_populates="tasks_responsavel")
    projeto = relationship("Project", back_populates="tarefas")
    colaboradores = relationship("TaskColaboradores", back_populates="tarefa")

class TaskColaboradores(Base):
    __tablename__ = "task_colaboradores"
    id = Column(Integer, primary_key=True)
    tarefa_id = Column(Integer, ForeignKey("tasks.id"))
    colaborador_id = Column(Integer, ForeignKey("users.id"))

    tarefa = relationship("Task", back_populates="colaboradores")
    colaborador = relationship("User", back_populates="tasks_colaborador")