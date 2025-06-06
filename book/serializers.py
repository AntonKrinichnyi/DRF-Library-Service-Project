from rest_framework import serializers
from book.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "authors", "cover", "inventory", "daily_fee")


class BookListSerializer(BookSerializer):
    authors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    
    class Meta:
        model = Book
        fields = ("id", "title", "authors", "cover", "inventory", "daily_fee")
