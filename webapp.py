from flask import Flask, render_templte, request, redirect, url_for 

app = Flask(__name__)

from db import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def home():
	return

@app.route('/login', methods = ['GET', 'POST'])
def login():
	return

@app.route('/science')
def science():
	return

@app.route('/literature')
def literature():
	return

if __name__ == '__main__':
	app.run()
	