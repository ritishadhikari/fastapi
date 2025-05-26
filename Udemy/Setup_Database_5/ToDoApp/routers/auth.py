from fastapi import APIRouter,Depends
from pydantic import BaseModel
from models import Users
from database import SessionLocal
from passlib.context import CryptContext
from starlette import status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

async def authenticate_user(username:str, password: str, db):
    user=db.query(Users).filter(Users.username==username).first()
    if user and bcrypt_context.verify(secret=password,hash=user.hashed_password):
        return True
    else: 
        return False

@router.post(path="/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request:CreateUserRequest,
    db:Session=Depends(dependency=get_db),
    ):
    
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password= bcrypt_context.hash(
            secret=create_user_request.password),
        is_active=True
    )

    db.add(instance=create_user_model)
    db.commit()

@router.post(path="/token")
async def login_for_access_token(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db: Session=Depends(dependency=get_db)
):
    user=await authenticate_user(username=form_data.username,
                           password=form_data.password,
                           db=db)
    
    return "Failed Authentication" if not user else "Successful Authentication"
