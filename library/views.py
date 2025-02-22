from django.shortcuts import render
from rest_framework import viewsets, mixins
from library.models import Author, Book, Borrowing, Payment
from library.serializers import (AuthorSerializer,
                                 BookSerializer,
                                 BorrowingSerializer,
                                 Payment)


class AuthorViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
