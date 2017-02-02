from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Users(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key= True)
	name = Column(String(225))
	gender = Column(String(225))
	email = Column(String(225), unique=True)
	password = Column(String(225))

class Science(Base):
	__tablename__ = "science"
	 id = Column(Integer, primary_key= True)
	 name = relationship('users,name')
	 subject = Column(String)
	 information = Column(String)

class Literature(Base):
	__tablename__ = "literature"
	id = Column(Integer, primary_key= True)
	name = relationship('users.name')
	subject = Column(String)
	information = Column(String)

engine = create_engine ('sqlite;///project.db')

Base.metadata.create_all(engine)
	



						