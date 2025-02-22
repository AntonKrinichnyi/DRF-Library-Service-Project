from rest_framework import serializers
from library.models import Author, Book, Borrowing, Payment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name")


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ("id",
                  "title",
                  "authors",
                  "cover",
                  "inventory",
                  "daily_fee")


