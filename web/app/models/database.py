from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

def get_connection(config: dict):
    db = config["db"]
    db_string=f"mysql+pymysql://{db['user']}:{db['pass']}@{db['host']}:{db['port']}/{db['name']}?charset=utf8mb4"
    engine=create_engine(db_string)
    connection=engine.connect()
    session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

    return session()
