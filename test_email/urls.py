from .views import UserView
from django.urls import path

urlpatterns = [
    path("test", UserView.as_view(),name="test"),
    path("test/<int:id>", UserView.as_view(),name="test")
]

