from rest_framework import viewsets, mixins
from django.http import HttpResponse
import stripe
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from library_service import settings
from payment.models import Payment
from payment.serializers import PaymentDetailSerializer, PaymentSerializer


class PaymentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Payment.objects.all().select_related("borrowing_id")
    serializer_class = PaymentSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
def payment_succes(request, session_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        payment = Payment.objects.get(session_id=session_id)
        payment.status = "paid"
        payment.save()
        return HttpResponse("Payment succesful")
    return HttpResponse("Payment failed")

def payment_cancel(request):
    return HttpResponse("Payment canceled")
