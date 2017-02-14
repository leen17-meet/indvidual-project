from flask import Flask, render_template, request, flash, redirect, url_for, g, session as login_session
from db import *

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

from db import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/', methods = ['GET', 'POST'])
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
			user = session.query(User).filter_by(email = email).one()
			flash('Login successful, welcome %s' % user.name)
			login_session['name'] = user.name
			login_session['email'] = user.email
			login_session['id'] = user.id
			return redirect(url_for('home'))
		else:
			flash('Incorrect Username/password combination')
			return redirect(url_for('login'))

@app.route('/home')
def home():
	return render_template("home.html")

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
		user.hash_password(password)
		session.add(user)
		session.commit()
		flash("User Created Successfully!")
		return redirect(url_for('home'))
	else:
		return render_template('new.html')


@app.route('/science', methods=['GET', 'POST'])
def science():
	if request.method == 'GET':
		science_list = session.query(Science).all()
		return render_template('science.html', science = science_list)
	else:
		new_name = request.form['Name']
		new_subject = request.form['Subject']
		new_information = request.form['Information']
		news = Science( name = new_name, subject = new_subject, information = new_information)
		session.add(news)
		session.commit()
		return redirect(url_for('science'))

@app.route('/science/delete/<int:science_id>/', methods=['GET','POST'])
def science_delete(science_id):
	lesson = session_query(Science).filter_by(id=science_id).first()
	if request.method == 'GET':
		return render_template('science_delete.html', lesson=lesson)
	else:
		session.delete(lesson)
		session.commit()
		return redirect(url_for('science'))

@app.route('/literature', methods=['GET', 'POST'])
def literature():
	if request.method == 'GET':
		literature_list = session.query(Literature).all()
		return render_template('literature.html', literature = literature_list)
	else:
		new_name = request.form['Name']
		new_subject = request.form['Subject']
		new_information = request.form['Information']
		newl = Literature( name = new_name, subject = new_subject, information = new_information)
		session.add(newl)
		session.commit()
		return redirect(url_for('literature'))

@app.route('/literature/delete/<int:literature_id>/', methods=['GET','POST'])
def literature_delete(literature_id):
	lesson = session_query(Literature).filter_by(id=literature_id).first()
	if request.method == 'GET':
		return render_template('literature_delete.html', lesson=lesson)
	else:
		session.delete(lesson)
		session.commit()
		return redirect(url_for('literature'))

@app.route('/logout')
def logout():
	if 'id' not in login_session:
		flash("You must be logged in order to log out")
		return redirect(url_for('login'))
	del login_session['name']
	del login_session['email']
	del login_session['id']
	flash("Logged Out Successfully")
	return redirect(url_for('login'))

def verify_password(email, password):
	user = session.query(User).filter_by(email = email).first()
	if not user or not user.verify_password(password):
		return False
	g.user = user
	return True

if __name__ == '__main__':
	app.run(debug = True)
	