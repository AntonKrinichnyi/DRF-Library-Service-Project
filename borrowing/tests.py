from django.test import TestCase
from datetime import datetime, date
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse
from book.models import Book, Author
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer