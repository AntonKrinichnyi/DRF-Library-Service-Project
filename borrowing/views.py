from rest_framework import viewsets
from rest_framework.decorators import action
from django.db import transaction
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from telegram_notificated import send_telegram_notification
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (Borrowing.objects.filter(user=self.request.user).
                    prefetch_related("book__authors").select_related("user"))
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
        book = serializer.validated_data["book"]
        with transaction.atomic():
            book.inventory -= 1    
            book.save()
            serializer.save(user=self.request.user)
            send_telegram_notification(
                f"User {self.request.user.email} borrowed book {book.title}"
            )
            create_stripe_session(serializer.instance)

    @extend_schema(
        request=BorrowingReturnSerializer,
        responses={200: BorrowingReturnSerializer(many=True)},
        methods=["POST"],
        description="Returns a book by its ID.",
    )
    @action(
        detail=True,
        methods=["get", "pdate"],
        url_path="return",
        serializer_class=BorrowingReturnSerializer,
    )
    def return_book(self, request, pk=None):
        with transaction.atomic():
            borrowing = self.get_object()
            if borrowing.actual_return_date:
                return Response(
                    {"error": "Book already returned"},
                    status=status.HTTP_400_BAD_REQUEST)
            actual_return_date = datetime.now()
            update = BorrowingReturnSerializer(
                borrowing,
                context={"request": self.request},
                data={"actual_return_date": actual_return_date},
                partial=True
            )
            update.is_valid(raise_exception=True)
            update.save()
            return Response({"success": "Book returned"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
