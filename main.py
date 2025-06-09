from fastapi import FastAPI
from app.db import models, database
from app.api import routes_admin, routes_user

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(routes_admin.router)
app.include_router(routes_user.router)

@app.get("/")
def root():
    return {"msg": "API com Admin e Usuário ativa"}