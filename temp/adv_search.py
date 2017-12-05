from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
import sys
import MySQLdb
import os



def getAdvSearchResults(titleBeginning, titleContains, beginningYear, endingYear, \
			genre, actor, beginningRating, endingRating):
	# Format inputs into SQL
	titleBeginning = titleBeginning + '%'
	titleContains = '%' + titleContains + '%'

	genreClause = ''
	if genre != 'All' and genre != '':
		genreClause = 'g.genre=' + genre + ' AND'
	
	actor = '%' + actor + '%'
	

		
	sql = 'SELECT m.movieID, m.title, m.year, r.Rating\
	       FROM Movies m, Ratings r, Genres g, Actors a, AppearsIn ai\
	       WHERE m.movieID=g.movieID AND m.movieID=r.MovieID AND m.movieID=ai.movieID\
		     m.title LIKE \'{}\' AND m.title LIKE \'{}\' AND\
		     m.year > {} AND m.year < {} AND\
		     {}\
		     a.name LIKE \'{}\' AND a.actorID=ai.actorID AND\
		     r.rating > {} AND r.rating < {}'.format(
			titleBeginning, titleContains, beginningYear, endingYear,
			genreClause, actor, beginningRating, endingRating) 
			 
	print(sql)

getAdvSearchResults('begin', 'contains', 1900, 2000, 'Action', 'Brad Pitt', 5.0, 8.0)
