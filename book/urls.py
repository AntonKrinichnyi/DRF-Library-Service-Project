from django.urls import path, include
from rest_framework import routers
from book.views import AuthorViewSet, BookViewSet

router = routers.DefaultRouter()
router.register("author", AuthorViewSet)
router.register("book", BookViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "book"
