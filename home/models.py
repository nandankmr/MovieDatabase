from django.db import models


class Movie(models.Model):
    logo = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    imdb_link = models.CharField(max_length=1000, unique=True)
    year = models.CharField(max_length=4)
    certificate = models.CharField(max_length=20)
    runtime = models.CharField(max_length=25)
    genre = models.CharField(max_length=100)
    imdb_rating = models.CharField(max_length=3)
    metascore = models.CharField(max_length=2)
    director = models.CharField(max_length=100)
    # director_link = models.CharField(max_length=1000)
    cast = models.CharField(max_length=1000)
    # cast_link = models.CharField(max_length=2000)
    gross = models.CharField(max_length=20)

    def __str__(self):
        return str(self.title) + ' - ' + str(self.year)


class Director(models.Model):
    logo = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    imdb_link = models.CharField(max_length=1000, primary_key=True)
    date_of_birth = models.CharField(max_length=100, default='None')
    movies = models.CharField(max_length=2000)
    movie_links = models.CharField(max_length=4000, default='None')
    profession = models.CharField(max_length=200)
    birth_place = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actor(models.Model):
    logo = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    imdb_link = models.CharField(max_length=1000, primary_key=True)
    date_of_birth = models.CharField(max_length=100, default='None')
    movies = models.CharField(max_length=2000)
    movie_links = models.CharField(max_length=4000, default='None')
    profession = models.CharField(max_length=200)
    birth_place = models.CharField(max_length=100)

    def __str__(self):
        return self.name
