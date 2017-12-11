from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
import sys
import MySQLdb
import os



def getAdvSearchResults(titleBeginning, titleContains, beginningYear, endingYear, \
			genre, actor, beginningRating, endingRating):
	### Format inputs into SQL

	# Title
	titleClause = ''
	if titleBeginning != '':
		print('**title beginning = {}'.format(titleBeginning))
		titleClause += 'm.title LIKE \'{}%\' AND '.format(titleBeginning)
	if titleContains != '':
		print('**title contains = {}'.format(titleContains))
		titleClause += 'm.title LIKE \'%{}%\' AND '.format(titleContains)
	
	# Year Range
	
	yearClause = ''
	if beginningYear != '':
		yearClause += 'm.year > {} AND '.format(beginningYear) 
	if endingYear != '':
		yearClause += 'm.year < {} AND '.format(endingYear)	

	# Genre
	genreClause = ''
	if genre != 'All' and genre != '':
		genreClause = 'g.genre=\'' + genre + '\' AND '
	
	# Actor
	actorClause = ''
	if actor != '':	
		actorClause += 'a.name LIKE \'%{}%\' AND a.actorID=ai.actorID AND '.format(actor)
	
	# Rating
	ratingClause = ''
	if beginningRating != '':
		ratingClause += 'r.rating >= {}'.format(beginningRating)
		if endingRating != '':
			ratingClause += ' AND '			

	if endingRating != '':
		ratingClause += 'rating =< {}'.format(endingRating)
	

		
	sql = 	'''	
			SELECT 	m.movieID, m.title, m.year, r.Rating
	       		FROM 	Movies m, Ratings r, Genres g, Actors a, AppearsIn ai
	       		WHERE 	m.movieID=g.movieID AND 
	       			m.movieID=r.MovieID AND
				m.movieID=ai.movieID AND
		     		{}
		     		{}
		     		{}
		     		{}
		     		{}'''.format(titleClause, yearClause, genreClause, actorClause, ratingClause) 
			 
	print(sql)

#getAdvSearchResults('begin', 'contains', 1900, 2000, 'Action', 'Brad Pitt', 5.0, 8.0)
getAdvSearchResults('Up', '', 2005, 2017, 'Animation', 'Pete Docter', 1.0, 10.0)
