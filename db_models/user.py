from sqlalchemy import Column, Integer, String
from db_models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"<User(name='{self.nickname}', email='{self.password}')>"