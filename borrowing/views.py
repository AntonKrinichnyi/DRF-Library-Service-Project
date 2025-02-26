from rest_framework import viewsets
from rest_framework.decorators import action
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from telegram_notificated import send_telegramm_notification
from payment.stripe_payment import create_stripe_session
from borrowing.models import Borrowing
from borrowing.serializers import (BorrowingCreateSerializer,
                                   BorrowingDetailSerializer,
                                   BorrowingListSerializer,
                                   BorrowingSerializer,
                                   BorrowingReturnSerializer)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        queryset = (Borrowing.objects.filter(user=self.request.user).
                    prefetch_related("book__author").select_related("user"))
        return queryset
    
    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action in ["create", "update", "partial_update"]:
            return BorrowingCreateSerializer
        return BorrowingSerializer
    
    def perform_create(self, serializer):
        with transaction.atomic():
            book = serializer.validated_data["book"]
            book.inventory -= 1
            book.save()
            serializer.save(user=self.request.user)
            send_telegramm_notification(
                f"User {self.request.user.email} borrowed book {book.title}"
            )
            create_stripe_session(serializer.instance)
    
    @action(
        detail=True,
        methods=["post"],
        url_path="return",
        url_name="return",
        serializer_class=BorrowingReturnSerializer,
    )
    def return_book(self, request, pk=None):
        with transaction.atomic():
            borrowing = self.get_object()
            borrowing.actual_return_date = datetime.now()
            borrowing.save()
            borrowing.book.inventory += 1
            borrowing.book.save()
            send_telegramm_notification(
                f"User {self.request.user.email} returned book {borrowing.book.title}"
            )
            return Response(
                BorrowingSerializer(borrowing).data, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
