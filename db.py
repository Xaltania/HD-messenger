'''
db
database file, containing all the logic to interface with the sql database
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display sql output

engine = create_engine("sqlite:///database/main.db", echo=False)
Session = sessionmaker(bind=engine)

# initializes the database
Base.metadata.create_all(engine)

# inserts a user to the database
def insert_user(username: str, password: str):
    session = Session()
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    session.close()

# gets a user from the database
def get_user(username: str):
    session = Session()
    user = session.query(User).get(username)
    session.close()
    return user