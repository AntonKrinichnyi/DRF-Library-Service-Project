from datetime import datetime
from rest_framework import serializers
from book.serializers import BookListSerializer
from borrowing.models import Borrowing
from payment.serializers import PaymentSerializer
from django.db import transaction
from telegram_notificated import send_telegram_notification


class BorrowingSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField(read_only=True)
    payment = PaymentSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "payment",
        )

    def get_is_active(self, obj):
        return obj.actual_return_date is None


class BorrowingListSerializer(BorrowingSerializer):
    payment = PaymentSerializer(many=False, read_only=True)
    book_title = serializers.CharField(source="book.title", read_only=True)
    book_author = serializers.CharField(source="book.author", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "expected_return_date",
            "actual_return_date",
            "book_title",
            "book_author",
            "payment",
        )

    def get_is_active(self, obj):
        return obj.actual_return_date is None


class BorrowingDetailSerializer(BorrowingSerializer):
    books = BookListSerializer(many=True, read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)
    payment = PaymentSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "books",
            "expected_return_date",
            "payment",
            "is_active",
            "borrow_date",
            "actual_return_date",
        )

    def get_is_active(self, obj):
        return obj.actual_return_date is None


class BorrowingCreateSerializer(BorrowingDetailSerializer):
    payment = PaymentSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "expected_return_date",
            "actual_return_date",
            "payment",
        )
        read_only_fields = ("id", "actual_return_date", "payment")

    def validate_book(self, book):
        if book.inventory == 0:
            raise serializers.ValidationError("Book is out of stock")
        return book

    def validate_expected_return_date(self, expected_return_date):
        if expected_return_date < datetime.now().date():
            raise serializers.ValidationError(
                "Expected return date must be in the future"
            )
        return expected_return_date


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "expected_return_date", "actual_return_date", "borrow_date")
        read_only_fields = ("id", "actual_return_date")

    @transaction.atomic
    def validate(self, attrs):
        borrowing = self.instance
        if borrowing.actual_return_date is not None:
            raise serializers.ValidationError("Book has already been returned")
        return super().validate(attrs=attrs)
    
    def update(self, instance):
        book = instance.book
        instance.actual_return_date = datetime.now().date()
        instance.save()
        book.inventory += 1
        book.save()
        send_telegram_notification(
            f"Book {book.title} returned by {instance.user.email}"
        )
        return instance
