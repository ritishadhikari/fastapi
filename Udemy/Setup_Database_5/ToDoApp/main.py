from fastapi import FastAPI, Depends,HTTPException,Path
from models import Todos, Base
from sqlalchemy.orm import Session
from database import engine 
from database import SessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field

app=FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title: str=Field(min_length=3)
    description: str=Field(min_length=3, max_length=100)
    priority: int=Field(gt=0,lt=6)
    complete: bool 




@app.get(path="/",status_code=status.HTTP_200_OK)
# async def read_all(db: Annotated[ Session, Depends(dependency=get_db) ]):
async def read_all(db: Session = Depends(dependency=get_db) ):
    return db.query(Todos).all()

@app.get(path="/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(
    todo_id: int=Path(gt=0),
    db: Session = Depends(dependency=get_db),
    ):
    todo_model=db.query(Todos).filter(Todos.idn==todo_id).first()
    if todo_model is not None:
        return todo_model
    else: 
        raise HTTPException(status_code=404, detail="Record does not exists")

@app.post(path="/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request:TodoRequest,
                      db: Session = Depends(dependency=get_db) ):
    todo_model=Todos(**todo_request.model_dump())
    db.add(instance=todo_model)
    db.commit()

@app.put("/todo_update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    todo_request:TodoRequest,
    todo_id:int=Path(gt=0),
    db: Session = Depends(dependency=get_db)
):
    todo_model=db.query(Todos).filter(Todos.idn==todo_id).first()
    if todo_model is None:
        return HTTPException(status_code=404,detail="Record not found for update")
    else:
        todo_model.title=todo_request.title
        todo_model.complete=todo_request.complete
        todo_model.priority=todo_request.priority
        todo_model.description=todo_request.description
        db.add(todo_model)  # has the old id, and id being a pk, update the record
        db.commit()

@app.delete(path="/todo/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    todo_id:int=Path(gt=0),
    db: Session = Depends(dependency=get_db)
    ):
    todo_model=db.query(Todos).filter(Todos.idn==todo_id).first()
    if todo_model is None:
        return HTTPException(status_code=404,detail="Record not found for delete")
    else:
        db.query(Todos).filter(Todos.idn==todo_id).delete()
        db.commit()