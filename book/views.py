from rest_framework import viewsets, mixins
from book.models import Author, Book
from book.serializers import AuthorSerializer, BookListSerializer, BookSerializer


class AuthorViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().prefetch_related("authors")
    serializer_class = BookSerializer
    
    def get_queryset(self):
        title = self.request.query_params.get("title")
        queryset = self.queryset
        if title:
            return self.queryset.filter(title__icontains=title)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookListSerializer
        return BookSerializer