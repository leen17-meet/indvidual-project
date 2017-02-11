from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class User(Base):
	__tablename__ = "user"
	id = Column(Integer, primary_key= True)
	name = Column(String(225))
	gender = Column(String(225))
	email = Column(String(225), unique=True)
	password = Column(String(225))
	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

class Science(Base):
	__tablename__ = "science"
	id = Column(Integer, primary_key= True)
	name = Column(String)
	subject = Column(String)
	information = Column(String)

class Literature(Base):
	__tablename__ = "literature"
	id = Column(Integer, primary_key= True)
	name = Column(String)
	subject = Column(String)
	information = Column(String)

engine = create_engine ('sqlite:///project.db')

Base.metadata.create_all(engine)
	



						