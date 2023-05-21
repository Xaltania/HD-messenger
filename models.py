# USYD CODE CITATION ACKNOWLEDGEMENT
# I declare that the following code template is distributed by Winston Wijaya
# With changes made to implement security features

'''
models
defines sql alchemy data models
also contains the definition for the room class used to keep track of socket.io rooms
'''

from sqlalchemy import String, Integer, Column, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Dict

# data models
class Base(DeclarativeBase):
    pass

# model to store user information
class User(Base):
    __tablename__ = "user"
    
    username: Mapped[str] = mapped_column(String, primary_key=True)
    password: Mapped[str] = mapped_column(String)

    def __str__(self):
        return self.username
    

# stateful counter used to generate the room id
class Counter():
    def __init__(self):
        self.counter = 0
    
    def get(self):
        self.counter += 1
        return self.counter


class Room():
    def __init__(self):
        self.counter = Counter()
        self.dict: Dict[str, int] = {}

    def create_room(self, sender: str, receiver: str) -> int:
        room_id = self.counter.get()
        self.dict[sender] = room_id
        self.dict[receiver] = room_id
        return room_id
    
    def join_room(self,  sender: str, room_id: int) -> int:
        self.dict[sender] = room_id

    def leave_room(self, user):
        if user not in self.dict.keys():
            return
        del self.dict[user]

    def get_room_id(self, user: str):
        if user not in self.dict.keys():
            return None
        return self.dict[user]
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    is_anonymous = Column(Boolean, nullable=False)
    author = Column(String(50))

    def __init__(self, content, is_anonymous, author):
        self.content = content
        self.is_anonymous = is_anonymous
        self.author = author