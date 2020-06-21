from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Status, Comment
from .renderers import StatusJSONRenderer, CommentJSONRenderer
from .serializers import StatusSerializer, CommentSerializer

class StatusViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    lookup_field = 'slug'
    queryset = Status.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (StatusJSONRenderer,)
    serializer_class = StatusSerializer

    def get_queryset(self):
        queryset = self.queryset

        profile = self.request.query_params.get('author', None)
        if profile is not None:
            queryset = queryset.filter(profile__user__name=profile)

        return queryset

    def create(self, request):
        serializer_context = {
            'author': request.user.profile,
            'request': request
        }
        serializer_data = request.data.get('status', {})

        serializer = self.serializer_class(
        data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Status.DoesNotExist:
            raise NotFound('A status post with this slug does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Status.DoesNotExist:
            raise NotFound('A status post with this slug does not exist.')
            
        serializer_data = request.data.get('status', {})

        serializer = self.serializer_class(
            serializer_instance, 
            context=serializer_context,
            data=serializer_data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class StatusFeedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Status.objects.all()
    renderer_classes = (StatusJSONRenderer,)
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.filter(
            status__in=self.request.user.profile.follows.all()
        )

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)

class CommentsListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'status__slug'
    lookup_url_kwarg = 'status_slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.select_related(
        'status', 'status__author', 'status__author__user',
        'author', 'author__user'
    )
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    def filter_queryset(self, queryset):
        # The built-in list function calls `filter_queryset`. Since we only
        # want comments for a specific status, this is a good place to do
        # that filtering.
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        return queryset.filter(**filters)

    def create(self, request, status_slug=None):
        data = request.data.get('comment', {})
        context = {'author': request.user.profile}

        try:
            context['status'] = Status.objects.get(slug=status_slug)
        except Status.DoesNotExist:
            raise NotFound('A status with this slug does not exist.')

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentsDestroyAPIView(generics.DestroyAPIView):
    lookup_url_kwarg = 'comment_pk'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()

    def destroy(self, request, status_slug=None, comment_pk=None):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class StatusFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (StatusJSONRenderer,)
    serializer_class = StatusSerializer

    def delete(self, request, status_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            status = Status.objects.get(slug=status_slug)
        except Status.DoesNotExist:
            raise NotFound('An status with this slug was not found.')

        profile.unfavorite(status)

        serializer = self.serializer_class(status, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, status_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            status = Status.objects.get(slug=status_slug)
        except Status.DoesNotExist:
            raise NotFound('An status with this slug was not found.')

        profile.favorite(status)

        serializer = self.serializer_class(status, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
