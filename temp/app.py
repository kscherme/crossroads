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
	sql = 'INSERT INTO Movies (year, title, is_tv) VALUES ("{}", "{}", "{}")'.format(year, title, is_tv)
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return True

# Searches for movie by title
def searchMovieDB(title):
	titleLike = "%" + title + "%"

	# Format SQL for Partial Match
	sql = 'SELECT m.movieID, m.title, m.year, r.Rating FROM Movies m LEFT JOIN Ratings r ON r.MovieID=m.movieID WHERE Title LIKE "{}" ORDER BY r.Rating DESC'.format(
		titleLike)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuples = cursor.fetchall()
	return tuples

def advSearchMovieDB(titleBeginning, titleContains, beginningYear, endingYear, \
			genre, actor, beginningRating, endingRating):

	sql = getAdvSearchQuery(titleBeginning, titleContains, beginningYear, endingYear, \
			genre, actor, beginningRating, endingRating)
	cursor.execute(sql)
	tuples = cursor.fetchall()
	for t in tuples:
		print t
	return tuples
	

def getAdvSearchQuery(titleBeginning, titleContains, beginningYear, endingYear, \
			genre, actor, beginningRating, endingRating):
	### Format inputs into SQL
	# Title
	titleClause = ''
	if titleBeginning != '':
		titleClause += 'AND m.title LIKE \'{}%\' '.format(titleBeginning)
	if titleContains != '':
		titleClause += 'AND m.title LIKE \'%{}%\' '.format(titleContains)
	
	# Year Range
	
	yearClause = ''
	if beginningYear != '':
		yearClause += 'AND m.year > {} '.format(beginningYear) 
	if endingYear != '':
		yearClause += 'AND m.year < {} '.format(endingYear)	

	# Genre
	genreClause = ''
	if genre != 'All' and genre != '':
		genreClause = 'AND g.genre=\'' + genre + '\' '
	
	# Actor
	actorClause = ''
	if actor != '':	
		actorClause += 'AND a.name LIKE \'%{}%\' AND a.actorID=ai.actorID '.format(actor)
	
	# Rating
	ratingClause = ''
	if beginningRating != '':
		ratingClause += 'AND r.rating >= {} '.format(beginningRating)
		# if endingRating != '':
		# 	ratingClause += ' AND '			

	if endingRating != '':
		ratingClause += 'AND rating <= {} '.format(endingRating)
	
		
	sql = 	'''	
			SELECT 	m.movieID, m.title, m.year, r.Rating
	       		FROM 	Movies m, Ratings r, Actors a, AppearsIn ai, Genres g
	       		WHERE 	m.movieID=r.MovieID AND m.movieID=ai.movieID AND m.movieID=g.movieID {}{}{}{}{};'''.format(titleClause, yearClause, genreClause, actorClause, ratingClause)
	print sql 
	return sql
	

# Searches for movie by title
def searchMovieDBRate(title):
	titleLike = "%" + title + "%"

	# Format SQL for Partial Match
	sql = 'SELECT m.movieID, m.title, m.year FROM Movies m WHERE Title LIKE "{}"'.format(
		titleLike)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuples = cursor.fetchall()
	return tuples

def searchUserDB(user, curr_user):
	user = "%" + user + "%"
	# Format SQL
	if user is not "%%":
		sql = 'SELECT * FROM Users WHERE username LIKE "{}" AND id != "{}"'.format(user, curr_user)
	else:
		sql = 'SELECT * FROM Users WHERE id != "{}"'.format(curr_user)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuples = cursor.fetchall()
	# Return results
	return tuples

# Update movie rating
def updateMovieRating(movieID, userRating):
	# Get Current Rating
	# Also get number of votes
	sql = 'SELECT Rating, numVotes FROM Ratings WHERE MovieID = "{}"'.format(movieID)
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
		# Format SQL
		sql = 'UPDATE Ratings SET Rating = "{}", numVotes = "{}" WHERE MovieID = "{}"'.format(
			newRating, NumVotes, movieID)
		# Execute SQL
		cursor.execute(sql)
		db.commit()
		return newRating
	else:
		sql = 'INSERT INTO Ratings (Source, MovieID, Rating, numVotes) VALUES ("{}","{}","{}","{}")'.format("User", movieID, userRating, 1)
		cursor.execute(sql)
		db.commit()
		return userRating

def authenticate(input_username, input_password):
	# Format SQL
	sql = 'SELECT id, username, password FROM Users WHERE username = "{}" and password = "{}"'.format(input_username, input_password)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuple = cursor.fetchall()
	if tuple:
		result = tuple[0][0]
	else:
		result = False
	# Return results
	if result:
		user.username = input_username
		user.password = input_password
		user.id = result
		return True
	else:
		return False

def createUser(input_username, input_password):
	# Format SQL to Check for Other Users
	sql = 'SELECT * FROM Users WHERE username = "{}"'.format(input_username)
	#Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuple = cursor.fetchall()
	if tuple:
		return False

	# Format SQL to Insert New User
	sql = 'INSERT INTO Users (username, password) VALUES ("{}", "{}")'.format(input_username, input_password)
	# Execute SQL
	cursor.execute(sql)
	db.commit()

	# Format SQL to Get ID
	sql = 'Select id FROM Users WHERE username = "{}"'.format(input_username)
	#Collect Results
	tuple = cursor.fetchall()
	id = 0
	if tuple:
		id = tuple[0][0]

	# Set User
	user.username = input_username
	user.password = input_password
	user.id = id
	return True    	

def setFollowingUser(userToFollow):
	# Format SQL to Check if Already Following
	sql = 'SELECT * FROM Following WHERE Follower = "{}" and Following = "{}"'.format(user.id, userToFollow)
	#Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuple = cursor.fetchall()
	if tuple:
		return False
	# if user.username == userToFollow:
	if user.id == userToFollow:
		return False
	# Format SQL to Set Following
	sql = 'INSERT INTO Following (Follower, Following) VALUES ("{}", "{}")'.format(user.id, userToFollow)
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return True

def setMovieLike(movieID):
	# Format SQL to Check if Already Liked
	sql = 'SELECT * FROM UserLikes WHERE user_id = "{}" and movie_id = "{}"'.format(user.id, movieID)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuple = cursor.fetchall()
	if tuple:
		return False
	# Format SQL to Set Like
	sql = 'INSERT INTO UserLikes (user_id, movie_id) VALUES ("{}","{}")'.format(user.id, movieID)
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return True

def unlikeMovie(userID, mid):
	# Format SQL to remove like from table
	sql = 'DELETE FROM UserLikes WHERE user_id="{}" AND movie_id="{}"'.format(userID, mid);
	print sql
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return True

def getRecommendations():
	# Formal SQL to get Followees' movie likes
	sql = 'SELECT UserLikes.movie_id, Movies.title, Movies.year FROM UserLikes, Following, Movies WHERE Following.Follower = "{}" and UserLikes.user_id = Following.Following and UserLikes.movie_id = Movies.movieID GROUP BY UserLikes.movie_id LIMIT 5'.format(user.id)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuples = cursor.fetchall()
	return tuples

def getLikes(userID, username):
	# Format SQL for Likes
	sql = 'SELECT movieID, title FROM Movies WHERE movieID IN (SELECT movie_id FROM UserLikes WHERE user_id={})'.format(userID)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuples = cursor.fetchall()
	newTuples = []
	for tuple in tuples:
		newTuple = (tuple, username)
		newTuples.append(newTuple)

	return newTuples

def getAdvSearchResults(titleBeginning, titleContains, beginningYear, endingYear, \
			genre, actor, beginningRating, endingRating):
	# Format SQL
	pass

# User Class
class User(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password

# Initialize user
user = User("","")

# Flask templates

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		print user.id
		return redirect(url_for('homepage'))

@app.route('/adv_search', methods=['GET', 'POST'])
def adv_search():
	tuples = []
	if request.method == 'POST':
		if request.form['submit'] == 'Like':
			mid = request.form['movieID']
			setMovieLike(mid)
		if request.form['submit'] == 'SEARCH':
			titleBeginning = request.form['titleBeginning']
			titleContains = request.form['titleContains']
			beginningYear = request.form['beginningYear']
			endingYear = request.form['endingYear']
			genre = request.form['genre']
			actor = request.form['actor']
			beginningRating = request.form['beginningRating']
			endingRating = request.form['endingRating']
			tuples = advSearchMovieDB(titleBeginning, titleContains, beginningYear, endingYear,\
						  genre, actor, beginningRating, endingRating)		

	return render_template('adv_search.html', tuples=tuples)

@app.route('/login', methods=['POST'])
def do_login():
	if request.method == 'POST':
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

@app.route("/create_user", methods=['POST','GET'])
def create_user():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if (createUser(username, password)):
			return do_login()

	return render_template('create_user.html')

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

@app.route("/search/<searchTerms>", methods=['POST', 'GET'])
@app.route("/search", methods=['POST', 'GET'])
def search(searchTerms = None):
	tuples = []
	if (searchTerms != None):
		tuples = searchMovieDB(searchTerms)
	print request.method, request.form
	if request.method == 'POST':
		if request.form['submit'] == 'Like':
			mid = request.form['movieID']
			setMovieLike(mid)
		if request.form['submit'] == 'SEARCH':
			searchTerms = request.form['movieSearch']
			tuples = searchMovieDB(searchTerms)
	if tuples:
		return render_template("search.html", tuples=tuples, searchTerms=searchTerms)
	else:
		return render_template("search.html", tuples=None, searchTerms=searchTerms)

@app.route("/likes", methods=['GET', 'POST'])
def likes():
	tuples = []
	if request.method == 'POST':
		if request.form['submit'] == 'Unlike':
			mid = request.form['movieID']
			unlikeMovie(user.id, mid)

	tuples = getLikes(user.id, user.username)
	if tuples:
		return render_template("likes.html", tuples=tuples)
	else:
		return render_template("likes.html", tuples=None)

@app.route("/followLikes/<userID>/<username>", methods=['GET', 'POST'])
def followLikes(userID=None, username=None):
	tuples = []
	tuples = getLikes(userID, username)

        if tuples:
		return render_template("followLikes.html", tuples=tuples)
        else:
		return render_template("followLikes.html", tuples=None)

@app.route("/follow", methods=['POST', 'GET'])
def follow():
	tuples = []
	if request.method == 'POST':
		if request.form['submit'] == 'Follow':
			userID = request.form['userID']
			setFollowingUser(userID)
		if request.form['submit'] == 'SEARCH ALL USERS':
			searchUser = ''
			tuples = searchUserDB(searchUser, user.id)
		elif request.form['submit'] == 'SEARCH':
			searchUser = request.form['userSearch']
			tuples = searchUserDB(searchUser, user.id)

		if tuples:
			return render_template("follow.html", tuples=tuples)
		else:
			return render_template("follow.html", tuples=None)

	else:
		return render_template("follow.html", tuples=tuples)	

@app.route("/get_rec", methods=['GET'])
def get_rec():
	tuples = []
	tuples = getRecommendations()
	return render_template("get_rec.html", tuples=tuples)	

@app.route("/update", methods=['POST', 'GET'])
def update():
	tuples = []
	if request.method == 'POST':
		searchMovie = request.form['movieSearch']
		tuples = searchMovieDB(searchMovie)
		return render_template("update.html", tuples=tuples)
	else:
		return render_template("update.html", tuples=None)

@app.route("/rate/<movieID>/<movieName>", methods=['POST', 'GET'])
def rate(movieID=None, movieName=None):
	if request.method == 'POST':
		userRating = request.form['userRating']
		rating = updateMovieRating(movieID, userRating)
		return render_template("rate.html", movieID=movieID, rating=rating, movieName=movieName)
	else:
		return render_template("rate.html", movieID=movieID, rating="", movieName=movieName)


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=5200, debug=True)
