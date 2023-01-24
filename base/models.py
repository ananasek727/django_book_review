from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Genre (models.Model):
    name = models.CharField(max_length=127)
    
    def __str__(self):
        return self.name


class Book (models.Model):
    title = models.CharField(max_length=127)
    author = models.CharField(max_length=127)
    numbers_of_review = models.IntegerField()
    stars = models.DecimalField(decimal_places=2, max_digits=5)
    genres = models.ManyToManyField(Genre)
    pub_date_book = models.DateField('date published')
    summary = models.TextField(null=True)
    
    def __str__(self):
        return self.title


class Review (models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=127)
    content = models.TextField(null=True, blank=True)
    stars = models.DecimalField(decimal_places=2, max_digits=5)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


