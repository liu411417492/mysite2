from django.db import models

# Create your models here.
class Author(models.Model):
    AuthorID = models.IntegerField(primary_key = True)
    Name = models.CharField(max_length= 30)
    Age = models.CharField(max_length = 10)
    timestamp = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length = 30)
    def __unicode__(self):
    	return self.Name
#adsf
class Book(models.Model):
	ISBN = models.IntegerField(primary_key = True)
	Title = models.CharField(max_length = 30)
	Author = models.ForeignKey(Author)
	Publisher = models.CharField(max_length = 30)
	PublishDate = models.DateTimeField(auto_now_add=True)
	Price = models.FloatField()