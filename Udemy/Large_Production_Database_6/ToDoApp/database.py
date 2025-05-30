from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL="sqlite:///./todosapp.db"
# SQLALCHEMY_DATABASE_URL="postgresql://postgres:test1234!@localhost/TodoApplicationDatabaseTwo"  # postgres
SQLALCHEMY_DATABASE_URL="mysql+pymysql://root:test1234@127.0.0.1:3306/todoapplicationdatabase"  # mysql

# engine=create_engine(url=SQLALCHEMY_DATABASE_URL,
#                      connect_args={'check_same_thread':False})

engine=create_engine(url=SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(
                    bind=engine,
                    autoflush=False,
                    autocommit=False)


Base=declarative_base()