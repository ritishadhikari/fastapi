from fastapi import FastAPI
from models import Todos, Base
from database import engine 
from routers import auth, todos

app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router=auth.router)
app.include_router(router=todos.router)

