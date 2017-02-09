from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

from db import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form ['password']
		if email is None or password is None:
			flash ('Missing Arguments')
			return redirect(url_for(login))
		if verify_password(email, password):
			customer = session.query(User).filter_by(email = email).one()
			flash('Login successful, welcome %s' % user.name)
			login_session['name'] = user.name
			login_session['email'] = user.email
			login_session['id'] = user.id
			return redirect(url_for('home'))
		else:
			flash('Incorrect Username/password combination')
			return redirect(url_for('login'))

	return render_template('login.html')

@app.route('/new', methods= ['GET', 'POST'])
def new():
	if request.method == 'POST':
		name = request.form['name']
		gender = request.form['gender']
		email = request.form['email']
		password = request.form['password']
		if name == "" or email == "" or password == "":
			flash("Your form is missing arguments")
			return redirect(url_for('new'))
		if session.query(User).filter_by(email = email).first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('new'))
		user = User(name = name, gender=gender, email=email)
		session.add(user)
		session.commit()
		flash("User Created Successfully!")
		return redirect(url_for('home'))
	else:
		return render_template('new.html')


@app.route('/science')
def science():
	return

@app.route('/literature')
def literature():
	return

@app.route('/logout', methods = ['POST'])
def logout():
	return

def verify_password(email, password):
	user = session.query(User).filter_by(email = email).first()
	if not user or not user.verify_password(password):
		return False
	g.user = user
	return True

if __name__ == '__main__':
	app.run()
	