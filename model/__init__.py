from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Imports elements defined in the model
from model.base import Base
from model.payment import Payment

# Specifies the database directory and verifies if it exists
db_path = "database/"
if not os.path.exists(db_path):
   os.makedirs(db_path)

# Url to access the database (this is a local sqlite access url)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Creates the engine that connects to the database
engine = create_engine(db_url, echo=False)

# Creates a session creator with the database
Session = sessionmaker(bind=engine)

# Creates the database, if it doesn´t exist yet
if not database_exists(engine.url):
    create_database(engine.url) 

# Creates database tables, if they don´t exist yet
Base.metadata.create_all(engine)
