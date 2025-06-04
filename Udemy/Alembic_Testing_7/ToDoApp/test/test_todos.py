from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool,QueuePool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.todos import get_db
from ..routers.auth import get_current_user
from fastapi.testclient import TestClient
from fastapi import status 

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
    return {
        'username':'ritishadhikaritest',
        'id':1,
        'username':'admin'
        }

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

# Forcing application to run as a test
client=TestClient(app=app)

def test_read_all_authenticated():
    response=client.get(url="/")
    assert response.status_code==status.HTTP_200_OK
    assert response.json()==[]
    