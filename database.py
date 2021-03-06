from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import *
import os
import yaml

config = yaml.load(open('config.yaml', 'r'))

try:
    if os.environ['FLASK_ENV'] == 'test':
        database_name = config['database']['test']['db']
        database_user = config['database']['test']['user']
        database_pass = config['database']['test']['pass']

    else:
        database_name = config['database']['development']['db']
        database_user = config['database']['development']['user']
        database_pass = config['database']['development']['pass']

except:
    database_name = config['database']['development']['db']
    database_user = config['database']['development']['user']
    database_pass = config['database']['development']['pass']

engine = create_engine('postgresql://'+database_user+':'+database_pass+'@localhost/' + database_name)
session = scoped_session(sessionmaker(bind=engine))
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)
Base.query = session.query_property()

def init_db():
    import models
    metadata.create_all(bind=engine)
    session.commit()

def drop_db():
    import models
    session.close()
    metadata.drop_all(bind=engine)

def create_db():
    postgres_engine = create_engine('postgresql://'+database_user+':'+database_pass+'@localhost/postgres')
    conn = postgres_engine.connect()
    conn.execute('commit')
    conn.execute('create database ' + database_name + ' WITH ENCODING=\'UNICODE\'')
    conn.close()

def destroy_db():
    postgres_engine = create_engine('postgresql://'+database_user+':'+database_pass+'@localhost/postgres')
    conn = postgres_engine.connect()
    conn.execute('commit')
    conn.execute('drop database ' + database_name)
    conn.close()

