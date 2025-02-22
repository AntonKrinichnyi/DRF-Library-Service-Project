from django.urls import path, include
from rest_framework import routers
from library.views import (AuthorViewSet,
                           BookViewSet,
                           BorrowingViewSet,
                           PaymentViewSet)

router = routers.DefaultRouter()
router.register("author", AuthorViewSet)
router.register("book", BookViewSet)
router.register("borrowing", BorrowingViewSet)
router.register("payment", PaymentViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "library"
