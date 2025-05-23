from django.urls import path, include
from rest_framework import routers
from borrowing.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowing", BorrowingViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "borrowing"
