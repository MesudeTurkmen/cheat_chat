from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

Base = declarative_base()

engine = create_engine('sqlite:///chat_users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)



def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(nickname, password):
    session = Session()
    if session.query(User).filter_by(nickname=nickname).first():
        print("Nickname already taken.")
        return False
    hashed_password = hash_password(password)
    new_user = User(nickname=nickname, password=hashed_password)
    session.add(new_user)
    session.commit()
    print("User registered successfully.")
    return True

def authenticate_user(nickname, password):
    session = Session()
    user = session.query(User).filter_by(nickname=nickname).first()
    if user and verify_password(password, user.password):
        print("Authentication successful.")
        return True
    else:
        print("Invalid nickname or password.")
        return False