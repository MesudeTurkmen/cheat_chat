from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Veritabanı bağlantısını burada tanımla
engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)

# Bu session, modellerde kullanılabilir
session = Session()
