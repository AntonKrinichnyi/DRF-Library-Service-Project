from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    
    def __str__(self):
        return self.first_name + "-" + self.last_name

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)