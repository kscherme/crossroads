#!/usr/bin python

# Libraries
from flask import Flask, render_template, request, redirect, url_for, session, abort, flash

import sys
import MySQLdb
import os

# Global Variables

# Database info
SQL_ADDR = 'localhost'
SQL_USER = 'kscherme'
SQL_PASSWD = 'crossroads111'
SQL_DB = 'crossroads'

# Flask info
app = Flask(__name__)

# Setup Database
db = MySQLdb.connect(host=SQL_ADDR, user=SQL_USER,
                     passwd=SQL_PASSWD, db=SQL_DB)

cursor = db.cursor()

# Functions

# Inserts a new movie into the database


def insertMovieDB(year, title, is_tv):
	# Format SQL
	sql = 'INSERT INTO Movies (year, title, is_tv) VALUES ("{}", "{}", "{}")'.format(
		year, title, is_tv)
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return True

# Searches for movie by title
def searchMovieDB(title):
    	title = "%" + title + "%"
	# Format SQL
	sql = 'SELECT movieID, title, year FROM Movies WHERE Title LIKE "{}" and is_tv = 1'.format(
		title)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuples = cursor.fetchall()
	# Return results
	return tuples


# def deleteMovie(movieID):
# 	# Format SQL
# 	sql = 'DELETE FROM Movies WHERE movieID = {}'.format(movieID)
# 	# Execute SQL
# 	cursor.execute(sql)
# 	db.commit()
# 	return True

# Update movie rating
def updateMovieRating(movieID, userRating):
	# Get Current Rating
	# Also get number of votes
	sql = 'SELECT Rating, numVotes FROM Ratings WHERE MovieID = "{}"'.format(
		movieID)
	cursor.execute(sql)
	rows = cursor.fetchall()
	print rows
	if rows:
		currentRating = rows[0][0]
		NumVotes = rows[0][1]
		# Calculate New Rating
		SumRatings = currentRating * NumVotes
		SumRatings = SumRatings + int(userRating)
		NumVotes = NumVotes + 1
		newRating = SumRatings / NumVotes
		print newRating
		# Format SQL
		sql = 'UPDATE Ratings SET Rating = "{}", numVotes = "{}" WHERE MovieID = "{}"'.format(
			newRating, NumVotes, movieID)
		# Execute SQL
		cursor.execute(sql)
		db.commit()
		return newRating
	else:
    		return "No MovieID"

def authenticate(input_username, input_password):
	# Format SQL
	sql = 'SELECT id, username, password FROM Users WHERE username = "{}" and password = "{}"'.format(
		input_username, input_password)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuple = cursor.fetchall()
	result = tuple[0][0]
	# Return results
	if result:
		user.username = input_username
		user.password = input_password
		user.id = result
		return True
	else:
		return False
    	
# User Class
class User(object):
	def __init__(self, username, password):
			self.username = username
			self.password = password
# Flask templates
user = User("","")

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for('homepage'))

@app.route('/login', methods=['POST'])
def do_login():
    if request.method == 'POST':
    #if request.form['password'] == 'password' and request.form['username'] == 'admin':
		username = request.form['username']
		password = request.form['password']
		if (authenticate(username, password)):
			session['logged_in'] = True
		else:
			flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/homepage")
def homepage():
	return render_template('homepage.html')


@app.route("/insert", methods=['POST', 'GET'])
def insert():
	if request.method == 'POST':
		movieName = request.form['movieTitle']
		movieYear = request.form['movieYear']
		is_tv = request.form['is_tv']
		insertMovieDB(movieYear, movieName, is_tv)
		return render_template("insert.html", name=movieName, year=movieYear)
	else:
		return render_template("insert.html", name="", year="")


@app.route("/search", methods=['POST', 'GET'])
def search():
    	tuples = []
	if request.method == 'POST':
		searchMovie = request.form['movieSearch']
		tuples = searchMovieDB(searchMovie)
		if tuples:
			return render_template("search.html", tuples=tuples)
		else:
    			return render_template("search.html", tuples=None)
	else:
		return render_template("search.html", tuples=tuples)


# @app.route("/delete", methods=['POST'])
# def delete():
# 	if request.method == 'POST':
# 		movieID = request.form['movieID']
# 		deleteMovie(movieID)
# 		return render_template('search.html')
# 	else:
# 		return render_template('search.html')


@app.route("/update", methods=['POST', 'GET'])
def update():
    	tuples = []
	if request.method == 'POST':
    		searchMovie = request.form['movieSearch']
		#movieID = request.form['movieID']
		#userRating = request.form['userRating']
		#rating = updateMovieRating(movieID, userRating)
		tuples = searchMovieDB(searchMovie)
		return render_template("update.html", tuples=tuples)
	else:
		return render_template("update.html", tuples=None)

@app.route("/rate/<movieID>", methods=['POST', 'GET'])
def rate(movieID=None):
	if request.method == 'POST':
		userRating = request.form['userRating']
		rating = updateMovieRating(movieID, userRating)
		return render_template("rate.html", movieID=movieID, rating=rating)
	else:
		return render_template("rate.html", movieID=movieID, rating="")


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=5200, debug=True)