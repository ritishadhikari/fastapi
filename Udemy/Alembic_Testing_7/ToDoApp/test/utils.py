"""
This Python  Script contains all the reusable components that will be shared
among all the test scripts
"""

from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool,QueuePool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from fastapi.testclient import TestClient
import pytest
from ..models import Todos
from ..main import app

SQLALCHEMY_DATABASE_URL="sqlite:///./testdb.db"

engine=create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread":False
        },
    poolclass=QueuePool
    )

TestingSessionLocal=sessionmaker(
                    bind=engine,
                    autoflush=False,
                    autocommit=False)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    yield {
        'username':'ritishadhikaritest',
        'id':1,
        'username':'admin'
        }
    
client=TestClient(app=app)

@pytest.fixture
def test_todo():
    todo=Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1
        )
    db=TestingSessionLocal()
    db.add(instance=todo)
    db.commit()
    yield db

    with engine.connect() as connection:
        connection.execute(statement=text(text="DELETE FROM todos"))
        connection.commit()