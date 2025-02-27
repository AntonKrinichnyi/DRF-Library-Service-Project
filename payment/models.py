from django.db import models
from borrowing.models import Borrowing

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
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
