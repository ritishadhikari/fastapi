from fastapi import APIRouter, Depends,HTTPException,Path
from models import Todos, Base
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from typing import Annotated

router=APIRouter()

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

@router.get(path="/",status_code=status.HTTP_200_OK)
# async def read_all(db: Annotated[ Session, Depends(dependency=get_db) ]):
async def read_all(
    user:dict=Depends(dependency=get_current_user),
    db: Session = Depends(dependency=get_db) ):
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()

@router.get(path="/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(
    user:dict=Depends(dependency=get_current_user) ,
    todo_id: int=Path(gt=0),
    db: Session = Depends(dependency=get_db),
    ):
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id)\
        .filter(Todos.owner_id==user.get('id'))\
        .first()
    
    if todo_model is not None:
        return todo_model
    else: 
        raise HTTPException(status_code=404, detail="Record does not exists")

@router.post(path="/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request:TodoRequest,
                      user:Annotated[dict,Depends(dependency=get_current_user)],
                      db:Annotated[Session,Depends(dependency=get_db)]
                      ):
    print("coming here")
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Authentication Failed")
    todo_model=Todos(**todo_request.model_dump(),owner_id=user.get('id'))
    db.add(instance=todo_model)
    db.commit()

@router.put("/todo_update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    todo_request:TodoRequest,
    todo_id:int=Path(gt=0),
    user:dict=Depends(dependency=get_current_user),
    db: Session = Depends(dependency=get_db)
    ):
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id)\
            .filter(Todos.owner_id==user.get('id'))\
            .first()
    if todo_model is None:
        return HTTPException(status_code=404,detail="Record not found for update")
    else:
        todo_model.title=todo_request.title
        todo_model.complete=todo_request.complete
        todo_model.priority=todo_request.priority
        todo_model.description=todo_request.description
        db.add(todo_model)  # has the old id, and id being a pk, update the record
        db.commit()

@router.delete(path="/todo/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    todo_id:int=Path(gt=0),
    user:dict=Depends(dependency=get_current_user),
    db: Session = Depends(dependency=get_db)
    ):
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id)\
        .filter(Todos.owner_id==user.get('id'))\
        .first()
    if todo_model is None:
        return HTTPException(status_code=404,detail="Record not found for delete")
    else:
        db.query(Todos).filter(Todos.id==todo_id)\
            .filter(Todos.owner_id==user.get('id'))\
            .delete()
        db.commit()