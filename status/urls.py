from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import StatusFeedAPIView, StatusViewSet

app_name = 'status'

router = DefaultRouter(trailing_slash=False)
router.register(r'status', StatusViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^status/feed/?$', StatusFeedAPIView.as_view()),

    
]