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


class BorrowingSerializer(serializers.Serializer):
    class Meta:
        model = Borrowing
        fields = ("id",
                  "expected_return_date",
                  "actual_return_date",
                  "book",
                  "user")


