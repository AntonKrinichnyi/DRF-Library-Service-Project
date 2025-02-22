from django.contrib import admin
from library.models import Book, Author, Borrowing, Payment


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Borrowing)
admin.site.register(Payment)
