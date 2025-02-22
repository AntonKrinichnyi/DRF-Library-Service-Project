from django.urls import path, include
from rest_framework import routers
from library.views import (AuthorViewSet,
                           BookViewSet,
                           BorowwingViewSet,
                           PaymentViewSet)
