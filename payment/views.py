from rest_framework import viewsets
from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().select_related("borrowing_id")
    serializer_class = PaymentSerializer
