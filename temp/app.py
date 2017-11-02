#!/usr/bin python

# Libraries
from flask import Flask, render_template, request, redirect, url_for

import sys
import MySQLdb

# Global Variables

# Database info
SQL_ADDR= 'localhost'
SQL_USER= 'kscherme'
SQL_PASSWD= 'crossroads111'
SQL_DB= 'crossroads'

# Flask info
app = Flask(__name__)

# Setup Database
db = MySQLdb.connect(host=SQL_ADDR, user=SQL_USER, passwd=SQL_PASSWD, db=SQL_DB)

cursor = db.cursor();

# Functions

# Inserts a new movie into the database
def insertMovieDB(year, title):
	# Format SQL
	sql = 'INSERT INTO Movies (year, title) VALUES ("{}", "{}")'.format(year, title)
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return True

# Searches for movie by title
def searchMovieDB(title):
	# Format SQL
	sql = 'SELECT * FROM Movies WHERE Title = "{}"'.format(title)
	# Execute SQL
	cursor.execute(sql)
	# Collect Results
	tuples = cursor.fetchall()
	# Return results
	if tuples:
		return (int(tuples[0][0]), tuples[0][1], int(tuples[0][2])) 
	else:
		return 0

# Deleted movie from database
def deleteMovie(movieID):
	# Format SQL
	sql = 'DELETE FROM Movies WHERE MovieID = {}'.format(movieID)
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return True

# Update movie rating
def updateMovieRating(movieID, userRating):
	# Get Current Rating
	# Also get number of votes
	sql = 'SELECT Rating, numVotes FROM Ratings WHERE MovieID = "{}"'.format(movieID)
	cursor.execute(sql)
	rows = cursor.fetchall()
	currentRating = rows[0][0]
	NumVotes = rows[0][1]
	# currentRating, NumVotes = cursor.fetchall()
	# if currentRating:
	# 	currentRating = int(currentRating[0])
	# 	NumVotes = int(NumVotes[0])
	# else:
	# 	return 0
	# Calculate New Rating
	SumRatings = currentRating*NumVotes
	SumRatings = SumRatings + int(userRating)
	NumVotes = NumVotes + 1
	newRating = SumRatings / NumVotes 
	#newRating = currentRating + 10
	# Format SQL
	sql = 'UPDATE Ratings SET Rating = "{}", numVotes = "{}" WHERE MovieID = "{}"'.format(newRating, NumVotes, movieID)
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return newRating

# Flask templates

@app.route("/")
def homepage():
	return render_template('homepage.html')

@app.route("/insert", methods=['POST','GET'])
def insert():
	if request.method == 'POST': 
		movieName = request.form['movieTitle']
		movieYear = request.form['movieYear']
		insertMovieDB(movieYear, movieName)
		return render_template("insert.html", name=movieName, year=movieYear)
	else:
		return render_template("insert.html", name="", year="")


@app.route("/search", methods=['POST', 'GET'])
def search():
	if request.method == 'POST':
		searchMovie = request.form['movieSearch']
		tuples = searchMovieDB(searchMovie)
		return render_template("search.html", movieID=tuples[0], name=tuples[1], year=tuples[2])#result=tuples)
	else:
		return render_template("search.html", movieID="", name="", year="")

@app.route("/delete", methods=['POST'])
def delete():
	if request.method == 'POST':
		movieID = request.form['movieID']
		deleteMovie(movieID)
		return render_template('search.html')
	else:
		return render_template('search.html')

@app.route("/update", methods=['POST','GET'])
def update():
	if request.method == 'POST':
		movieID = request.form['movieID']
		userRating = request.form['userRating']
		rating = updateMovieRating(movieID, userRating)
		return render_template("update.html", movieID=movieID, rating=rating)
	else:
		return render_template("update.html", movieID="", rating="")
		

if __name__ == "__main__":
	app.run(host='dsg1.crc.nd.edu',port=5202,debug=True)



