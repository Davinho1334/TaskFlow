from pydantic import BaseModel, EmailStr

class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None