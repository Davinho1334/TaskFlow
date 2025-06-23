from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class RoleEnum(str, Enum):
    root = "root"
    admin = "admin"
    user = "user"

class TaskStatusEnum(str, Enum):
    aberto = "aberto"
    andamento = "andamento"
    pendente = "pendente"
    concluido = "concluido"

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.user

class UserOut(UserBase):
    id: int
    role: RoleEnum
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjectBase(BaseModel):
    nome: str
    descricao: Optional[str]

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    titulo: str
    descricao: Optional[str]
    status: Optional[TaskStatusEnum] = TaskStatusEnum.aberto
    projeto_id: Optional[int]
    responsavel_id: int
    colaboradores_ids: List[int] = []

class TaskOut(TaskBase):
    id: int
    class Config:
        orm_mode = True