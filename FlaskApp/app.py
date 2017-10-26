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

cursor = db.cursor;

# Functions

# Inserts a new movie into the database
def insertMovieDB(year, title, mid):
	# Format SQL
	sql = 'INSERT INTO movies (year, title, movieid) VALUES ("{}", "{}", "{}")'.format(year, title, mid)
	# Execute SQL
	cursor.execute(sql)
	db.commit()
	return True

# Flask templates

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/insert", methods=['POST','GET'])
def insert():
	if request.method == 'POST':
		movieName = request.form['movieTitle']
		movieYear = request.form['movieYear']
		movieID = request.form['mid']
		#insertMovieDB(movieYear, movieName, movieID)
		return render_template("insert.html", name=movieName, year=movieYear, mid=movieID)

if __name__ == "__main__":
	app.run(host='dsg1.crc.nd.edu',port=5201,debug=True)

# @app.route("/insert", methods=['POST','GET'])
# def insert():
# 	if request.form['submit'] == 'POST':
# 		movieName = request.form['movieTitle']
# 		movieYear = request.form['movieYear']
# 		movieID = request.form['mid']
# 		insertMovieDB(movieYear, movieName, movieID)
# 		return render_template("insert.html", name=movieName, year=movieYear, mid=movieID)



