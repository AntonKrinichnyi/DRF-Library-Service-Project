from django.urls import path, include
from rest_framework import routers
from payment.views import (PaymentViewSet,
                           payment_succes,
                           payment_cancel)

router = routers.DefaultRouter()
router.register("payment", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("payment_succes/<str:session_id>/",
         payment_succes,
         name="payment_succes"),
    path("payment_cancel/", payment_cancel, name="payment_cancel"),
]

app_name = "payment"
