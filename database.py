from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

try:
    engine = create_engine('postgresql://gisuser:abc123@localhost/denver_streets')
except:
    setup_db()
    engine = create_engine('postgresql://gisuser:abc123@localhost/denver_streets')

session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    session.commit()

def drop_db():
    import models
    session.close()
    Base.metadata.drop_all(bind=engine)

def setup_db():
    engine = create_engine('postgresql://postgres@localhost/postgres')
    conn = engine.connect()
    conn.execute('commit')
    conn.execute('create database denver_streets')
    conn.close()

def destroy_db():
    engine = create_engine('postgresql://postgres@localhost/postgres')
    conn = engine.connect()
    conn.execute('commit')
    conn.execute('drop database denver_streets')
    conn.close()
