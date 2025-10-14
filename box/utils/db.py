from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os.path import basename, dirname, abspath
import inspect

Base = declarative_base()

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)

    def __repr__(self):
        return f"<Settings(key='{self.key}', value='{self.value}')>"

DATABASE_URL = "sqlite:///settings.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

class cfg:
    def read(key):
        try:
            plugin = basename(dirname(abspath(inspect.stack()[1].filename)))
        except IndexError:
            plugin = "global"
        key = f"{plugin}-{key}"

        try:
            return db.query(Settings).filter_by(key=key).first().value
        except:
            return
    
    def write(key, value):
        try:
            plugin = basename(dirname(abspath(inspect.stack()[1].filename)))
        except IndexError:
            plugin = "global"
        key = f"{plugin}-{key}"

        q = db.query(Settings).filter_by(key=key).first()
        if q:
            q.value = value
            db.commit()
        else:
            db.add(Settings(key=key, value=value))
            db.commit()

    def get(key):
        try:
            plugin = basename(dirname(abspath(inspect.stack()[1].filename)))
        except IndexError:
            plugin = "global"
        key = f"{plugin}-{key}"
        print(key)

        try:
            return db.query(Settings).filter_by(key=key).first().value
        except:
            return None