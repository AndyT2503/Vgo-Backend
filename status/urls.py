from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import StatusFeedAPIView, StatusViewSet, StatusFavoriteAPIView, CommentsListCreateAPIView, CommentsDestroyAPIView

app_name = 'status'

router = DefaultRouter(trailing_slash=False)
router.register(r'status', StatusViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^status/feed/?$', StatusFeedAPIView.as_view()),

    url(r'^status/(?P<status_slug>[-\w]+)/favorite/?$',
        StatusFavoriteAPIView.as_view()),

    url(r'^status/(?P<status_slug>[-\w]+)/comments/?$', 
        CommentsListCreateAPIView.as_view()),

    url(r'^status/(?P<article_slug>[-\w]+)/comments/(?P<comment_pk>[\d]+)/?$',
        CommentsDestroyAPIView.as_view()),
]