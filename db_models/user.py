from db_models.base import Model, TimeStampedModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship 

class User(TimeStampedModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nick_name = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)

    roles = Relationship('Role', secondary='user_roles',back_populates='users', passive_deletes=True)

    def __repr__(self):
        return f'{self.__class__.__name__},name: {self.first_name} {self.last_name}'
    
class Role(Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80),nullable=False)
    slug = Column(String(80),nullable=False, unique=True)

    users = Relationship('User', secondary='user_roles', back_populates='roles', passive_deletes=True)

    def __repr__(self):
        return f'{self.__class__.__name__}, name:{self.name}'
    


class UserRole(TimeStampedModel):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('users.id', ondelete=' CASCADE'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete=' CASCADE'), primary_key=True)
