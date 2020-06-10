from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Status
from .renderers import StatusJSONRenderer
from .serializers import StatusSerializer

class StatusViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    lookup_field = 'slug'
    queryset = Status.objects.select_related('profile', 'profile__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (StatusJSONRenderer,)
    serializer_class = StatusSerializer

    def get_queryset(self):
        queryset = self.queryset

        profile = self.request.query_params.get('profile', None)
        if profile is not None:
            queryset = queryset.filter(profile__user__name=profile)

        return queryset

    def create(self, request):
        serializer_context = {
            'profile': request.user.profile,
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