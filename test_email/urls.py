from .views import UserView,SendingEmailView
from django.urls import path

urlpatterns = [
    path("test", UserView.as_view(),name="test"),
    path("test/<int:id>", UserView.as_view(),name="test"),
    path("send-emails",SendingEmailView.as_view(),name="send-emails")
]

