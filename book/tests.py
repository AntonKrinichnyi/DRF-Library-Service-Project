from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient
from book.models import Book, Author
from book.serializers import BookSerializer, AuthorSerializer

BOOK_URL = reverse("book:book-list")
AUTHOR_URL = reverse("book:author-list")

def sample_author(**params):
    defaults = {
        "first_name": "Sample",
        "last_name": "Author"
    }
    defaults.update(params)
    return Author.objects.create(**defaults)

def sample_book(**params):
    defaults = {
        "title": "Sample Book",
        "isbn": "1234567890123",
        "author": sample_author()
    }
    defaults.update(params)
    return Book.objects.create(**defaults)

class UnauthenticatedBookTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_book_list_unauthenticated(self):
        sample_author()
        sample_book()
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_author_list_unauthenticated(self):
        sample_author()
        res = self.client.get(AUTHOR_URL)
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_book_create_unauthenticated(self):
        payload = {"title": "Sample Book", "isbn": "1234567890123", "author": sample_author().id}
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_author_create_unauthenticated(self):
        payload = {"first_name": "Sample", "last_name": "Author"}
        res = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="sample@test.com",
            password="testpass1133",
        )
        self.client.force_authenticate(self.user)
    
    def test_book_list_authenticated(self):
        sample_author()
        sample_book()
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_author_list_authenticated(self):
        sample_author()
        res = self.client.get(AUTHOR_URL)
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def create_book_authenticated(self):
        payload = {"title": "Sample Book", "isbn": "1234567890123", "author": sample_author().id}
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def create_author_authenticated(self):
        payload = {"first_name": "Sample", "last_name": "Author"}
        res = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="testpass1133",
        )
        self.client.force_authenticate(self.admin_user)
    
    def test_create_book_by_admin(self):
        sample_author()
        payload = {"title": "Sample Book", "isbn": "1234567890123", "author": sample_author().id}
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    def test_create_author_by_admin(self):
        payload = {"first_name": "Sample", "last_name": "Author"}
        res = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
