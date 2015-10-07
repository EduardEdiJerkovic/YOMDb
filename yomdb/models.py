from django.db import models
	
class Genre( models.Model ):
	name = models.CharField( max_length = 64 )

class Actor( models.Model ):
	name = models.CharField( max_length = 128 )
	
class Movie( models.Model ):
	title = models.CharField( max_length = 128 )
	watched = models.BooleanField( default = False )
	date_added = models.DateTimeField()
	actors = models.ManyToManyField( Actor )
	genres = models.ManyToManyField( Genre )

