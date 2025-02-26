from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import get_user_model
from book.models import Author, Book
from borrowing.models import Borrowing
from payment.views import payment_success, payment_cancelled
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
        borrow_date="2024-12-12",
        expected_return_date="2024-12-15",
        actual_return_date="2024-12-14",
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


class PaymentSuccessTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.session_id = "test_session_id"
        self.user = get_user_model().objects.create_user(
            email="test@user.com", password="password111333"
        )
        self.author = Author.objects.create(
            first_name="Test",
            last_name="Author")
        self.book = Book.objects.create(
            title="Sample",
            authors=self.author,
            cover="Hard",
            inventory=23,
            daily_fee=2.45,
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date="2024-12-12",
            expected_return="2024-12-15",
            actual_return="2024-12-14",
            book=self.book,
            user=self.user,
        )
        self.payment = Payment.objects.create(
            status=Payment.StatusChoices.PENDING,
            type=Payment.TypeChoices.PAYMENT,
            borrowing_id=self.borrowing.id,
            session_url=f"https://checkout.stripe.com/pay/{self.session_id}",
            session_id=self.session_id,
            money_to_pay=25.50,
        )

    @patch("stripe.checkout.Session.retrieve")
    def test_payment_success(self, mock_retrieve):
        mock_session = MagicMock()
        mock_session.payment_status = "paid"
        mock_retrieve.return_value = mock_session

        request = self.factory.get("/payment_success_url")

        response = payment_success(request, self.session_id)

        self.payment.refresh_from_db()

        self.assertEqual(self.payment.status, Payment.StatusChoices.PAID)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Payment successful")

    @patch("stripe.checkout.Session.retrieve")
    def test_payment_not_successful(self, mock_retrieve):
        mock_session = MagicMock()
        mock_session.payment_status = "unpaid"
        mock_retrieve.return_value = mock_session

        request = self.factory.get("/payment_success_url")

        response = payment_success(request, self.session_id)

        self.payment.refresh_from_db()

        self.assertEqual(self.payment.status, Payment.StatusChoices.PENDING)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Payment failed")

    def test_payment_cancel(self):
        request = self.factory.get("/payment_cancelled_url")
        response = payment_cancelled(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode(),
            "Payment cancelled",
        )
