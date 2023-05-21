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

# inserts a post into the database
def create_post(content: str, is_anonymous: bool):
    session = Session()
    post = Post(content=content, is_anonymous=is_anonymous)
    session.add(post)
    session.commit()
    session.close()

# retrieves all posts from the database
def get_posts():
    session = Session()
    posts = session.query(Post).all()
    session.close()
    return posts