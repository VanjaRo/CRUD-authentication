from django.urls import path

from .views import LoginAPIView, RegistrationAPIView, UserRetriveUpdateAPIView

app_name = 'authentication'
urlpatterns = [
    path('user', UserRetriveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('token-auth/', LoginAPIView.as_view())
]
