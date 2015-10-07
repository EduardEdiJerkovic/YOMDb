from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import *

import requests


def index(request):
	movies = [ { 'id' : m.id, 'title' : m.title, 'genres' : [ g.name for g in m.genres.all() ], 
		'actors' : [ a.name for a in m.actors.all() ], 'watched' : m.watched, 'date_added' : m.date_added } 
		for m in Movie.objects.all() ]
	return render( request, 'yomdb/index.html', { 'movies' : movies } )


def add_movie( request ):
	movie_title = request.POST[ 'movie_title' ]

	response = requests.get( 'http://omdbapi.com/?t={}&r=json'.format( movie_title ) )
	data = response.json()
	
	if data.get( 'Title' ):	
		movie = Movie( title = data[ 'Title' ], watched = False, date_added = timezone.now() )
		movie.save()
	
		for actor_name in data[ 'Actors' ].split( ',' ):
			actor, created = Actor.objects.get_or_create( name = actor_name )
			movie.actors.add( actor )
	
		for genre_name in data[ 'Genre' ].split( ',' ):
			genre, created = Genre.objects.get_or_create( name = genre_name )
			movie.genres.add( genre )
		
	return redirect( 'index' )


def show_filtered( request ):
	filter_type = request.GET[ 'type' ]
	filter_content = request.GET[ 'content' ]
	
	if filter_type == "0":
		movie_objs = Movie.objects.filter( title__icontains = filter_content )
	elif filter_type == "1":
		movie_objs = Movie.objects.filter( actors__name__icontains = filter_content )
	elif filter_type == "2":
		movie_objs = Movie.objects.filter( genres__name__icontains = filter_content )
	else:
		movie_objs = Movie.objects.all()
		
	type_name = { "0" : "title", "1" : "actor", "2" : "genre" }[ filter_type ]
	
	movies = [ { 'id' : m.id, 'title' : m.title, 'genres' : [ g.name for g in m.genres.all() ], 
		'actors' : [ a.name for a in m.actors.all() ], 'watched' : m.watched, 'date_added' : m.date_added } 
		for m in movie_objs ]
	
	return render( request, 'yomdb/filtered.html', { 'filter_type' : type_name, 'filter_content' : filter_content, 'movies' : movies } )
	

def delete_movie( request, movie_id ):
	movie = get_object_or_404( Movie, pk = movie_id )
	movie.delete()
	return redirect( 'index' )
	
def mark_watched( request, movie_id ):
	movie = get_object_or_404( Movie, pk = movie_id )
	movie.watched = True
	movie.save()
	return redirect( 'index' )
	
