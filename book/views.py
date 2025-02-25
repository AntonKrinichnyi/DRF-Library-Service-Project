from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser
from book.models import Author, Book
from book.serializers import AuthorSerializer, BookListSerializer, BookSerializer


class AuthorViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return []
        return [IsAdminUser()]


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
    
    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return []
        return [IsAdminUser()]
