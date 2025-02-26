from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import get_user_model
from book.models import Author, Book
from borrowing.models import Borrowing
from payment.models import Payment
from payment.serializers import PaymentDetailSerializer, PaymentSerializer
from rest_framework import status

PAYMENT_URL = "paymnets:payment-list"

def sample_payment(user, **params):
    author = Author.objects.create(
        first_name="Test",
        last_name="Author",
        )
    book = Book.objects.create(
        title="Book Title",
        author=author,
        price=100,
        stock=10,
    )
    borrowing = Borrowing.objects.create(
        borrow_date="2022-12-12",
        expected_return_date="2022-12-12",
        actual_return_date="2022-12-12",
        book=book,
        user=user,
    )
    defaults = {
        "status": "Pending",
        "payment_type": "Payment",
        "borrowing_id": borrowing,
        "session_id": "sesion_id",
        "session_url": "https://session.url",
        "money_to_pay": 100,
    }
    defaults.update(params)
    return Payment.objects.create(**defaults)


class UnautheticatedPaymentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPaymentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            password="password111333",
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_payments(self):
        payment = sample_payment(user=self.user)
        url = reverse("payments:payment-detail", kwargs={"pk": payment.pk})
        response = self.client.get(url)
        serializer = PaymentDetailSerializer(payment, many=False)
        self.assertEqual(response.data, serializer.data)
    
    def test_list_payments(self):
        sample_payment(user=self.user)
        response = self.client.get(PAYMENT_URL)
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        