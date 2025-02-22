from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    
    def __str__(self):
        return self.first_name + "-" + self.last_name

class Book(models.Model):
    class CoverChoises(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"
        
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover = models.CharField(max_length=10, choices=CoverChoises)
    inventory = models.IntegerField(min=0)
    daily_fee = models.DecimalField(max_digits=2, min=0)
    
    def __str__(self):
        return self.title