from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL="sqlite:///./todosapp.db"

engine=create_engine(url=SQLALCHEMY_DATABASE_URL,
                     connect_args={'check_same_thread':False})

SessionLocal=sessionmaker(
                    bind=engine,
                    autoflush=False,
                    autocommit=False)


Base=declarative_base()