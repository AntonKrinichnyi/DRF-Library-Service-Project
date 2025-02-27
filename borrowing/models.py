from django.db import models
from library_service import settings
from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateTimeField(blank=True, null=True)
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name="borrowings",
                             blank=True,
                             null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f"{self.user.email} borrow by {self.borrow_date}"

    class Meta:
        ordering = ["-borrow_date"]