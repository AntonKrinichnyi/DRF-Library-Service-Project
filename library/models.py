from django.db import models

from library_service import settings


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


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField()
    book = models.ManyToManyField(Book)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f"{self.user.email} borrow by {self.borrow_date}"


class Payment(models.Model):
    class StatusChoises(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"
    
    class TypeChoises(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"
    
    status = models.CharField(
        choices=StatusChoises,
        max_length=15
    )
    payment_type = models.CharField(
        choices=TypeChoises,
        max_length=15
    )
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.IntegerField()
    money_to_pay = models.DecimalField(max_digits=2)
