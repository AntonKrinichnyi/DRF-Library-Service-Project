from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.first_name + "-" + self.last_name

class Book(models.Model):
    class CoverChoises(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"
        
    title = models.CharField(max_length=255, unique=True)
    authors = models.ManyToManyField(Author)
    cover = models.CharField(max_length=10, choices=CoverChoises)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title
