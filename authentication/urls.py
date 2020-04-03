from django.conf.urls import url

from .views import RegistrationAPIView

app_name = 'authentication'
urlpatterns = [
    url('users/', RegistrationAPIView.as_view()),
]