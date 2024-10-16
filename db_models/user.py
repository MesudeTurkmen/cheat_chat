from db_models.base import Model, TimeStampedModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship 

class User(TimeStampedModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nick_name = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__},name: {self.first_name} {self.last_name}'
    
